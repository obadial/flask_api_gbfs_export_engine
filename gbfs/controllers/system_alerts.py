import logging

from gbfs.models.system_alerts import SystemAlerts

logger = logging.getLogger()


def create_system_alerts(session, data):
    """
    Create new System Alert in DB.
    """
    logger.debug("create new system alert in DB.")
    system_alert = SystemAlerts(last_updated=data["last_updated"], data=data["data"])
    session.add(system_alert)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
