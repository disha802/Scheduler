from app.notifications.email_adapter import send_email_notification


def dispatch_notification(reminder):
    if reminder.channel == "email":
        send_email_notification(reminder)
    else:
        print(f"⚠️ No adapter for channel: {reminder.channel}")
