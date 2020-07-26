import pytest
import os

import mozloc

is_ci = os.environ.get("CI", "").lower() == "true"


@pytest.mark.skipif(is_ci, reason="CI doesn't usually have WiFi")
def test_nm_loc():

    loc = mozloc.get_cli()

    assert isinstance(loc, list)
    assert isinstance(loc[0], dict)
    assert -130 < int(loc[0]["signalStrength"]) < 0, "impossible RSSI"


def test_nm_connection():

    assert mozloc.cli_config_check()
