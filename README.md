# mozilla-location-python
Uses nmcli on Linux in a short, simple Mozilla Location Services with Wifi from Python.
Goal was to be as simple as possible.
Works with Python &ge; 3.6.

## Install
```sh
python -m pip install -e .
```

### prereqs
Linux system with NetworkManager (e.g. Ubuntu, Raspberry Pi, etc.).



## Usage

    ./MozLoc.py

Returns `dict` containing `lat` `lng` `accuracy` `N BSSIDs heard`.
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
   sudo apt install network-manager
   sudo apt purge dhcpcd5
   ```
   reboot
2. upon reboot, try
   ```sh
   nmcli dev wifi list
   ```
   you should see several wifi access points and signal.
3. try the MLS geolocation program above.
