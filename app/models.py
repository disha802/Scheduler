from tortoise import fields
from tortoise.models import Model
from enum import Enum


class ReminderStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"


class ReminderJob(Model):
    id = fields.IntField(pk=True)
    
    # Entity metadata
    entity_type = fields.CharField(max_length=100)
    entity_id = fields.CharField(max_length=100)
    
    # Event metadata
    event_type = fields.CharField(max_length=100)
    channel = fields.CharField(max_length=50)
    
    # Scheduling
    schedule_type = fields.CharField(max_length=50)
    interval_minutes = fields.IntField(null=True)
    start_time = fields.DatetimeField(null=True)  # NEW: When to start sending
    
    next_run_at = fields.DatetimeField(null=True)
    last_run_at = fields.DatetimeField(null=True)
    
    # Stop condition
    stop_condition_type = fields.CharField(max_length=100)
    stop_condition_value = fields.CharField(max_length=255)
    
    # Status
    status = fields.CharEnumField(ReminderStatus, default=ReminderStatus.ACTIVE)
    
    # Timestamps
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)
    
    class Meta:
        table = "reminder_jobs"
        indexes = [
            ("status", "next_run_at"),  # Composite index for scheduler
        ]

    def __str__(self):
        return f"Reminder {self.id}: {self.entity_type}/{self.entity_id}"


class StatusFlag(Model):
    key = fields.CharField(max_length=255, pk=True)
    value = fields.BooleanField(default=False)
    
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "status_flags"

    def __str__(self):
        return f"{self.key}: {self.value}"