# Mozilla Location Services from Python

[![ci](https://github.com/scivision/mozilla-location-wifi/actions/workflows/ci.yml/badge.svg)](https://github.com/scivision/mozilla-location-wifi/actions/workflows/ci.yml)
[![PyPi Download stats](http://pepy.tech/badge/mozloc)](http://pepy.tech/project/mozloc)

Uses command line access to WiFi information in a short, simple Mozilla Location Services with Wifi from Python.
The command line programs used to access WiFi information include:

* Linux: `nmcli` [NetworkManager](https://developer.gnome.org/NetworkManager/stable/nmcli.html)
* MacOS: `airport` built into MacOS
* Windows: [`netsh`](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc755301(v=ws.10)?redirectedfrom=MSDN)

Note that a similar service with better accuracy is available from
[Google](https://developers.google.com/maps/documentation/geolocation/intro).
Let us know if you're interested.

## Install

Get latest release

```sh
pip install mozloc
```

or for latest development version:

```sh
git clone https://github.com/scivision/mozilla-location-wifi/
pip install -e mozilla-location-wifi/
```

## Usage

```sh
python -m mozloc
```

Shows `time` `lat` `lng` `accuracy` `N BSSIDs heard`.
In urban areas, accuracy of less than 100 meters is possible.

### dump raw signals

```sh
python -m mozloc.signal
```

### Windows

On Windows, NetSH is used.
You may need to disconnect from WiFi (leave WiFi enabled) to make your WiFi chipset scan and be able to get location.

### convert to KML

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

### Raspberry Pi 3 / 4 / Zero W

Debian comes without NetworkManager by default.
Thus we recommend using Ubuntu or similar on the Raspberry Pi with this program.

If you do use Debian with the procedure below, you lose Wifi password and stored WiFi networks.

1. Install network manager and remove the old
   ```sh
   apt install network-manager
   apt purge dhcpcd5
   ```
2. Reboot and try
   ```sh
   nmcli dev wifi list
   ```
   you should see several wifi access points and signal.
3. try the MLS geolocation program above.
