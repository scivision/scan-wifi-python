#!/usr/bin/env python
import pytest
import mozloc
import datetime
import subprocess


def test_nm_loc():
    try:
        loc = mozloc.get_nmcli()
    except subprocess.CalledProcessError as e:
        pytest.xfail(f'problem with NMCLI API--old NMCLI version?  {e}')
    assert isinstance(loc, dict)
    assert isinstance(loc['t'], datetime.datetime)


def test_nm_connection():
    try:
        mozloc.nm_config_check()
    except subprocess.CalledProcessError as e:
        pytest.xfail(f'problem with NMCLI WiFi API--do you have WiFi?  {e}')


if __name__ == '__main__':
    pytest.main(['-xrsv', __file__])
