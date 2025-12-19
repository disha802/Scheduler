from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app import models, schemas
from app.models import ReminderStatus

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=schemas.ReminderResponse)
def create_reminder(
    reminder: schemas.ReminderCreate,
    db: Session = Depends(get_db)
):
    # Idempotency check
    existing = (
        db.query(models.ReminderJob)
        .filter(
            models.ReminderJob.entity_type == reminder.entity_type,
            models.ReminderJob.entity_id == reminder.entity_id,
            models.ReminderJob.event_type == reminder.event_type,
            models.ReminderJob.status == ReminderStatus.ACTIVE,
        )
        .first()
    )

    if existing:
        return existing

    # Compute next run
    next_run = None
    if reminder.schedule_type == "recurring" and reminder.interval_minutes:
        next_run = datetime.now(timezone.utc) + timedelta(minutes=reminder.interval_minutes)

    db_reminder = models.ReminderJob(
        **reminder.dict(),
        next_run_at=next_run,
    )

    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)

    return db_reminder


@router.get("/")
def list_reminders(db: Session = Depends(get_db)):
    return db.query(models.ReminderJob).all()
