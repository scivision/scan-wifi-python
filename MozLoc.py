#!/usr/bin/env python
"""
https://mozilla.github.io/ichnaea/api/geolocate.html
you should get your own Mozilla Location Services API key

Don't abuse the API or you'll get banned (excessive polling rate)

Uses ``nmcli`` from Linux only. Could be extended to other tools and OS.
"""
from mozloc import logwifiloc
from argparse import ArgumentParser


def main():
    """
    output: lat lon [deg] accuracy [m]
    """
    p = ArgumentParser()
    p.add_argument('logfile', help='logfile to append location to', nargs='?')
    p.add_argument('-T', '--cadence', help='how often to ping [sec]. Some laptops cannot go faster than 30 sec.',
                   default=60, type=float)
    p = p.parse_args()

    logwifiloc(p.cadence, p.logfile)


if __name__ == '__main__':
    main()
