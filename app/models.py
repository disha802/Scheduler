from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Enum
)
from sqlalchemy.sql import func
from app.database import Base
import enum
from sqlalchemy import Boolean

class ReminderStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"


class ReminderJob(Base):
    __tablename__ = "reminder_jobs"

    id = Column(Integer, primary_key=True, index=True)

    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)

    event_type = Column(String, nullable=False)
    channel = Column(String, nullable=False)

    schedule_type = Column(String, nullable=False)
    interval_minutes = Column(Integer, nullable=True)

    next_run_at = Column(DateTime(timezone=True), nullable=True)
    last_run_at = Column(DateTime(timezone=True), nullable=True)

    stop_condition_type = Column(String, nullable=False)
    stop_condition_value = Column(String, nullable=False)

    status = Column(
        Enum(ReminderStatus),
        default=ReminderStatus.ACTIVE,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
    deleted_at = Column(
        DateTime(timezone=True), 
        nullable=True
    )


class StatusFlag(Base):
    __tablename__ = "status_flags"

    key = Column(String, primary_key=True, index=True)
    value = Column(Boolean, nullable=False, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )