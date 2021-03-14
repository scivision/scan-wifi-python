""" Windows NetSH functions """

from __future__ import annotations
import typing as T
import subprocess
import logging
import shutil
import io
from math import log10

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


def get_signal() -> list[dict[str, T.Any]]:
    """ get signal strength using CLI """
    ret = subprocess.run(CMD, timeout=1.0, stdout=subprocess.PIPE, text=True)
    if ret.returncode != 0:
        logging.error("consider slowing scan cadence.")

    dat: list[dict[str, str]] = []
    out = io.StringIO(ret.stdout)
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
                break

    return dat


def signal_percent_to_dbm(percent: int) -> int:
    """arbitrary conversion factor from Windows WiFi signal % to dBm
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
