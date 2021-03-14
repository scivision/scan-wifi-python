""" MacOS airport functions """

from __future__ import annotations
import typing as T
import shutil
import io
import logging
import subprocess
import re

EXE = shutil.which("airport", path="/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources")
if not EXE:
    raise ImportError("Could not find Airport")


def cli_config_check() -> bool:
    # %% check that Airport is available and WiFi is active
    ret = subprocess.run([EXE, "--getinfo"], stdout=subprocess.PIPE, text=True, timeout=30)

    if ret.returncode != 0:
        return False

    stdout = ret.stdout.strip().lower()
    if len(stdout) == "airport: off":
        return False

    if "state: running" in stdout:
        return True

    logging.error("could not determine WiFi state.")
    return False


def get_signal() -> list[dict[str, T.Any]]:

    ret = subprocess.run([EXE, "-s"], timeout=30.0, stdout=subprocess.PIPE, text=True)

    if ret.returncode != 0:
        logging.error("consider slowing scan cadence.")

    pat = re.compile(r"\s*([0-9a-zA-Z\-\.]+)\s+([0-9a-f]{2}(?::[0-9a-f]{2}){5})\s+(-\d{2,3})")
    dat: list[dict[str, str]] = []

    for line in io.StringIO(ret.stdout):
        mat = pat.match(line)
        if mat:
            ssid = mat.group(1)
            # optout
            if ssid.endswith("_nomap"):
                continue

            dat.append({"ssid": ssid, "macAddress": mat.group(2), "signalStrength": mat.group(3)})

    return dat
