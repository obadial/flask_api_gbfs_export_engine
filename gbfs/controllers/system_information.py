import logging

from gbfs.models.system_information import SystemInformation

logger = logging.getLogger()


def create_system_information(session, data):
    """
    Create new system information in DB.
    """
    logger.debug("create new system information in DB.")
    system_information = SystemInformation(
        last_updated=data["last_updated"], data=data["data"]
    )
    session.add(system_information)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
