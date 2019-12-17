#!/usr/bin/env python
import pytest
import datetime
import subprocess


def test_nm_loc():
    mozloc = pytest.importorskip("mozloc")

    try:
        loc = mozloc.netman.get_nmcli()
    except subprocess.CalledProcessError as e:
        pytest.skip(f"problem with NMCLI API--old NMCLI version?  {e}")

    assert isinstance(loc, dict)
    assert isinstance(loc["t"], datetime.datetime)


def test_nm_connection():
    mozloc = pytest.importorskip("mozloc")

    try:
        mozloc.netman.nm_config_check()
    except subprocess.CalledProcessError as e:
        pytest.skip(f"problem with NMCLI WiFi API--do you have WiFi?  {e}")


if __name__ == "__main__":
    pytest.main([__file__])
