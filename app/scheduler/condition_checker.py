from app.models import ReminderJob, StatusFlag


async def is_stop_condition_met(reminder: ReminderJob) -> bool:
    """Check if reminder's stop condition is met"""
    if reminder.stop_condition_type == "db_check":
        flag = await StatusFlag.filter(key=reminder.stop_condition_value).first()
        return flag is not None and flag.value is True
    
    return False