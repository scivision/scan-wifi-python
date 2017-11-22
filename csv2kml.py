#!/usr/bin/env python
"""convert logged positions to KML"""
import numpy as np
from simplekml import Kml

def makekml(t, lonLatAlt, ofn):
    """
    write KML track/positions

    t: vector of times
    lonLatAlt: longitude, latitude, altitude or just lon,lat
    ofn: KML filename to create
    """
    lonLatAlt = np.asarray(lonLatAlt)
    assert lonLatAlt.ndim==2 and lonLatAlt.shape[1] in (2,3), 'Expect Nx2 or Nx3 array'

    kml = Kml(name='My Kml',open=1)

    if t is not None: # track over time
        trk = kml.newgxtrack(name='My Track')
        trk.newwhen(t)
        trk.newgxcoord(lonLatAlt.tolist()) #list of lon,lat,alt, NOT ndarray!
    else: # just a bunch of points
        for i,p in enumerate(lonLatAlt): # iterate over rows
            kml.newpoint(name=str(i), coords=[p])

    print('writing',ofn)
    kml.save(ofn)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('logfn',help='csv logfile to read')
    p.add_argument('kmlfn',help='kml filename to write')
    p = p.parse_args()

    dat = np.fliplr(np.loadtxt(p.logfn, usecols=(1,2)))

    makekml(None,dat,p.kmlfn)
