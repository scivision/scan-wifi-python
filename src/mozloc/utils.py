from simplekml import Kml
from pathlib import Path
import pandas


def csv2kml(csvfn: Path, kmlfn: Path):
    """
    convert csv to mkl

    Parameters
    ----------

    csvfn: pathlib.Path
      CSV filename to read
    kmlfn: pathlib.Path
       KML filename to write
    """

    # lon, lat
    dat = pandas.read_csv(csvfn, sep=" ", index_col=0, header=0)

    t = dat.index.tolist()
    lla = dat.loc[:, ["lon", "lat"]].values
    # %% write KML
    """
    http://simplekml.readthedocs.io/en/latest/geometries.html#gxtrack
    https://simplekml.readthedocs.io/en/latest/kml.html#id1
    https://simplekml.readthedocs.io/en/latest/geometries.html#simplekml.GxTrack
    """
    kml = Kml(name="My Kml")
    trk = kml.newgxtrack(name="My Track")
    trk.newwhen(t)  # list of times. MUST be format 2010-05-28T02:02:09Z
    trk.newgxcoord(lla.tolist())  # list of lon,lat,alt, NOT ndarray!

    # just a bunch of points
    #        for i,p in enumerate(lla): # iterate over rows
    #            kml.newpoint(name=str(i), coords=[p])

    print("writing", kmlfn)
    kml.save(kmlfn)
