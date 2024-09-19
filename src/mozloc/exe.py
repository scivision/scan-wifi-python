from __future__ import annotations
import os
import functools
import shutil
import subprocess


def running_as_root() -> bool:
    return os.getuid() == 0


@functools.cache
def get_exe(name: str, path: str | None = None) -> str:
    if not (exe := shutil.which(name, path=path)):
        raise FileNotFoundError(name)
    return exe


def get_airport() -> str:
    exe = get_exe(
        "airport",
        "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources",
    )

    msg = subprocess.check_output(exe, text=True, timeout=10)
    if "WARNING: The airport command line tool is deprecated" in msg:
        raise EnvironmentError(msg)

    return exe
