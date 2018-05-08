[![Python versions (PyPI)](https://img.shields.io/pypi/pyversions/mozilla-location-python.svg)](https://pypi.python.org/pypi/mozilla-location-python)

[![Distribution format (PyPI)](https://img.shields.io/pypi/format/mozilla-location-python.svg)](https://pypi.python.org/pypi/mozilla-location-python)

# mozilla-location-python
Uses nmcli on Linux in a short, simple Mozilla Location Services with Wifi from Python.
Goal was to be as simple as possible.

Note that a similar service with better accuracy is available from [Google](https://developers.google.com/maps/documentation/geolocation/intro).
Let us know if you're interested.

## Install
```sh
python -m pip install -e .
```

### prereqs
Linux system with NetworkManager (e.g. Ubuntu, Raspberry Pi, etc.).



## Usage
```sh
./MozLoc.py
```

Returns `dict()` containing `lat` `lng` `accuracy` `N BSSIDs heard`.
In urban areas, accuracy ~ 5 - 100 meters.


### convert to KML
You can display your logged data in Google Earth or other KML value after converting by

    ./csv2kml.py in.log out.kml

with

    pip install simplekml
    
Note that your time MUST be in ISO 8601 format or some KML reading programs such as Google Earth will just show a blank file.
E.g.

2016-07-24T12:34:56


## Contributing
Pull request if you have another favorite approach.
Would like to add Bluetooth, should be simple.


## Notes

* [Inspired by](https://github.com/flyinva/mozlosh)
* [Alternative using Skyhook and geoclue](https://github.com/scivision/python-geoclue)
* [Raspberry Pi NetworkManager](https://raspberrypi.stackexchange.com/a/73816)

### Raspberry Pi 3
Debian comes without NetworkManager by default.
Be careful as you lose Wifi password etc. by this procedure

1. Install network manager and remove the old
   ```sh
   apt install network-manager
   apt purge dhcpcd5
   ```
   reboot
2. upon reboot, try
   ```sh
   nmcli dev wifi list
   ```
   you should see several wifi access points and signal.
3. try the MLS geolocation program above.
