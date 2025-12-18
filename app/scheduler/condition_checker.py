from app.models import ReminderJob


def is_stop_condition_met(reminder: ReminderJob) -> bool:
    """
    Evaluates whether the reminder should stop.

    For now, this is a mocked implementation.
    """

    if reminder.stop_condition_type == "api_check":
        # 🔹 MOCK LOGIC (replace later with real API/db check)
        # Example: feedback_submitted == true
        # For now, always return False (i.e., keep reminding)
        return False

    # Default: do not stop
    return False
