import logging
from datetime import datetime

import requests
import pandas


def get_loc_mozilla(dat: pandas.DataFrame, url: str):

    json_to = dat.to_json(orient="records")

    json_to = '{ "wifiAccessPoints":' + json_to + "}"
    try:
        req = requests.post(url, data=json_to)
        if req.status_code != 200:
            logging.error(req.text)
            return None
    except requests.exceptions.ConnectionError as e:
        logging.error(f"no network connection.  {e}")
        return None
    # %% process MLS response
    json_from = req.json()
    loc = json_from["location"]
    loc["accuracy"] = json_from["accuracy"]
    loc["N"] = len(dat)  # number of BSSIDs used
    loc["t"] = datetime.now()

    return loc
