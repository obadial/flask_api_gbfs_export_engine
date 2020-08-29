import logging
import requests
import json
from datetime import datetime

from gbfs.models.free_bike_status import FreeBikeStatus

logger = logging.getLogger()


def create_free_bike_status(session, data):
    """
    Create new Free Bike Status in DB.
    """
    logger.debug("create new free bike status with data : %s", data)
    free_bike_status = FreeBikeStatus(
        last_updated=data["last_updated"], data=data["data"]
    )
    session.add(free_bike_status)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise


def add_element_in_list(bike_id, old_list_bike, station_information, history_list):
    for elem in old_list_bike:
        if elem["bike_id"] == bike_id:
            if station_information["data"]["stations"] == []:
                station_id = ""
                name = ""
                short_name = ""
            else:
                for elem_station in station_information["data"]["stations"]:
                    station_id = elem_station["station_id"]
                    name = elem_station["name"]
                    short_name = ""
                new_info_elem = {
                    "started_at": datetime.utcnow().isoformat(),
                    "ended_at": "",
                    "duration": "",
                    "start_station_id": station_id,
                    "start_station_name": name,
                    "start_station_description": short_name,
                    "start_station_latitude": elem["lat"],
                    "start_station_longitude": elem["lon"],
                    "end_station_id": "",
                    "end_station_name": "",
                    "end_station_description": "",
                    "end_station_latitude": "",
                    "end_station_longitude": "",
                }
                history_list.append(new_info_elem)
                return history_list


def update_element_in_list(bike_id, new_list_bike, station_information, history_list):
    found_elem = 0
    for elem in new_list_bike:
        if elem["bike_id"] == bike_id:
            if station_information["data"]["stations"] == []:
                station_id = ""
                name = ""
                short_name = ""
            else:
                for elem_station in station_information["data"]["stations"]:
                    station_id = elem_station["station_id"]
                    name = elem_station["name"]
                    short_name = ""
                for elem_history in history_list:
                    if (
                        elem_history["start_station_latitude"] == elem["lat"]
                        and elem_history["start_station_longitude"] == elem["lon"]
                    ):
                        found_elem = 1
                        elem_history["ended_at"] = datetime.utcnow()
                        elem_history["end_station_id"] = station_id
                        elem_history["end_station_name"] = name
                        elem_history["end_station_description"] = short_name
                        elem_history["end_station_latitude"] = elem["lat"]
                        elem_history["end_station_longitude"] = elem["lon"]
                        if elem_history["ended_at"] is not "":
                            delta = (
                                elem_history["ended_at"] - elem_history["started_at"]
                            )
                            elem_history["duration"] = delta.total_seconds()
                        else:
                            elem_history["duration"] = 0
                if found_elem == 0:
                    new_info_elem = {
                        "started_at": "",
                        "ended_at": datetime.utcnow().isoformat(),
                        "duration": "",
                        "start_station_id": "",
                        "start_station_name": "",
                        "start_station_description": "",
                        "start_station_latitude": "",
                        "start_station_longitude": "",
                        "end_station_id": station_id,
                        "end_station_name": name,
                        "end_station_description": short_name,
                        "end_station_latitude": elem["lat"],
                        "end_station_longitude": elem["lon"],
                    }
                history_list.append(new_info_elem)
            return history_list


def check_if_all_old_are_in_new(
    old_list, new_list, old_list_bike, station_information, history_list
):
    for elem in old_list:
        if elem not in new_list:
            history_list = add_element_in_list(
                elem, old_list_bike, station_information, history_list
            )
            return history_list, 401
    return "", 201


def check_if_no_new_are_not_in_old(
    old_list, new_list, new_list_bike, station_information, history_list
):
    for elem in new_list:
        if elem not in old_list:
            history_list = update_element_in_list(
                elem, new_list_bike, station_information, history_list
            )
            return history_list, 402
    return "", 202


def actualise_data_of_free_bike_status(
    url, old_list_bike_id, old_list_bike, station_information, history_list
):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_dict = json.loads(response.content)
    bikes_element = response_dict["data"]["bikes"]
    new_list_bike_id = [sub["bike_id"] for sub in bikes_element]
    elem_return, code_error = check_if_all_old_are_in_new(
        old_list_bike_id,
        new_list_bike_id,
        old_list_bike,
        station_information,
        history_list,
    )
    if code_error == 401:
        history_list = elem_return
    elem_return, code_error = check_if_no_new_are_not_in_old(
        old_list_bike_id,
        new_list_bike_id,
        bikes_element,
        station_information,
        history_list,
    )
    if code_error == 402:
        history_list = elem_return
    return new_list_bike_id, bikes_element, station_information, history_list
