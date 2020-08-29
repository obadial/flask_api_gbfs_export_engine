import logging

from gbfs.models.gbfs_version import GbfsVersion

logger = logging.getLogger()


def create_gbfs_version(session, data):
    """
    Create new Gbfs version in DB.
    """
    logger.debug("create new Gbfs version with data : %s", data)
    gbfs_version = GbfsVersion(last_updated=data["last_updated"], data=data["data"])
    session.add(gbfs_version)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
