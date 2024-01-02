from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text

from src.common.db import Base


class FeedBack(Base):
    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {"eager_defaults": True}
    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    message: str = Column(Text, nullable=False)
    send_time: datetime = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )
