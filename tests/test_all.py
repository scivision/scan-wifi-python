#!/usr/bin/env python
import pytest
import mozloc
import datetime
import os

CI = bool(os.environ['CI']) if 'CI' in os.environ else False


@pytest.mark.skipif(CI, reason="CI doesn't have WiFi")
def test_nm_loc():
    loc = mozloc.get_nmcli()
    assert isinstance(loc, dict)
    assert isinstance(loc['t'], datetime.datetime)


@pytest.mark.skipif(CI, reason="CI doesn't have WiFi")
def test_nm_connection():
    mozloc.nm_config_check()


if __name__ == '__main__':
    pytest.main(['-xrsv', __file__])
