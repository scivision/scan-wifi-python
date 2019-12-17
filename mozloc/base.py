from time import sleep
from pathlib import Path

from .netman import nm_config_check, get_nmcli

HEADER = "time lat lon accuracy NumBSSIDs"


def log_wifi_loc(T: float, logfile: Path):

    if logfile:
        logfile = Path(logfile).expanduser()
        with logfile.open("a") as f:
            f.write(HEADER + "\n")

    print(f"updating every {T} seconds")
    print(HEADER)

    nm_config_check()
    sleep(0.5)  # nmcli errored for less than about 0.2 sec.
    while True:
        loc = get_nmcli()
        if loc is None:
            sleep(T)
            continue

        stat = f'{loc["t"].isoformat(timespec="seconds")} {loc["lat"]} {loc["lng"]} {loc["accuracy"]:.1f} {loc["N"]:02d}'
        print(stat)

        if logfile:
            with logfile.open("a") as f:
                f.write(stat + "\n")

        sleep(T)
