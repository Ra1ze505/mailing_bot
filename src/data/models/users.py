import datetime

from sqlalchemy import Column, Integer, String, Time

from src.common.db import Base


class Users(Base):
    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {"eager_defaults": True}
    id: int = Column(Integer, primary_key=True, index=True)
    chat_id: int = Column(Integer, unique=True, index=True)
    username: str = Column(String, nullable=True)
    city: str = Column(String(50), default="Москва")
    timezone: int = Column(Integer, default=3)
    time_mailing: datetime.time = Column(Time, default=datetime.time(hour=5, minute=0))
