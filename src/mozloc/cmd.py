from __future__ import annotations

import functools
import shutil


@functools.cache
def get_exe(name: str, path: str | None = None) -> str:
    if not (exe := shutil.which(name, path=path)):
        raise ImportError(f"{name} not found")
    return exe


def get_airport() -> str:
    return get_exe(
        "airport",
        "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources",
    )


def get_nmcli() -> str:
    return get_exe("nmcli")


def get_netsh() -> str:
    return get_exe("netsh")
