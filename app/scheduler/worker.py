from app.scheduler.condition_checker import is_stop_condition_met
from app.models import ReminderJob, ReminderStatus
from datetime import datetime, timezone, timedelta
from app.database import SessionLocal
import time

POLL_INTERVAL_SECONDS = 30

def run_scheduler():
    print("🟢 Scheduler started")

    while True:
        db = SessionLocal()
        try:
            now = datetime.now(timezone.utc)
            print(f"🔍 Scheduler tick at {now}")

            reminders = (
                db.query(ReminderJob)
                .filter(ReminderJob.status == ReminderStatus.ACTIVE)
                .filter(ReminderJob.next_run_at <= now)
                .all()
            )

            if not reminders:
                print("😴 No reminders due")

            for reminder in reminders:
                print(f"⏰ Evaluating reminder {reminder.id}")

                # 🧠 Stop-condition check
                if is_stop_condition_met(reminder):
                    print(f"✅ Stop condition met for reminder {reminder.id}")
                    reminder.status = ReminderStatus.COMPLETED
                    continue

                print(f"📨 Triggering reminder {reminder.id}")

                reminder.last_run_at = now
                reminder.next_run_at = now + timedelta(
                    minutes=reminder.interval_minutes or 0
                )


            db.commit()
        finally:
            db.close()

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_scheduler()
