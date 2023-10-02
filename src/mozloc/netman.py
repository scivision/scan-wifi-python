""" Network Manager CLI (nmcli) functions """

from __future__ import annotations
import typing as T
import subprocess
import logging
import pandas
import io
from time import sleep

from .cmd import get_nmcli


def cli_config_check() -> bool:
    # %% check that NetworkManager CLI is available and WiFi is active

    try:
        ret = subprocess.check_output([get_nmcli(), "-t", "radio", "wifi"], text=True, timeout=2)
    except subprocess.CalledProcessError as err:
        logging.error(err)
        return False

    stdout = ret.strip().split(":")
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
    cmd = [get_nmcli(), "-g", "SSID,BSSID,FREQ,SIGNAL", "device", "wifi"]
    # Debian stretch, Ubuntu 18.04
    # cmd = [EXE, "-t", "-f", "SSID,BSSID,FREQ,SIGNAL", "device", "wifi"]
    # ubuntu 16.04

    try:
        subprocess.check_call(cmd, timeout=1.0)
    except subprocess.CalledProcessError as err:
        raise ConnectionError(f"could not connect with NetworkManager for WiFi   {err}")

    sleep(0.5)  # nmcli errored for less than about 0.2 sec.
    # takes several seconds to update, so do it now.

    scan = [get_nmcli(), "device", "wifi", "rescan"]

    try:
        ret = subprocess.check_output(scan, timeout=1.0, text=True)
    except subprocess.CalledProcessError as err:
        logging.error(f"consider slowing scan cadence. {err}")

    return ret


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
