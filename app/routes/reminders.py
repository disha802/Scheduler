from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException
from app import models, schemas
from app.models import ReminderStatus
import pytz

router = APIRouter()
IST = pytz.timezone('Asia/Kolkata')


@router.post("/", response_model=schemas.ReminderResponse)
async def create_reminder(reminder: schemas.ReminderCreate):
    """Create a new reminder"""
    
    # Idempotency check
    existing = await models.ReminderJob.filter(
        entity_type=reminder.entity_type,
        entity_id=reminder.entity_id,
        event_type=reminder.event_type,
        status=ReminderStatus.ACTIVE,
        deleted_at__isnull=True
    ).first()
    
    if existing:
        return await schemas.ReminderResponse.from_tortoise_orm(existing)
    
    # Compute next run
    now = datetime.now(timezone.utc)
    
    if reminder.start_time:
        # Use the provided start time (convert from IST to UTC if needed)
        if reminder.start_time.tzinfo is None:
            # Assume IST if no timezone provided
            start_time_ist = IST.localize(reminder.start_time)
            next_run = start_time_ist.astimezone(timezone.utc)
        else:
            next_run = reminder.start_time.astimezone(timezone.utc)
        
        # Don't allow scheduling in the past
        if next_run < now:
            raise HTTPException(
                status_code=400, 
                detail="Start time cannot be in the past"
            )
    else:
        # No start_time provided
        if reminder.schedule_type == "recurring" and reminder.interval_minutes:
            # Recurring without start_time: start after first interval
            next_run = now + timedelta(minutes=reminder.interval_minutes)
        else:
            # One-time without start_time: send immediately
            next_run = now
    
    # Create reminder
    db_reminder = await models.ReminderJob.create(
        entity_type=reminder.entity_type,
        entity_id=reminder.entity_id,
        event_type=reminder.event_type,
        channel=reminder.channel,
        schedule_type=reminder.schedule_type,
        interval_minutes=reminder.interval_minutes,
        stop_condition_type=reminder.stop_condition_type,
        stop_condition_value=reminder.stop_condition_value,
        next_run_at=next_run,
        start_time=reminder.start_time,
    )
    
    return await schemas.ReminderResponse.from_tortoise_orm(db_reminder)


@router.get("/", response_model=list[schemas.ReminderResponse])
async def list_reminders():
    """List all reminders (excluding soft-deleted)"""
    reminders = await models.ReminderJob.filter(deleted_at__isnull=True).all()
    return [await schemas.ReminderResponse.from_tortoise_orm(r) for r in reminders]


@router.get("/active", response_model=list[schemas.ReminderResponse])
async def list_active_reminders():
    """List only active reminders"""
    reminders = await models.ReminderJob.filter(
        status=ReminderStatus.ACTIVE,
        deleted_at__isnull=True
    ).all()
    return [await schemas.ReminderResponse.from_tortoise_orm(r) for r in reminders]


@router.get("/{reminder_id}", response_model=schemas.ReminderResponse)
async def get_reminder(reminder_id: int):
    """Get a specific reminder"""
    reminder = await models.ReminderJob.filter(id=reminder_id, deleted_at__isnull=True).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return await schemas.ReminderResponse.from_tortoise_orm(reminder)


@router.delete("/{reminder_id}")
async def delete_reminder(reminder_id: int):
    """Soft delete a reminder"""
    reminder = await models.ReminderJob.filter(id=reminder_id, deleted_at__isnull=True).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    reminder.deleted_at = datetime.now(timezone.utc)
    reminder.status = ReminderStatus.COMPLETED
    await reminder.save()
    
    return {"message": "Reminder deleted successfully", "id": reminder_id}


@router.post("/{reminder_id}/pause")
async def pause_reminder(reminder_id: int):
    """Pause a reminder"""
    reminder = await models.ReminderJob.filter(id=reminder_id, deleted_at__isnull=True).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    if reminder.status != ReminderStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Only active reminders can be paused")
    
    reminder.status = ReminderStatus.PAUSED
    await reminder.save()
    
    return {"message": "Reminder paused successfully", "id": reminder_id}


@router.post("/{reminder_id}/resume")
async def resume_reminder(reminder_id: int):
    """Resume a paused reminder"""
    reminder = await models.ReminderJob.filter(id=reminder_id, deleted_at__isnull=True).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    if reminder.status != ReminderStatus.PAUSED:
        raise HTTPException(status_code=400, detail="Reminder is not paused")
    
    reminder.status = ReminderStatus.ACTIVE
    
    # Reschedule based on type
    now = datetime.now(timezone.utc)
    if reminder.schedule_type == "recurring" and reminder.interval_minutes:
        reminder.next_run_at = now + timedelta(minutes=reminder.interval_minutes)
    else:
        # One-time reminder: schedule immediately
        reminder.next_run_at = now
    
    await reminder.save()
    
    return {"message": "Reminder resumed successfully", "id": reminder_id}