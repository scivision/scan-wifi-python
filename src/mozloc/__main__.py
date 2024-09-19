"""
https://mozilla.github.io/ichnaea/api/geolocate.html
https://ichnaea.readthedocs.io/en/latest/api/geolocate.html

you should get your own Mozilla Location Services API key

Don't abuse the API or you'll get banned (excessive polling rate)
"""

import argparse
from pprint import pprint

from .base import log_wifi_loc, process_file
from .modules import scan_signal, get_signal


p = argparse.ArgumentParser()
p.add_argument("logfile", help="logfile to append location to", nargs="?")
p.add_argument(
    "-T",
    "--cadence",
    help="how often to update [sec]. Some laptops cannot go faster than 30 sec.",
    default=60,
    type=float,
)
p.add_argument(
    "-url",
    help="Mozilla location services URL--don't use this default test key",
    default="https://location.services.mozilla.com/v1/geolocate?key=test",
)
p.add_argument(
    "-d", "--dump", help="print raw data to console without logging", action="store_true"
)
p.add_argument("-i", "--infile", help="use raw text saved from command line")
args = p.parse_args()

if args.dump:
    pprint(get_signal(scan_signal()))
elif args.infile:
    process_file(args.infile, mozilla_url=args.url)
else:
    log_wifi_loc(cadence_sec=args.cadence, mozilla_url=args.url, logfile=args.logfile)
