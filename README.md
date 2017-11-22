# mozilla-location-python
Uses nmcli on Linux in a short, simple Mozilla Location Services with Wifi from Python.
Goal was to be as simple as possible.
Works with Python 2.7 and 3.

## prereqs
Linux system with NetworkManager (e.g. Ubuntu, Raspberry Pi, etc.).

    pip install pandas requests


## Usage

    ./mozloc.py

Returns `dict` containing `lat` `lng` `accuracy`.
In urban areas, accuracy ~ 100 meters.


### convert to KML
You can display your logged data in Google Earth or other KML value after converting by

    ./csv2kml.py in.log out.kml
    
with
    
    pip install simplekml
    

## Contributing
Pull request if you have another favorite approach.
Would like to add Bluetooth, should be simple.


## Notes

* [Inspired by](https://github.com/flyinva/mozlosh)
* [Alternative using Skyhook and geoclue](https://github.com/scivision/python-geoclue)
