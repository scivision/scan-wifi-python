""" Network Manager CLI (nmcli) functions """
import subprocess
import logging
import shutil
import pandas
import typing as T
from io import StringIO
from time import sleep

NMCLI = shutil.which("nmcli")
if not NMCLI:
    raise ImportError('Could not find NetworkManager "nmcli"')

NMCMD = [NMCLI, "-g", "SSID,BSSID,FREQ,SIGNAL", "device", "wifi"]  # Debian stretch, Ubuntu 18.04
NMLEG = [NMCLI, "-t", "-f", "SSID,BSSID,FREQ,SIGNAL", "device", "wifi"]  # ubuntu 16.04
NMSCAN = [NMCLI, "device", "wifi", "rescan"]


def cli_config_check() -> bool:
    # %% check that NetworkManager CLI is available and WiFi is active
    ret = subprocess.run([NMCLI, "-t", "radio", "wifi"], stdout=subprocess.PIPE, text=True, timeout=2)

    if ret.returncode != 0:
        return False

    stdout = ret.stdout.strip().split(":")
    if "enabled" in stdout:
        return True

    if "disabled" in stdout:
        logging.error(
            """must enable WiFi, perhaps via:
nmcli radio wifi on"""
        )
        return False

    logging.error("could not determine WiFi state.")
    return False


def get_signal() -> T.List[T.Dict[str, T.Any]]:

    ret = subprocess.run(NMCMD, timeout=1.0)
    if ret.returncode != 0:
        raise ConnectionError("could not connect with NetworkManager for WiFi")
    sleep(0.5)  # nmcli errored for less than about 0.2 sec.
    # takes several seconds to update, so do it now.
    ret = subprocess.run(NMSCAN, timeout=1.0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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

    # %% cleanup
    dat["ssid"] = dat["ssid"].str.replace("nan", "")
    dat["macAddress"] = dat["macAddress"].str.replace(r"\\:", ":")

    return dat
