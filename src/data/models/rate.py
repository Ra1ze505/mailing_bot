from sqlalchemy import JSON, Column, DateTime, Integer, func

from src.common.db import Base


class Rate(Base):
    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    date = Column(DateTime(timezone=True), server_default=func.now())
