import logging

from gbfs.models.system_hours import SystemHours

logger = logging.getLogger()


def create_system_hours(session, data):
    """
    Create new system hour in DB.
    """
    logger.debug("create new system hour in DB.")
    system_hour = SystemHours(last_updated=data["last_updated"], data=data["data"])
    session.add(system_hour)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
