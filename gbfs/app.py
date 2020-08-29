from flask import Flask

from gbfs.api import api_v1
from gbfs.extensions import db
from gbfs.models.free_bike_status import FreeBikeStatus
from gbfs.models.gbfs import Gbfs
from gbfs.models.gbfs_version import GbfsVersion
from gbfs.models.station_information import StationInformation
from gbfs.models.station_status import StationStatus
from gbfs.models.system_alerts import SystemAlerts
from gbfs.models.system_calendar import SystemCalendar
from gbfs.models.system_hours import SystemHours
from gbfs.models.system_information import SystemInformation
from gbfs.models.system_pricing_plans import SystemPricingPlans
from gbfs.models.system_regions import SystemRegions


def create_app():
    app = Flask(__name__)
    configure_app(app)
    configure_blueprints(app)
    configure_extensions(app)
    db.app = app
    db.create_all()
    return app


def configure_app(app):
    app.config.from_object("gbfs.config")


def configure_blueprints(app):
    app.register_blueprint(api_v1)


def configure_extensions(app):
    db.init_app(app)
