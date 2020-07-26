import pytest
import importlib.resources


def test_kml():
    simplekml = pytest.importorskip("simplekml")
    # Data for the track
    when = [
        "2010-05-28T02:02:09Z",
        "2010-05-28T02:02:35Z",
        "2010-05-28T02:02:44Z",
        "2010-05-28T02:02:53Z",
        "2010-05-28T02:02:54Z",
        "2010-05-28T02:02:55Z",
        "2010-05-28T02:02:56Z",
    ]

    coord = [
        (-122.207881, 37.371915, 156.000000),
        (-122.205712, 37.373288, 152.000000),
        (-122.204678, 37.373939, 147.000000),
        (-122.203572, 37.374630, 142.199997),
        (-122.203451, 37.374706, 141.800003),
        (-122.203329, 37.374780, 141.199997),
        (-122.203207, 37.374857, 140.199997),
    ]

    kml = simplekml.Kml(name="Tracks",)
    trk = kml.newgxtrack(name="test")

    trk.newwhen(when)
    trk.newgxcoord(coord)

    with importlib.resources.path("mozloc.tests", "Test.kml") as file:
        kml.save(file)
