# /usr/bin/env python3
"""
MUST USE SYSTEM PYTHON /usr/bin/python3
DON'T USE sudo as LocationServices Python won't pop up.

TODO: even with all this, BSSID is still (null) / None

LocationServices Python app becomes available to enable in
Settings > Privacy > Location Services

pip install pyobjc

from https://forums.developer.apple.com/forums/thread/748161?answerId=782574022#782574022
"""

import objc
import CoreLocation
from time import sleep

# Need authorization to get BSSID

mgr = CoreLocation.CLLocationManager.alloc().init()
# mgr = CoreLocation.CLLocationManager.new()
# mgr.requestAlwaysAuthorization()
mgr.startUpdatingLocation()

max_wait = 10
# Get the current authorization status for Python
for i in range(1, max_wait):
    s = mgr.authorizationStatus()
    if s in {3, 4}:
        print("Python has been authorized for location services")
        break
    if i == max_wait - 1:
        raise SystemExit("Unable to obtain authorization, exiting")
    print(f"Waiting for authorization... do you see the Location Services popup window? {s}")
    sleep(0.5)

# Get the current location

bundle_path = "/System/Library/Frameworks/CoreWLAN.framework"

objc.loadBundle("CoreWLAN", bundle_path=bundle_path, module_globals=globals())

# https://developer.apple.com/documentation/corewlan/cwinterface
# iface = CWInterface.interface()  # not recommended, low-level
# https://developer.apple.com/documentation/corewlan/cwwificlient
iface = CoreLocation.CWWiFiClient.sharedWiFiClient().interface()

print(f"WiFi interface {iface.interfaceName()}")


# need to run once to warmup -- otherwise all SSID are "(null)"
iface.scanForNetworksWithName_includeHidden_error_(None, True, None)

networks, error = iface.scanForNetworksWithName_includeHidden_error_(None, True, None)

for network in networks:
    print(f"{network.ssid()} {network.bssid()} {network.rssi()}  channel {network.channel()}")
