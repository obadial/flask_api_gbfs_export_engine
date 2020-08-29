def get_last_element(session, DbTable):
    """
    Return the last element add in DB.
    """
    logger.debug("get last selected element in db ")
    element = session.query(DbTable).order_by(DbTable.date_creation.desc()).first()
    return element
