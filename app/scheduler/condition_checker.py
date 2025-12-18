from app.database import SessionLocal
from app.models import ReminderJob, StatusFlag


def is_stop_condition_met(reminder: ReminderJob) -> bool:
    if reminder.stop_condition_type == "db_check":
        db = SessionLocal()
        try:
            flag = db.get(StatusFlag, reminder.stop_condition_value)
            return flag is not None and flag.value is True
        finally:
            db.close()

    return False
