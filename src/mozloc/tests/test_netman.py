import pytest
import os
import pandas

is_ci = os.environ.get("CI", "").lower() == "true"


@pytest.mark.skipif(is_ci, reason="CI doesn't usually have WiFi")
def test_nm_loc():
    mozloc = pytest.importorskip("mozloc")
    loc = mozloc.parse_signal(mozloc.get_signal())

    assert isinstance(loc, pandas.DataFrame)
    assert -130 < int(loc["signalStrength"][0]) < 0, "impossible RSSI"


@pytest.mark.skipif(is_ci, reason="CI doesn't usually have WiFi")
def test_nm_connection():
    mozloc = pytest.importorskip("mozloc")
    assert mozloc.cli_config_check()
