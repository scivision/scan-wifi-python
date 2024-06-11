# Mozilla Location Services from Python

[![ci](https://github.com/scivision/mozilla-location-wifi/actions/workflows/ci.yml/badge.svg)](https://github.com/scivision/mozilla-location-wifi/actions/workflows/ci.yml)
[![PyPi Download stats](http://pepy.tech/badge/mozloc)](http://pepy.tech/project/mozloc)

Uses command line access to WiFi information via
[Mozilla Location Services API](https://ichnaea.readthedocs.io/en/latest/api/geolocate.html?highlight=macaddress#wifi-access-point-fields)
from Python.
The command line programs used to access WiFi information include:

* Linux: [nmcli](https://developer.gnome.org/NetworkManager/stable/nmcli.html) NetworkManager
* MacOS: [airport](https://ss64.com/osx/airport.html) built into MacOS
* Windows: [netsh](https://learn.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh)

Note that a similar service with better accuracy is available from
[Google](https://developers.google.com/maps/documentation/geolocation/intro).

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

Note: macOS 14.4+ no longer works as "airport" has been removed.
If someone has time to implement, perhaps starting with example
[CoreLocation](./macos_corelocation.py)
code, we would welcome a PR.

On macOS, much more accurate results come by running as root by using sudo.
This is because "airport" only emits BSSID if running with sudo.

Possible future implementation could use
[CoreWLAN](https://developer.apple.com/documentation/corewlan/).

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

Would like to add Bluetooth beacons.

## Notes

* [Inspired by](https://github.com/flyinva/mozlosh)
* [Alternative using Skyhook and geoclue](https://github.com/scivision/python-geoclue)
* [Raspberry Pi NetworkManager](https://raspberrypi.stackexchange.com/a/73816)

To print verbose information about nearby WiFi:

* Windows: `netsh wlan show networks mode=bssid`
* MacOS: `airport -s`
* Linux: `nmcli dev wifi list`
