import pytest
import os
import pandas
import mozloc

is_ci = os.environ.get("CI", "").lower() == "true"


@pytest.mark.skipif(is_ci, reason="CI doesn't usually have WiFi")
def test_signal():
    if not mozloc.config_check():
        pytest.skip("WiFi not available")

    loc = mozloc.get_signal(mozloc.scan_signal())

    assert isinstance(loc, pandas.DataFrame)
    assert -130 < int(loc["signalStrength"][0]) < 0, "impossible RSSI"
