import pytest
import os

is_ci = os.environ.get("CI", "").lower() == "true"


@pytest.mark.skipif(is_ci, reason="CI doesn't usually have WiFi")
def test_nm_loc():

    mozloc = pytest.importorskip('mozloc')
    loc = mozloc.get_signal()

    assert isinstance(loc, list)
    assert isinstance(loc[0], dict)
    assert -130 < int(loc[0]["signalStrength"]) < 0, "impossible RSSI"


@pytest.mark.skipif(is_ci, reason="CI doesn't usually have WiFi")
def test_nm_connection():

    mozloc = pytest.importorskip('mozloc')
    assert mozloc.cli_config_check()
