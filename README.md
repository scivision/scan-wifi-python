# RETIRED: Mozilla Location Services from Python

[![ci](https://github.com/scivision/mozilla-location-wifi/actions/workflows/ci.yml/badge.svg)](https://github.com/scivision/mozilla-location-wifi/actions/workflows/ci.yml)
[![PyPI Download stats](http://pepy.tech/badge/mozloc)](http://pepy.tech/project/mozloc)

This project is RETIRED due to
[discontinuation of Mozilla Location Services](https://discourse.mozilla.org/t/retiring-the-mozilla-location-service/128693).
It worked so well, sorry to see it go!

This project can nonetheless be used as a reference for accessing WiFi information from Python.

A future direction might be to use
[Google Geolocation API](https://developers.google.com/maps/documentation/geolocation/intro)

---

Uses command line access to WiFi information via
[Mozilla Location Services API](https://ichnaea.readthedocs.io/en/latest/api/geolocate.html?highlight=macaddress#wifi-access-point-fields)
from Python.
The command line programs used to access WiFi information include:

* Linux: [nmcli](https://developer.gnome.org/NetworkManager/stable/nmcli.html) NetworkManager
* MacOS: [CoreLocation.CWWiFiClient](https://developer.apple.com/documentation/corewlan/cwwificlient) or for macOS < 14.4 [airport](https://ss64.com/osx/airport.html)
* Windows: [netsh](https://learn.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh)

## Install

Get latest release

```sh
pip install mozloc
```

or for latest development version:

```sh
git clone https://github.com/scivision/mozilla-location-wifi/
pip install -e ./mozilla-location-wifi
```

## Usage

```sh
python -m mozloc
```

Shows `time` `lat` `lng` `accuracy` `N BSSIDs heard`.
In urban areas, accuracy of less than 100 meters is possible.

dump raw signals, without using API:

```sh
python -m mozloc --dump
```

### macOS

macOS &ge; 14.4 uses CoreLocation.CWWiFiClient as "airport" was removed.

### Windows

On Windows, NetSH is used.
You may need to disconnect from WiFi (leave WiFi enabled) to make your WiFi chipset scan and be able to get location.

## convert to KML

Display logged data in Google Earth or other KML viewer after converting from CSV to KML:

```sh
python -m mozloc.csv2kml in.log out.kml
```

which uses

```sh
pip install simplekml
```

Note that your time MUST be in ISO 8601 format or some KML reading programs such as Google Earth will just show a blank file.
E.g.

2016-07-24T12:34:56

## TODO

Would like to add Bluetooth beacons. Need to use a new location service.

## Notes

* [Inspired by](https://github.com/flyinva/mozlosh)
* [Alternative using Skyhook and geoclue](https://github.com/scivision/python-geoclue)
* [Raspberry Pi NetworkManager](https://raspberrypi.stackexchange.com/a/73816)

To print verbose information about nearby WiFi:

* Windows: `netsh wlan show networks mode=bssid`
* MacOS: `airport -s`
* Linux: `nmcli dev wifi list`
