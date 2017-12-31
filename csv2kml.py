#!/usr/bin/env python
"""convert logged positions to KML"""
from mozloc import csv2kml

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('logfn',help='csv logfile to read')
    p.add_argument('kmlfn',help='kml filename to write')
    p = p.parse_args()


    csv2kml(p.logfn, p.kmlfn)
