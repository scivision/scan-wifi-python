""" Network Manager CLI (nmcli) functions """
import subprocess
import typing
import logging
import shutil
import io
import requests
import json
from math import log10
from datetime import datetime

from .config import URL

CLI = shutil.which("netsh")
if not CLI:
    raise ImportError('Could not find NetSH "netsh"')

CMD = [CLI, "wlan", "show", "networks", "mode=bssid"]


def cli_config_check():
    # %% check that NetSH CLI is available and WiFi is active
    ret = subprocess.check_output(CMD, universal_newlines=True, timeout=1.0)
    for line in ret.split("\n"):
        if "networks currently visible" in line:
            return
        if "The wireless local area network interface is powered down and doesn't support the requested operation" in line:
            raise ConnectionError("must enable WiFi, it appears to be turned off.")
    logging.error("could not determine WiFi state.")


def get_cli() -> typing.Dict[str, typing.Any]:
    """ get signal strength using CLI """
    ret = subprocess.run(CMD, timeout=1.0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if ret.returncode != 0:
        logging.error(f"consider slowing scan cadence.  {ret.stderr}")

    dat: typing.List[typing.Dict[str, str]] = []
    out = io.StringIO(ret.stdout)
    for line in out:
        d: typing.Dict[str, str] = {}
        if not line.startswith("SSID"):
            continue
        ssid = line.split(":", 1)[1].strip()
        # optout
        if ssid.endswith("_nomap"):
            continue
        # find BSSID MAC address
        for line in out:
            if not line[4:9] == "BSSID":
                continue
            d["macAddress"] = line.split(":", 1)[1].strip()
            for line in out:
                if not line[9:15] == "Signal":
                    continue
                signal_percent = int(line.split(":", 1)[1][:3])
                d["signalStrength"] = str(signal_percent_to_dbm(signal_percent))
                d["ssid"] = ssid
                dat.append(d)
                d = {}
                break
    if len(dat) < 2:
        logging.warning("cannot locate since at least 2 BSSIDs required")
        return None
    # %% JSON
    jdat = json.dumps(dat)
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
    loc["N"] = len(dat)  # number of BSSIDs used
    loc["t"] = datetime.now()

    return loc


def signal_percent_to_dbm(percent: int) -> int:
    """ arbitrary conversion factor from Windows WiFi signal % to dBm
    assumes 100% is -30 dBm

    Parameters
    ----------
    percent: int
        signal strength as percent 0..100

    Returns
    -------
    meas_dBm: int
        truncate to nearest integer because of uncertainties
    """
    REF = -30  # dBm
    ref_mW = 10 ** (REF / 10) / 1000
    meas_mW = max(ref_mW * percent / 100, 1e-7)
    meas_dBm = 10 * log10(meas_mW) + 30
    return int(meas_dBm)
