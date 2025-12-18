from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReminderCreate(BaseModel):
    entity_type: str
    entity_id: str
    event_type: str
    channel: str
    schedule_type: str
    interval_minutes: Optional[int] = None
    stop_condition_type: str
    stop_condition_value: str


class ReminderResponse(ReminderCreate):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
