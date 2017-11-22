# mozilla-location-python
Uses nmcli in a short, simple Mozilla Location Services with Wifi from Python. Extensible.

## prereqs

    pip install pandas requests

## Usage

    ./mozloc.py

Returns `dict` containing `lat` `lng` `accuracy`.
In urban areas, accuracy ~ 100 meters.

## Notes
[Inspired by](https://github.com/flyinva/mozlosh)

[Alternative using Skyhook and geoclue](https://github.com/scivision/python-geoclue)