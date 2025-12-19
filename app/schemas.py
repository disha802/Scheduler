from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models import ReminderJob


class ReminderCreate(BaseModel):
    entity_type: str
    entity_id: str
    event_type: str
    channel: str
    schedule_type: str
    interval_minutes: Optional[int] = None
    stop_condition_type: str
    stop_condition_value: str
    start_time: Optional[datetime] = Field(
        None, 
        description="When to start sending reminders (ISO format in IST, e.g., '2025-12-20T10:00:00'). If not provided, recurring reminders start after first interval, one-time reminders send immediately."
    )


# Generate Pydantic model from Tortoise model
ReminderResponse = pydantic_model_creator(
    ReminderJob,
    name="ReminderResponse",
    exclude=("deleted_at",)
)