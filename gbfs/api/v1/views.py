from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import request
from marshmallow import ValidationError
from time import sleep

from gbfs.extensions import db
from gbfs.controllers.analyse_gbfs import analyse_gbfs
from gbfs.controllers.repeated_timer import RepeatedTimer
from gbfs.controllers.free_bike_status import actualise_data_of_free_bike_status
from gbfs.controllers.station_status import actualise_data_of_station_status
from gbfs.constantes import DURATION_EXECUTION
from gbfs.constantes import FREE_BIKE_URL
from gbfs.constantes import STATION_STATUS_URL
from gbfs.controllers.export_data import export_data


blueprint = Blueprint("api_v1", __name__, url_prefix="/api/v1")


@blueprint.errorhandler(404)
def handle_gbfs_error(e):
    return jsonify(e.messages), 404


@blueprint.route("/ping", methods=["GET"])
def ping():
    return "pong", 200


@blueprint.route("/send_gbfs", methods=["POST"])
def catch_information():
    (
        STATION_STATUS_URL,
        FREE_BIKE_URL,
        list_bike_id,
        list_bike,
        station_information,
    ) = analyse_gbfs(db.session, request.json)
    history_list = []
    print("GBFS export engine is starting...")
    message = (
        "Please wait " + str(DURATION_EXECUTION) + " seconds for the first reports."
    )
    print(message)
    if FREE_BIKE_URL == "":
        rt = RepeatedTimer(
            2,
            actualise_data_of_station_status,
            STATION_STATUS_URL,
            list_bike_id,
            list_bike,
            station_information,
            history_list,
        )
        try:
            sleep(DURATION_EXECUTION)
        finally:
            rt.stop()
    else:
        rt = RepeatedTimer(
            2,
            actualise_data_of_free_bike_status,
            FREE_BIKE_URL,
            list_bike_id,
            list_bike,
            station_information,
            history_list,
        )
        try:
            sleep(DURATION_EXECUTION)
        finally:
            rt.stop()
    export_data(history_list)
    print(history_list)
    return jsonify(history_list), 200

