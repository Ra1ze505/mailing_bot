from sqlalchemy import Column, String

from src.common.db import Base


class BotSession(Base):
    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {"eager_defaults": True}

    session = Column(String, nullable=False, primary_key=True)
