import requests
import logging
import pandas
import json
import typing as T
from datetime import datetime


def get_loc_mozilla(dat: T.Sequence[T.Any], url: str):
    match dat:
        case pandas.DataFrame():
            json_to = dat.to_json(orient="records")
        case list():
            json_to = json.dumps(dat)
        case _:
            raise TypeError("Unknown data format")

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
