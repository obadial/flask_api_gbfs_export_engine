import logging

from gbfs.models.system_calendar import SystemCalendar

logger = logging.getLogger()


def create_system_calendar(session, data):
    """
    Create new System Calendar in DB.
    """
    logger.debug("create new system calendar in DB.")
    system_calendar = SystemCalendar(
        last_updated=data["last_updated"], data=data["data"]
    )
    session.add(system_calendar)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
