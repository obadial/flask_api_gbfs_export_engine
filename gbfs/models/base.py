from datetime import datetime

import pytz
from sqlalchemy import Column
from sqlalchemy import DateTime


class TimestampMixin(object):
    date_creation = Column(
        DateTime(timezone=True),
        default=datetime.now(tz=pytz.timezone("UTC")),
        nullable=False,
    )
    date_modification = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(tz=pytz.timezone("UTC")),
        onupdate=datetime.now(tz=pytz.timezone("UTC")),
    )
