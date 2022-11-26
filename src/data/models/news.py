from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Text

from src.common.db import Base


class News(Base):
    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {"eager_defaults": True}

    id: int = Column(Integer, primary_key=True, index=True)
    content: str = Column(Text, nullable=False)
    created_at: datetime = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )
