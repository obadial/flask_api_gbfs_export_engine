import logging

from gbfs.models.station_information import StationInformation

logger = logging.getLogger()


def create_station_information(session, data):
    """
    Create new Station Information in DB.
    """
    logger.debug("create new station information entry in DB.")
    station_information = StationInformation(
        last_updated=data["last_updated"], data=data["data"]
    )
    session.add(station_information)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
