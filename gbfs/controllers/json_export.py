import datetime
import json

import os


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def json_export(data):

    data_json = json.dumps(data, default=myconverter)
    with open("json_export_gbfs.json", "w+") as f:
        f.write(data_json)
        f.close()
