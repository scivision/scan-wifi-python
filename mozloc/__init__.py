import subprocess
import logging
from io import StringIO
import pandas
import requests
from datetime import datetime
from time import sleep
from pathlib import Path
#
URL='https://location.services.mozilla.com/v1/geolocate?key=test'
NMCMD = ['nmcli','-g','SSID,BSSID,FREQ,SIGNAL','device','wifi'] # Debian stretch, Ubuntu 17.10
NMLEG = ['nmcli','-t','-f','SSID,BSSID,FREQ,SIGNAL','device','wifi'] # ubuntu 16.04
NMSCAN = ['nmcli','device','wifi','rescan']
HEADER='time lat lon accuracy NumBSSIDs'

# %%
def logwifiloc(T:float, logfile:Path):

    if logfile:
        logfile = Path(logfile).expanduser()
        with logfile.open('a') as f:
            f.write(HEADER+'\n')


    print(f'updating every {T} seconds')
    print(HEADER)
    while True:
        loc = get_nmcli()
        if loc is None:
            sleep(T)
            continue

        stat = f'{loc["t"].isoformat(timespec="seconds")} {loc["lat"]} {loc["lng"]} {loc["accuracy"]:.1f} {loc["N"]:02d}'
        print(stat)

        if logfile:
            with logfile.open('a') as f:
                f.write(stat+'\n')

        sleep(T)

# %%
def get_nmcli():


    ret = subprocess.check_output(NMLEG, universal_newlines=True, timeout=1.)
    sleep(0.5) # nmcli crashed for less than about 0.2 sec.
    try:
        subprocess.check_call(NMSCAN, timeout=1.) # takes several seconds to update, so do it now.
    except subprocess.CalledProcessError as e:
        logging.error(f'consider slowing scan cadence.  {e}')

    dat = pandas.read_csv(StringIO(ret), sep=r'(?<!\\):', index_col=False,
                          header=0, encoding='utf8', engine='python',
                          dtype=str, usecols=[0,1,3],
                          names=['ssid','macAddress','signalStrength'])
# %% optout
    dat = dat[~dat['ssid'].str.endswith('_nomap')]
# %% cleanup
    dat['ssid'] = dat['ssid'].str.replace('nan','')
    dat['macAddress'] = dat['macAddress'].str.replace(r'\\:',':')
# %% JSON
    jdat = dat.to_json(orient='records')
    jdat = '{ "wifiAccessPoints":' + jdat + '}'
#    print(jdat)
# %% cloud MLS
    try:
        req = requests.post(URL, data=jdat)
        if req.status_code != 200:
            logging.error(req.text)
            return
    except requests.exceptions.ConnectionError as e:
        logging.error(f'no network connection.  {e}')
        return
# %% process MLS response
    jres = req.json()
    loc = jres['location']
    loc['accuracy'] = jres['accuracy']
    loc['N'] = dat.shape[0] # number of BSSIDs used
    loc['t'] = datetime.now()

    return loc
# %%

def csv2kml(csvfn:Path, kmlfn:Path):
    from simplekml import Kml

    """
    write KML track/positions

    t: vector of times
    lonLatAlt: longitude, latitude, altitude or just lon,lat
    ofn: KML filename to create
    """

    # lon, lat
    dat = pandas.read_csv(csvfn, sep=' ', index_col=0, header=0)

    t = dat.index.tolist()
    lla = dat.loc[:,['lon','lat']].values
# %% write KML
    """
    http://simplekml.readthedocs.io/en/latest/geometries.html#gxtrack
    https://simplekml.readthedocs.io/en/latest/kml.html#id1
    https://simplekml.readthedocs.io/en/latest/geometries.html#simplekml.GxTrack
    """
    kml = Kml(name='My Kml')
    trk = kml.newgxtrack(name='My Track')
    trk.newwhen(t)  # list of times. MUST be format 2010-05-28T02:02:09Z
    trk.newgxcoord(lla.tolist()) #list of lon,lat,alt, NOT ndarray!

# just a bunch of points
#        for i,p in enumerate(lla): # iterate over rows
#            kml.newpoint(name=str(i), coords=[p])

    print('writing', kmlfn)
    kml.save(kmlfn)
