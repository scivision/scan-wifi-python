#!/usr/bin/env python
"""
https://mozilla.github.io/ichnaea/api/geolocate.html
you should get your own Mozilla Location Services API key

Don't abuse the API or you'll get banned (excessive polling rate)

Uses ``nmcli`` from Linux only. Could be extended to other tools and OS.
"""
import subprocess
from io import BytesIO
import pandas
import requests
from datetime import datetime
from time import sleep

URL='https://location.services.mozilla.com/v1/geolocate?key=test'

def get_nmcli():

    cmd =['nmcli','-fields','BSSID,FREQ,SIGNAL','device','wifi']
    ret = subprocess.check_output(cmd)

    dat = pandas.read_csv(BytesIO(ret), sep='\s+', index_col=False,
                          header=0,usecols=[0,1,3],
                          names=['macAddress','frequency','signalStrength'])
    jdat = dat.to_json(orient='records')
    jdat = '{ "wifiAccessPoints":' + jdat + '}'
#    print(jdat)
    req = requests.post(URL, data=jdat)
    if req.status_code != 200:
        raise RuntimeError(ret.text)

    return req.json()

if __name__ == '__main__':
    """
    output: lat lon [deg] accuracy [m]
    """
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('logfile',help='logfile to append location to',nargs='?')
    p = p.parse_args()

    T = 60  # fastest allowed polling cadence is 1 minute

    logfile = p.logfile

    print('updating every {} seconds'.format(T))
    while True:
        ret = get_nmcli()
        loc = ret['location']
        stat = '{} {} {} {}'.format(datetime.now().strftime('%xT%X'),
                            loc['lat'], loc['lng'], ret['accuracy'])
        print(stat)

        if logfile:
            with open(logfile,'a') as f:
                f.write(stat+'\n')

        sleep(T)