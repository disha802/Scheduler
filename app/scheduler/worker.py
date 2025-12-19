from app.scheduler.condition_checker import is_stop_condition_met
from app.scheduler.notifier import trigger_notification
from app.models import ReminderJob, ReminderStatus
from datetime import datetime, timezone, timedelta
from app.database import init_db, close_db
import asyncio
import pytz

POLL_INTERVAL_SECONDS = 30
IST = pytz.timezone('Asia/Kolkata')


def utc_to_ist(utc_dt):
    """Convert UTC datetime to IST for display"""
    if utc_dt is None:
        return None
    return utc_dt.astimezone(IST)


async def run_scheduler():
    """Main scheduler loop"""
    print("🟢 Scheduler started")
    print(f"⏱️  Poll interval: {POLL_INTERVAL_SECONDS} seconds")
    print(f"🌏 Display timezone: IST (Asia/Kolkata)")
    
    await init_db()
    
    try:
        while True:
            try:
                now = datetime.now(timezone.utc)
                now_ist = utc_to_ist(now)
                print(f"\n🔍 Scheduler tick at {now_ist.strftime('%Y-%m-%d %H:%M:%S IST')}")
                
                # Query for active reminders that are due
                reminders = await ReminderJob.filter(
                    status=ReminderStatus.ACTIVE,
                    deleted_at__isnull=True,
                    next_run_at__lte=now
                ).all()
                
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
                        
                        # Check stop condition BEFORE sending notification
                        if await is_stop_condition_met(reminder):
                            print(f"✅ Stop condition met for reminder {reminder.id}")
                            reminder.status = ReminderStatus.COMPLETED
                            await reminder.save()
                            print(f"🏁 Reminder {reminder.id} marked as COMPLETED")
                            continue
                        
                        # Trigger notification
                        print(f"📨 Triggering notification for reminder {reminder.id}")
                        
                        notification_data = {
                            'entity_type': reminder.entity_type,
                            'entity_id': reminder.entity_id,
                            'event_type': reminder.event_type,
                            'channel': reminder.channel,
                            'recipient_email': f"{reminder.entity_id}@example.com",
                        }
                        
                        notification_success = trigger_notification(notification_data)
                        
                        if notification_success:
                            print(f"✅ Notification sent successfully for reminder {reminder.id}")
                        else:
                            print(f"⚠️ Notification failed for reminder {reminder.id}")
                        
                        # Update last run time
                        reminder.last_run_at = now
                        
                        # Schedule next run based on schedule type
                        if reminder.schedule_type == "recurring" and reminder.interval_minutes:
                            reminder.next_run_at = now + timedelta(minutes=reminder.interval_minutes)
                            next_run_ist = utc_to_ist(reminder.next_run_at)
                            print(f"🔄 Rescheduled for {next_run_ist.strftime('%Y-%m-%d %H:%M:%S IST')}")
                        else:
                            reminder.status = ReminderStatus.COMPLETED
                            print(f"🏁 One-time reminder {reminder.id} completed")
                        
                        await reminder.save()
                        
                    except Exception as e:
                        print(f"❌ Error processing reminder {reminder.id}: {e}")
                        continue
                
            except Exception as e:
                print(f"❌ Scheduler error: {e}")
            
            print(f"\n💤 Sleeping for {POLL_INTERVAL_SECONDS} seconds...")
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
            
    finally:
        await close_db()


if __name__ == "__main__":
    asyncio.run(run_scheduler())