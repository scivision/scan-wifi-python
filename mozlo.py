#!/usr/bin/env python
"""
https://mozilla.github.io/ichnaea/api/geolocate.html
you should get your own Mozilla Location Services API key

Uses ``nmcli`` from Linux only. Could be extended to other tools and OS.
"""
import subprocess
from io import BytesIO
import pandas
import requests

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

    return ret.json()

if __name__ == '__main__':
    ret = get_nmcli()