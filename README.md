# Mozilla Location Services from Python

![Actions Status](https://github.com/scivision/mozilla-location-wifi/workflows/ci/badge.svg)
[![Python versions (PyPI)](https://img.shields.io/pypi/pyversions/mozloc.svg)](https://pypi.python.org/pypi/mozloc)
[![PyPi Download stats](http://pepy.tech/badge/mozloc)](http://pepy.tech/project/mozloc)

Uses command line access to WiFi information in a short, simple Mozilla Location Services with Wifi from Python.
The command line programs used to access WiFi information include:

* Linux: `nmcli` [NetworkManager](https://developer.gnome.org/NetworkManager/stable/nmcli.html)
* Windows: [`netsh`](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc755301(v=ws.10)?redirectedfrom=MSDN)

Note that a similar service with better accuracy is available from
[Google](https://developers.google.com/maps/documentation/geolocation/intro).
Let us know if you're interested.

## Install


Get latest release

```sh
pip install mozloc
```

or for latest development version
```sh
git clone https://github.com/scivision/mozilla-location-wifi/
pip install -e mozilla-location-wifi/
```

## Usage

```sh
MozLoc
```

Shows `time` `lat` `lng` `accuracy` `N BSSIDs heard`.
In urban areas, accuracy of less than 100 meters is possible.

### dump raw signals

```sh
mozloc_signal
```

### Windows

On Windows, NetSH is used.
You may need to disconnect from WiFi (leave WiFi enabled) to make your WiFi chipset scan and be able to get location.

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

### Windows

To print verbose information about nearby WiFi:

```posh
netsh wlan show networks mode=bssid
```

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
