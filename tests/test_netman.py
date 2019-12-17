#!/usr/bin/env python
import pytest
import datetime
import subprocess


def test_nm_loc():
    mozloc = pytest.importorskip("mozloc")

    try:
        loc = mozloc.get_cli()
    except subprocess.CalledProcessError as e:
        pytest.skip(f"problem with NMCLI API--old NMCLI version?  {e}")

    if loc is None:
        pytest.skip("need at least 2 WiFi AP")

    assert isinstance(loc, dict)
    assert isinstance(loc["t"], datetime.datetime)


def test_nm_connection():
    mozloc = pytest.importorskip("mozloc")

    try:
        mozloc.cli_config_check()
    except subprocess.CalledProcessError as e:
        pytest.skip(f"problem with CLI WiFi API--do you have WiFi?  {e}")


if __name__ == "__main__":
    pytest.main([__file__])
