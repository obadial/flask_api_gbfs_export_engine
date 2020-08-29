import logging
import requests
import json
from datetime import datetime

from gbfs.models.station_status import StationStatus

logger = logging.getLogger()


def create_station_status(session, data):
    """
    Create new Station Status in DB.
    """
    logger.debug("create new station status in DB.")
    station_status = StationStatus(last_updated=data["last_updated"], data=data["data"])
    session.add(station_status)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise


def add_element_in_list_station(station_id, station_information, history_list, nb_of_bike):
    index_of_exec = 0
    while index_of_exec < nb_of_bike:
        # print("depart d'un velo")
        for elem in station_information["data"]["stations"]:
            if elem["station_id"] == station_id:
                new_info_elem = {
                    "started_at": datetime.utcnow().isoformat(),
                    "ended_at": "",
                    "duration": "",
                    "start_station_id": station_id,
                    "start_station_name": elem["name"],
                    "start_station_description": "",
                    "start_station_latitude": elem["lat"],
                    "start_station_longitude": elem["lon"],
                    "end_station_id": "",
                    "end_station_name": "",
                    "end_station_description": "",
                    "end_station_latitude": "",
                    "end_station_longitude": "",
                }
                history_list.append(new_info_elem)
                index_of_exec = index_of_exec + 1
        return history_list


def update_element_in_list_station(station_id, station_information, history_list, nb_of_bike):
    index_of_exec = 0
    while index_of_exec < nb_of_bike:
        found_elem = 0
        for station in station_information["data"]["stations"]:
            if station["station_id"] == station_id:
                my_station = station
        for elem_history in history_list:
            if (
                elem_history["start_station_id"] == station_id
                and elem_history["end_station_id"] == ""
            ):
                found_elem = 1
                elem_history["ended_at"] = datetime.utcnow()
                elem_history["end_station_id"] = station_id
                elem_history["end_station_name"] = my_station["name"]
                elem_history["end_station_description"] = ""
                elem_history["end_station_latitude"] = my_station["lat"]
                elem_history["end_station_longitude"] = my_station["lon"]
                if elem_history["ended_at"] is not "":
                    delta = elem_history["ended_at"] - elem_history["started_at"]
                    elem_history["duration"] = delta.total_seconds()
                else:
                    elem_history["duration"] = 0
        if found_elem == 0:
            new_info_elem = {
                "started_at": datetime.utcnow(),
                "ended_at": "",
                "duration": "",
                "start_station_id": station_id,
                "start_station_name": my_station["name"],
                "start_station_description": "",
                "start_station_latitude": my_station["lat"],
                "start_station_longitude": my_station["lon"],
                "end_station_id": "",
                "end_station_name": "",
                "end_station_description": "",
                "end_station_latitude": "",
                "end_station_longitude": "",
            }
            found_elem = 0
            history_list.append(new_info_elem)
        index_of_exec = index_of_exec + 1
    return history_list


def check_if_change_in_station(old_list_station, new_list_station, station_information, history_list):
    if old_list_station != "":
        first_list_diseaper = set(old_list_station) - set(new_list_station)
        first_list_new = set(new_list_station) - set(old_list_station)
        if first_list_diseaper != set() and first_list_new != set():
            list_diseaper = list(first_list_diseaper)
            list_new = list(first_list_new)
            for elem1 in list_diseaper:
                for elem2 in list_new:
                    if elem1[0] == elem2[0]:
                        if elem1[1] > elem2[1]:
                            nb_of_bike = elem1[1] - elem2[1]
                            history_list = add_element_in_list_station(
                                elem1[0], station_information, history_list, nb_of_bike
                            )
                        elif elem1[1] < elem2[1]:
                            nb_of_bike = elem2[1] - elem1[1]
                            history_list = update_element_in_list_station(
                                elem1[0], station_information, history_list, nb_of_bike
                            )
            return history_list, 401
    return "", 201


def actualise_data_of_station_status(url, old_station_status_tuples, old_list_station, station_information, history_list):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_dict = json.loads(response.content)
    station_element = response_dict["data"]["stations"]
    new_list_station_id = [sub["station_id"] for sub in station_element]
    new_list_bikes_available = [sub["num_bikes_available"] for sub in station_element]
    new_station_status_tuples = list(zip(new_list_station_id, new_list_bikes_available))
    elem_return, code_error = check_if_change_in_station(
        old_station_status_tuples,
        new_station_status_tuples,
        station_information,
        history_list,
    )
    if code_error == 401:
        history_list = elem_return
    return new_station_status_tuples, station_element, station_information, history_list
