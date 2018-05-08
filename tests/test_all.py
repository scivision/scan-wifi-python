#!/usr/bin/env python
from numpy.testing import run_module_suite
import mozloc
import datetime

def test_nm_connection():
    loc = mozloc.get_nmcli()
    assert isinstance(loc,dict)
    assert isinstance(loc['t'],datetime.datetime)

def test_nm_loc():
    mozloc.nm_config_check()


def gen_kml():
    from simplekml import Kml
    # Data for the track
    when = ["2010-05-28T02:02:09Z",
        "2010-05-28T02:02:35Z",
        "2010-05-28T02:02:44Z",
        "2010-05-28T02:02:53Z",
        "2010-05-28T02:02:54Z",
        "2010-05-28T02:02:55Z",
        "2010-05-28T02:02:56Z"]

    coord = [(-122.207881,37.371915,156.000000),
        (-122.205712,37.373288,152.000000),
        (-122.204678,37.373939,147.000000),
        (-122.203572,37.374630,142.199997),
        (-122.203451,37.374706,141.800003),
        (-122.203329,37.374780,141.199997),
        (-122.203207,37.374857,140.199997)]


    kml = Kml(name="Tracks",)
    trk = kml.newgxtrack(name='test')

    trk.newwhen(when)
    trk.newgxcoord(coord)

    kml.save('Test.kml')


if __name__ == '__main__':
    run_module_suite()