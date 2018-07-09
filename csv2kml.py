#!/usr/bin/env python
"""convert logged positions to KML"""
from mozloc import csv2kml
from argparse import ArgumentParser


def main():
    p = ArgumentParser()
    p.add_argument('logfn', help='csv logfile to read')
    p.add_argument('kmlfn', help='kml filename to write')
    p = p.parse_args()

    csv2kml(p.logfn, p.kmlfn)


if __name__ == '__main__':
    main()
