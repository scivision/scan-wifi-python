from __future__ import annotations
from time import sleep
from pathlib import Path
import logging
from pprint import pprint

from .modules import get_signal, parse_signal, cli_config_check
from .web import get_loc_mozilla

HEADER = "time                lat        lon         accuracy NumBSSIDs"


def process_file(file: Path, mozilla_url: str):
    """
    process raw data captured from NetSH etc. by user previously to a file
    """

    raw = Path(file).expanduser().read_text()
    dat = parse_signal(raw)
    pprint(dat)
    loc = get_loc_mozilla(dat, url=mozilla_url)

    stat = f'{loc["t"].isoformat(timespec="seconds")} {loc["lat"]} {loc["lng"]} {loc["accuracy"]:.1f} {loc["N"]:02d}'

    print(stat)


def log_wifi_loc(cadence_sec: float, mozilla_url: str, logfile: Path | None = None):
    if logfile:
        logfile = Path(logfile).expanduser()
        with logfile.open("a") as f:
            f.write(HEADER + "\n")

    print(f"updating every {cadence_sec} seconds")
    print(HEADER)

    if not cli_config_check():
        raise ConnectionError("Could not connect to WiFi hardware")
    # nmcli errored for less than about 0.2 sec.
    sleep(0.5)
    while True:
        raw = get_signal()
        dat = parse_signal(raw)
        if len(dat) < 2:
            logging.warning(f"cannot locate since at least 2 BSSIDs required\n{dat}")
            sleep(cadence_sec)
            continue

        loc = get_loc_mozilla(dat, mozilla_url)
        if loc is None:
            logging.warning(f"Did not get location from {len(dat)} BSSIDs")
            sleep(cadence_sec)
            continue

        stat = f'{loc["t"].isoformat(timespec="seconds")} {loc["lat"]} {loc["lng"]} {loc["accuracy"]:.1f} {loc["N"]:02d}'
        print(stat)

        if logfile:
            with logfile.open("a") as f:
                f.write(stat + "\n")

        sleep(cadence_sec)
