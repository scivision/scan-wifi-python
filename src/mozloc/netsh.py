""" Windows NetSH functions """

from __future__ import annotations
import typing as T
import subprocess
import logging
import io
import shutil

CLI = shutil.which("netsh")
if not CLI:
    raise ImportError('Could not find NetSH "netsh"')

CMD = [CLI, "wlan", "show", "networks", "mode=bssid"]


def cli_config_check() -> bool:
    # %% check that NetSH CLI is available and WiFi is active
    ret = subprocess.run(CMD, stdout=subprocess.PIPE, text=True, timeout=2)
    for line in ret.stdout.split("\n"):
        if "networks currently visible" in line:
            return True
        if "The wireless local area network interface is powered down and doesn't support the requested operation" in line:
            logging.error("must enable WiFi, it appears to be turned off.")
            return False

    logging.error("could not determine WiFi state.")
    return False


def get_signal() -> str:
    """
    get signal strength using CLI

    returns dict of data parsed from CLI
    """
    ret = subprocess.run(CMD, timeout=1.0, stdout=subprocess.PIPE, text=True)
    if ret.returncode != 0:
        logging.error("consider slowing scan cadence.")

    return ret.stdout


def parse_signal(raw: str) -> list[dict[str, T.Any]]:

    dat: list[dict[str, str]] = []
    out = io.StringIO(raw)

    for line in out:
        d: dict[str, str] = {}
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
                try:
                    signal_percent = int(line.split(":", 1)[1].split("%", 1)[0])
                except ValueError:
                    logging.error(line)
                    break
                d["signalStrength"] = str(signal_percent_to_dbm(signal_percent))
                d["ssid"] = ssid
                dat.append(d)
                d = {}
                # need break at each for level
                break
            break

    return dat


def signal_percent_to_dbm(percent: int) -> int:
    """
    arbitrary conversion factor from Windows WiFi signal % to dBm
    assumes signal percents map to dBm like:

    * 100% is -30 dBm
    * 0% is -100 dBm

    Parameters
    ----------
    percent: int
        signal strength as percent 0..100

    Returns
    -------
    meas_dBm: int
        truncate to nearest integer because of uncertainties
    """

    REF = -100  # dBm
    assert 0 <= percent <= 100, "percent must be 0...100"

    return int(REF + percent * 7 / 10)
