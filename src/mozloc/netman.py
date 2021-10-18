""" Network Manager CLI (nmcli) functions """

from __future__ import annotations
import typing as T
import subprocess
import logging
import shutil
import pandas
import io
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


def get_signal() -> str:

    ret = subprocess.run(NMCMD, timeout=1.0)
    if ret.returncode != 0:
        raise ConnectionError("could not connect with NetworkManager for WiFi")
    sleep(0.5)  # nmcli errored for less than about 0.2 sec.
    # takes several seconds to update, so do it now.
    ret = subprocess.run(NMSCAN, timeout=1.0, stdout=subprocess.PIPE, text=True)
    if ret.returncode != 0:
        logging.error("consider slowing scan cadence.")

    return ret.stdout


def parse_signal(raw: str) -> list[dict[str, T.Any]]:

    dat = pandas.read_csv(
        io.StringIO(raw),
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
