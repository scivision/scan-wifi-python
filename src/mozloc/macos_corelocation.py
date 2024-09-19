# /usr/bin/env python3
"""
MUST USE SYSTEM PYTHON /usr/bin/python3
DON'T USE sudo as LocationServices Python won't pop up.

TODO: even with all this, BSSID is still (null) / None

LocationServices Python app becomes available to enable in
Settings > Privacy > Location Services

pip install pyobjc

from https://forums.developer.apple.com/forums/thread/748161?answerId=782574022#782574022

Ref: https://docs.python.org/3/using/mac.html#gui-programming
"""

import CoreLocation
import time
import logging
import pandas

import objc


def config_check() -> bool:
    """
    Need authorization to get BSSID
    """

    mgr = CoreLocation.CLLocationManager.alloc().init()
    # mgr = CoreLocation.CLLocationManager.new()
    # mgr.requestAlwaysAuthorization()
    mgr.startUpdatingLocation()

    max_wait = 10
    # Get the current authorization status for Python
    # https://stackoverflow.com/a/75843844
    for i in range(1, max_wait):
        s = mgr.authorizationStatus()
        if s in {3, 4}:
            print("Python has been authorized for location services")
            return True
        if i == max_wait - 1:
            logging.error("Unable to obtain authorization")
            return False
        print(f"Waiting for authorization... do you see the Location Services popup window? {s}")
        time.sleep(0.5)

    return False


def get_signal(networks):
    # Get the current location

    dat: list[dict[str, str]] = []

    for network in networks:
        # print(f"{network.ssid()} {network.bssid()} {network.rssi()}  channel {network.channel()}")
        d = {"ssid": network.ssid(), "signalStrength": network.rssi()}
        if network.bssid() is not None:
            d["macAddress"] = network.bssid()
        dat.append(d)

    return pandas.DataFrame(dat)


def scan_signal():

    bundle_path = "/System/Library/Frameworks/CoreWLAN.framework"

    objc.loadBundle("CoreWLAN", bundle_path=bundle_path, module_globals=globals())

    # https://developer.apple.com/documentation/corewlan/cwinterface
    # iface = CWInterface.interface()  # not recommended, low-level
    # https://developer.apple.com/documentation/corewlan/cwwificlient
    iface = CoreLocation.CWWiFiClient.sharedWiFiClient().interface()

    logging.info(f"WiFi interface {iface.interfaceName()}")

    # need to run once to warmup -- otherwise all SSID are "(null)"
    iface.scanForNetworksWithName_includeHidden_error_(None, True, None)

    networks, error = iface.scanForNetworksWithName_includeHidden_error_(None, True, None)

    return networks
