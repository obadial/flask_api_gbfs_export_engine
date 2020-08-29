import logging

from gbfs.models.system_pricing_plans import SystemPricingPlans

logger = logging.getLogger()


def create_system_pricing_plans(session, data):
    """
    Create new system pricing plans in DB.
    """
    logger.debug("create new system pricing plans in DB.")
    system_pricing_plan = SystemPricingPlans(
        last_updated=data["last_updated"], data=data["data"]
    )
    session.add(system_pricing_plan)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
