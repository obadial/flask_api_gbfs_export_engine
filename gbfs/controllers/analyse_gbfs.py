import requests
import json

from gbfs.controllers.free_bike_status import create_free_bike_status
from gbfs.controllers.gbfs_version import create_gbfs_version
from gbfs.controllers.station_information import create_station_information
from gbfs.controllers.station_status import create_station_status
from gbfs.controllers.system_alerts import create_system_alerts
from gbfs.controllers.system_calendar import create_system_calendar
from gbfs.controllers.system_hours import create_system_hours
from gbfs.controllers.system_information import create_system_information
from gbfs.controllers.system_pricing_plans import create_system_pricing_plans
from gbfs.controllers.system_regions import create_system_regions
from gbfs.controllers.gbfs import create_gbfs
from gbfs.constantes import FREE_BIKE_URL
from gbfs.constantes import STATION_STATUS_URL


def analyse_gbfs(session, data):
    create_gbfs(session, data)
    feed = data["data"]["en"]["feeds"]
    payload = {}
    headers = {}

    for elem in feed:
        if elem["name"] == "system_information":
            response = requests.request(
                "GET", elem["url"], headers=headers, data=payload
            )
            create_system_information(session, json.loads(response.content))
        if elem["name"] == "station_information":
            response = requests.request(
                "GET", elem["url"], headers=headers, data=payload
            )
            create_station_information(session, json.loads(response.content))
            station_informations = json.loads(response.content)
        if elem["name"] == "station_status":
            response = requests.request(
                "GET", elem["url"], headers=headers, data=payload
            )
            STATION_STATUS_URL = elem["url"]
            FREE_BIKE_URL = ""  # peux poser des porbleeme a garder en tete
            bikes_element = {}
            list_bike_id = ""
            create_station_status(session, json.loads(response.content))
        if elem["name"] == "gbfs_version":
            response = requests.request(
                "GET", elem["url"], headers=headers, data=payload
            )
            create_gbfs_version(session, json.loads(response.content))
        if elem["name"] == "free_bike_status":
            response = requests.request(
                "GET", elem["url"], headers=headers, data=payload
            )
            FREE_BIKE_URL = elem["url"]
            STATION_STATUS_URL = ""
            response_dict = json.loads(response.content)
            bikes_element = response_dict["data"]["bikes"]
            list_bike_id = [sub["bike_id"] for sub in bikes_element]
            create_free_bike_status(session, json.loads(response.content))
        if elem["name"] == "system_hours":
            response = requests.request(
                "GET", elem["url"], headers=headers, data=payload
            )
            create_system_hours(session, json.loads(response.content))
        if elem["name"] == "system_calendar":
            response = requests.request(
                "GET", elem["url"], headers=headers, data=payload
            )
            create_system_calendar(session, json.loads(response.content))
        if elem["name"] == "system_regions":
            response = requests.request(
                "GET", elem["url"], headers=headers, data=payload
            )
            create_system_regions(session, json.loads(response.content))
        if elem["name"] == "system_pricing_plans":
            response = requests.request(
                "GET", elem["url"], headers=headers, data=payload
            )
            create_system_pricing_plans(session, json.loads(response.content))
        if elem["name"] == "system_alerts":
            response = requests.request(
                "GET", elem["url"], headers=headers, data=payload
            )
            create_system_alerts(session, json.loads(response.content))
    return (
        STATION_STATUS_URL,
        FREE_BIKE_URL,
        list_bike_id,
        bikes_element,
        station_informations,
    )
