"""convert logged positions to KML"""

import argparse

from ..utils import csv2kml

p = argparse.ArgumentParser()
p.add_argument("logfn", help="csv logfile to read")
p.add_argument("kmlfn", help="kml filename to write")
args = p.parse_args()

csv2kml(args.logfn, args.kmlfn)
