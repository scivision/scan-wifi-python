# /usr/bin/env python3
"""
pip install pyobjc

from https://forums.developer.apple.com/forums/thread/748161?answerId=782574022#782574022
"""

import objc
import CoreLocation

location_manager = CoreLocation.CLLocationManager.alloc().init()
location_manager.requestWhenInUseAuthorization()


bundle_path = "/System/Library/Frameworks/CoreWLAN.framework"

objc.loadBundle("CoreWLAN", bundle_path=bundle_path, module_globals=globals())

# https://developer.apple.com/documentation/corewlan/cwinterface
iface = CoreLocation.CWInterface.interface()

print(iface.interfaceName())
print(iface.ssid())

networks, error = iface.scanForNetworksWithSSID_error_(None, None)

for network in networks:
    print(network.ssid())
