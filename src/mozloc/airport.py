""" MacOS airport functions

Airport was removed from macOS 14.4+, so these functions no longer are relevant.
"""

from __future__ import annotations
import typing as T
import logging
import subprocess
import re

from .cmd import get_airport, running_as_root


def cli_config_check() -> bool:
    # %% check that Airport is available and WiFi is active

    try:
        ret = subprocess.check_output([get_airport(), "--getinfo"], text=True, timeout=30)
    except subprocess.CalledProcessError as err:
        logging.error(err)
        return False

    stdout = ret.strip().lower()
    if len(stdout) == "airport: off":
        return False

    if "state: running" in stdout:
        return True

    logging.error("could not determine WiFi state.")
    return False


def get_signal() -> str:
    try:
        ret = subprocess.check_output([get_airport(), "--scan"], text=True, timeout=30)
    except subprocess.CalledProcessError as err:
        logging.error(f"consider slowing scan cadence. {err}")

    return ret


def parse_signal(raw: str) -> list[dict[str, T.Any]]:
    isroot = running_as_root()

    psudo = r"\s*([0-9a-zA-Z\s\-\.]+)\s+([0-9a-f]{2}(?::[0-9a-f]{2}){5})\s+(-\d{2,3})"
    # BSSID only present if sudo
    puser = r"\s*([0-9a-zA-Z\s\-\.]+)\s+(-\d{2,3})"
    # non-sudo has no BSSID

    p = psudo if isroot else puser
    isig = 3 if isroot else 2
    ibssid = 2
    pat = re.compile(p)
    dat: list[dict[str, str]] = []

    for line in raw.split("\n"):
        mat = pat.match(line)
        if mat:
            # Hidden SSID optout implicitly excluded by regex
            ssid = mat.group(1).strip()
            # optout
            if ssid.endswith("_nomap"):
                continue
            d = {"ssid": ssid, "signalStrength": mat.group(isig)}
            if isroot:
                d["macAddress"] = mat.group(ibssid)
            dat.append(d)

    return dat
