#!/usr/bin/env python
"""
https://mozilla.github.io/ichnaea/api/geolocate.html
you should get your own Mozilla Location Services API key

Don't abuse the API or you'll get banned (excessive polling rate)

Uses ``nmcli`` from Linux only. Could be extended to other tools and OS.
"""
import subprocess
import logging
from io import BytesIO
import pandas
import requests
from datetime import datetime
from time import sleep

URL='https://location.services.mozilla.com/v1/geolocate?key=test'
NMCMD = ['nmcli','-g','SSID,BSSID,FREQ,SIGNAL','device','wifi'] # Debian stretch, Ubuntu 17.10
NMLEG = ['nmcli','-t','-f','SSID,BSSID,FREQ,SIGNAL','device','wifi'] # ubuntu 16.04
NMSCAN = ['nmcli','device','wifi','rescan']


def get_nmcli():


    ret = subprocess.check_output(NMLEG)
    sleep(0.5) # nmcli crashed for less than about 0.2 sec.
    try:
        subprocess.check_call(NMSCAN) # takes several seconds to update, so do it now.
    except subprocess.CalledProcessError as e:
        print('consider slowing scan cadence.  {}'.format(e))

    dat = pandas.read_csv(BytesIO(ret), sep=r'(?<!\\):', index_col=False,
                          header=0, encoding='utf8',engine='python',
                          dtype=str,usecols=[0,1,3],
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
        logging.error('no network connection.  {}'.format(e))
        return
# %% process MLS response
    jres = req.json()
    loc = jres['location']
    loc['accuracy'] = jres['accuracy']
    loc['N'] = dat.shape[0] # number of BSSIDs used
    loc['t'] = datetime.now()

    return loc


if __name__ == '__main__':
    """
    output: lat lon [deg] accuracy [m]
    """
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('logfile',help='logfile to append location to',nargs='?')
    p.add_argument('-T','--cadence',help='how often to ping [sec]. Some laptops cannot go faster than 30 sec.',
                    default=60,type=float)
    p = p.parse_args()

    T = p.cadence

    logfile = p.logfile

    print('updating every {} seconds'.format(T))
    while True:
        loc = get_nmcli()
        if loc is None:
            sleep(p.T)
            continue

        stat = '{} {} {} {} {}'.format(loc['t'].strftime('%xT%X'),
                            loc['lat'], loc['lng'], loc['accuracy'], loc['N'])
        print(stat)

        if logfile:
            with open(logfile,'a') as f:
                f.write(stat+'\n')

        sleep(T)
