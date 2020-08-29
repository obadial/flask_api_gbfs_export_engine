import logging

from gbfs.models.gbfs import Gbfs

logger = logging.getLogger()


def create_gbfs(session, data):
    """
    Create new Gbfs in DB.
    """
    logger.debug("create new Gbfs with data : %s", data)
    gbfs_status = Gbfs(last_updated=data["last_updated"], data=data["data"])
    session.add(gbfs_status)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
