""" Network Manager CLI (nmcli) functions """
import subprocess
import typing
import logging
import shutil
import pandas
from io import StringIO
from time import sleep
import requests
from datetime import datetime

from .config import URL

NMCLI = shutil.which("nmcli")
if not NMCLI:
    raise ImportError('Could not find NetworkManager "nmcli"')

NMCMD = [NMCLI, "-g", "SSID,BSSID,FREQ,SIGNAL", "device", "wifi"]  # Debian stretch, Ubuntu 18.04
NMLEG = [NMCLI, "-t", "-f", "SSID,BSSID,FREQ,SIGNAL", "device", "wifi"]  # ubuntu 16.04
NMSCAN = [NMCLI, "device", "wifi", "rescan"]


def cli_config_check():
    # %% check that NetworkManager CLI is available and WiFi is active
    ret = subprocess.check_output([NMCLI, "-t", "radio", "wifi"], universal_newlines=True, timeout=1.0).strip().split(":")

    if "enabled" not in ret and "disabled" in ret:
        raise ConnectionError("must enable WiFi, perhaps via nmcli radio wifi on")


def get_cli() -> typing.Dict[str, typing.Any]:

    ret = subprocess.run(NMCMD, timeout=1.0)
    if ret.returncode != 0:
        raise ConnectionError(f"could not connect with NetworkManager for WiFi")
    sleep(0.5)  # nmcli errored for less than about 0.2 sec.
    # takes several seconds to update, so do it now.
    ret = subprocess.run(NMSCAN, timeout=1.0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if ret.returncode != 0:
        logging.error(f"consider slowing scan cadence.  {ret.stderr}")

    dat = pandas.read_csv(
        StringIO(ret.stdout),
        sep=r"(?<!\\):",
        index_col=False,
        header=0,
        encoding="utf8",
        engine="python",
        dtype=str,
        usecols=[0, 1, 3],
        names=["ssid", "macAddress", "signalStrength"],
    )
    # %% optout
    dat = dat[~dat["ssid"].str.endswith("_nomap")]
    if dat.shape[0] < 2:
        logging.warning("cannot locate since at least 2 BSSIDs required")
        return None
    # %% cleanup
    dat["ssid"] = dat["ssid"].str.replace("nan", "")
    dat["macAddress"] = dat["macAddress"].str.replace(r"\\:", ":")
    # %% JSON
    jdat = dat.to_json(orient="records")
    jdat = '{ "wifiAccessPoints":' + jdat + "}"
    logging.debug(jdat)
    # %% cloud MLS
    try:
        req = requests.post(URL, data=jdat)
        if req.status_code != 200:
            logging.error(req.text)
            return None
    except requests.exceptions.ConnectionError as e:
        logging.error(f"no network connection.  {e}")
        return None
    # %% process MLS response
    jres = req.json()
    loc = jres["location"]
    loc["accuracy"] = jres["accuracy"]
    loc["N"] = dat.shape[0]  # number of BSSIDs used
    loc["t"] = datetime.now()

    return loc
