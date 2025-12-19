from app.scheduler.condition_checker import is_stop_condition_met
from app.scheduler.notifier import trigger_notification
from app.models import ReminderJob, ReminderStatus
from datetime import datetime, timezone, timedelta
from app.database import SessionLocal
import time

POLL_INTERVAL_SECONDS = 30


def run_scheduler():
    print("🟢 Scheduler started")
    print(f"⏱️  Poll interval: {POLL_INTERVAL_SECONDS} seconds")

    while True:
        db = SessionLocal()
        try:
            now = datetime.now(timezone.utc)
            print(f"\n🔍 Scheduler tick at {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")

            # Query for active reminders that are due
            # with_for_update(skip_locked=True) prevents race conditions with multiple workers
            reminders = (
                db.query(ReminderJob)
                .filter(ReminderJob.status == ReminderStatus.ACTIVE)
                .filter(ReminderJob.deleted_at.is_(None))  # Respect soft deletes
                .filter(ReminderJob.next_run_at <= now)
                .with_for_update(skip_locked=True)  # Row-level locking
                .all()
            )

            if not reminders:
                print("😴 No reminders due")
            else:
                print(f"📋 Found {len(reminders)} reminder(s) to process")

            for reminder in reminders:
                try:
                    print(f"\n⏰ Processing reminder ID: {reminder.id}")
                    print(f"   Entity: {reminder.entity_type}/{reminder.entity_id}")
                    print(f"   Event: {reminder.event_type}")
                    print(f"   Channel: {reminder.channel}")

                    # 🧠 Check stop condition BEFORE sending notification
                    if is_stop_condition_met(reminder):
                        print(f"✅ Stop condition met for reminder {reminder.id}")
                        reminder.status = ReminderStatus.COMPLETED
                        reminder.updated_at = now
                        db.commit()
                        print(f"🏁 Reminder {reminder.id} marked as COMPLETED")
                        continue

                    # 📨 Trigger notification
                    print(f"📨 Triggering notification for reminder {reminder.id}")
                    
                    notification_data = {
                        'entity_type': reminder.entity_type,
                        'entity_id': reminder.entity_id,
                        'event_type': reminder.event_type,
                        'channel': reminder.channel,
                        'recipient_email': f"{reminder.entity_id}@example.com",  # Replace with actual lookup
                    }
                    
                    notification_success = trigger_notification(notification_data)
                    
                    if notification_success:
                        print(f"✅ Notification sent successfully for reminder {reminder.id}")
                    else:
                        print(f"⚠️ Notification failed for reminder {reminder.id}")

                    # Update last run time
                    reminder.last_run_at = now

                    # 🔄 Schedule next run based on schedule type
                    if reminder.schedule_type == "recurring" and reminder.interval_minutes:
                        reminder.next_run_at = now + timedelta(minutes=reminder.interval_minutes)
                        print(f"🔄 Rescheduled for {reminder.next_run_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                    else:
                        # One-time reminder - mark as completed after sending
                        reminder.status = ReminderStatus.COMPLETED
                        print(f"🏁 One-time reminder {reminder.id} completed")

                    reminder.updated_at = now
                    db.commit()

                except Exception as e:
                    print(f"❌ Error processing reminder {reminder.id}: {e}")
                    db.rollback()
                    # Continue with next reminder instead of crashing
                    continue

        except Exception as e:
            print(f"❌ Scheduler error: {e}")
            db.rollback()
        finally:
            db.close()

        print(f"\n💤 Sleeping for {POLL_INTERVAL_SECONDS} seconds...")
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_scheduler()