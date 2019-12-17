# Mozilla Location Services from Python

[![Build Status](https://travis-ci.com/scivision/mozilla-location-wifi-python.svg?branch=master)](https://travis-ci.com/scivision/mozilla-location-wifi-python)
[![Python versions (PyPI)](https://img.shields.io/pypi/pyversions/mozilla-location-python.svg)](https://pypi.python.org/pypi/mozilla-location-python)
[![PyPi Download stats](http://pepy.tech/badge/mozilla-location-python)](http://pepy.tech/project/mozilla-location-python)

Uses command line access to WiFi information in a short, simple Mozilla Location Services with Wifi from Python.
The command line programs used to access WiFi inforamtion include:

* Linux: `nmcli` [NetworkManager](https://developer.gnome.org/NetworkManager/stable/nmcli.html)
* Windows: [`netsh`](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc755301(v=ws.10)?redirectedfrom=MSDN)

Note that a similar service with better accuracy is available from
[Google](https://developers.google.com/maps/documentation/geolocation/intro).
Let us know if you're interested.

## Install

```sh
python -m pip install -e .
```

## Usage

```sh
python MozLoc.py
```

Returns `dict()` containing `lat` `lng` `accuracy` `N BSSIDs heard`.
In urban areas, accuracy ~ 5 - 100 meters.

### convert to KML

Display logged data in Google Earth or other KML viewer after converting from CSV to KML:

```sh
python csv2kml.py in.log out.kml
```

which uses

```sh
pip install simplekml
```

Note that your time MUST be in ISO 8601 format or some KML reading programs such as Google Earth will just show a blank file.
E.g.

2016-07-24T12:34:56

## TODO

Would like to add Bluetooth beacons.

## Notes

* [Inspired by](https://github.com/flyinva/mozlosh)
* [Alternative using Skyhook and geoclue](https://github.com/scivision/python-geoclue)
* [Raspberry Pi NetworkManager](https://raspberrypi.stackexchange.com/a/73816)

### Raspberry Pi 3 / 4 / Zero W

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
