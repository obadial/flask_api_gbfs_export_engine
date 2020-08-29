import logging

from gbfs.models.system_regions import SystemRegions

logger = logging.getLogger()


def create_system_regions(session, data):
    """
    Create new system_regions in DB.
    """
    logger.debug("create new system_regions in DB.")
    system_regions = SystemRegions(last_updated=data["last_updated"], data=data["data"])
    session.add(system_regions)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
