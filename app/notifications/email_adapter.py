def send_email_notification(reminder):
    """
    Dummy email sender.
    Replace with real email provider later.
    """
    print(
        f"📧 [EMAIL SENT] "
        f"Entity={reminder.entity_type}:{reminder.entity_id} | "
        f"Event={reminder.event_type}"
    )
