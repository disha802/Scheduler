# Test Payloads & Commands

## 1. Create Recurring Reminder (Feedback Form)

### cURL Command
```bash
curl -X POST "http://127.0.0.1:8000/reminders/" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "interviewer",
    "entity_id": "INT_100",
    "event_type": "feedback_form",
    "channel": "email",
    "schedule_type": "recurring",
    "interval_minutes": 1,
    "stop_condition_type": "db_check",
    "stop_condition_value": "feedback_submitted"
  }'
```

### JSON Payload
```json
{
  "entity_type": "interviewer",
  "entity_id": "INT_100",
  "event_type": "feedback_form",
  "channel": "email",
  "schedule_type": "recurring",
  "interval_minutes": 1,
  "stop_condition_type": "db_check",
  "stop_condition_value": "feedback_submitted"
}
```

**What it does**: Sends an email reminder every 1 minute until `feedback_submitted` flag is true.

---

## 2. Create One-Time Reminder (Interview Invitation)

### cURL Command
```bash
curl -X POST "http://127.0.0.1:8000/reminders/" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "candidate",
    "entity_id": "CAND_200",
    "event_type": "interview_invitation",
    "channel": "email",
    "schedule_type": "one_time",
    "interval_minutes": null,
    "stop_condition_type": "db_check",
    "stop_condition_value": "interview_scheduled"
  }'
```

### JSON Payload
```json
{
  "entity_type": "candidate",
  "entity_id": "CAND_200",
  "event_type": "interview_invitation",
  "channel": "email",
  "schedule_type": "one_time",
  "interval_minutes": null,
  "stop_condition_type": "db_check",
  "stop_condition_value": "interview_scheduled"
}
```

**What it does**: Sends one email immediately, then marks reminder as completed.

---

## 3. Create Hourly Payment Reminder

### cURL Command
```bash
curl -X POST "http://127.0.0.1:8000/reminders/" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "customer",
    "entity_id": "CUST_300",
    "event_type": "payment_reminder",
    "channel": "email",
    "schedule_type": "recurring",
    "interval_minutes": 60,
    "stop_condition_type": "db_check",
    "stop_condition_value": "invoice_paid_300"
  }'
```

### JSON Payload
```json
{
  "entity_type": "customer",
  "entity_id": "CUST_300",
  "event_type": "payment_reminder",
  "channel": "email",
  "schedule_type": "recurring",
  "interval_minutes": 60,
  "stop_condition_type": "db_check",
  "stop_condition_value": "invoice_paid_300"
}
```

**What it does**: Sends payment reminder every hour until invoice is marked as paid.

---

## 4. Create Daily Document Submission Reminder

### cURL Command
```bash
curl -X POST "http://127.0.0.1:8000/reminders/" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "employee",
    "entity_id": "EMP_400",
    "event_type": "document_submission",
    "channel": "email",
    "schedule_type": "recurring",
    "interval_minutes": 1440,
    "stop_condition_type": "db_check",
    "stop_condition_value": "documents_submitted_400"
  }'
```

### JSON Payload
```json
{
  "entity_type": "employee",
  "entity_id": "EMP_400",
  "event_type": "document_submission",
  "channel": "email",
  "schedule_type": "recurring",
  "interval_minutes": 1440,
  "stop_condition_type": "db_check",
  "stop_condition_value": "documents_submitted_400"
}
```

**What it does**: Sends daily (1440 minutes = 24 hours) reminder until documents are submitted.

---

## 5. Create Slack Reminder (Future Use)

### cURL Command
```bash
curl -X POST "http://127.0.0.1:8000/reminders/" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "team",
    "entity_id": "TEAM_500",
    "event_type": "standup_reminder",
    "channel": "slack",
    "schedule_type": "recurring",
    "interval_minutes": 30,
    "stop_condition_type": "db_check",
    "stop_condition_value": "standup_completed"
  }'
```

### JSON Payload
```json
{
  "entity_type": "team",
  "entity_id": "TEAM_500",
  "event_type": "standup_reminder",
  "channel": "slack",
  "schedule_type": "recurring",
  "interval_minutes": 30,
  "stop_condition_type": "db_check",
  "stop_condition_value": "standup_completed"
}
```

**What it does**: Sends Slack message every 30 minutes until standup is marked complete.

---

## Testing Stop Conditions

### 1. Insert Status Flag (Before Creating Reminder)

```sql
-- For feedback form reminder
INSERT INTO status_flags (key, value)
VALUES ('feedback_submitted', false);

-- For payment reminder
INSERT INTO status_flags (key, value)
VALUES ('invoice_paid_300', false);

-- For document submission
INSERT INTO status_flags (key, value)
VALUES ('documents_submitted_400', false);
```

### 2. Complete a Reminder (Set Flag to True)

```sql
-- Mark feedback as submitted
UPDATE status_flags
SET value = true, updated_at = NOW()
WHERE key = 'feedback_submitted';

-- Mark invoice as paid
UPDATE status_flags
SET value = true, updated_at = NOW()
WHERE key = 'invoice_paid_300';
```

### 3. Reset a Flag (For Re-testing)

```sql
UPDATE status_flags
SET value = false, updated_at = NOW()
WHERE key = 'feedback_submitted';
```

---

## List All Reminders

### cURL Command
```bash
curl -X GET "http://127.0.0.1:8000/reminders/"
```

---

## Quick Test Workflow

### Step 1: Start Services
```bash
# Terminal 1: Start API
uvicorn app.main:app --reload

# Terminal 2: Start Worker
python -m app.scheduler.worker
```

### Step 2: Create Status Flag
```sql
INSERT INTO status_flags (key, value)
VALUES ('feedback_submitted', false);
```

### Step 3: Create Reminder (1-minute interval for quick testing)
```bash
curl -X POST "http://127.0.0.1:8000/reminders/" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "interviewer",
    "entity_id": "INT_100",
    "event_type": "feedback_form",
    "channel": "email",
    "schedule_type": "recurring",
    "interval_minutes": 1,
    "stop_condition_type": "db_check",
    "stop_condition_value": "feedback_submitted"
  }'
```

### Step 4: Watch Worker Logs
You should see:
```
📨 Triggering notification for reminder 1
📧 [DEMO MODE] Email notification:
   To: INT_100@example.com
   ...
🔄 Rescheduled for 2025-01-15 10:31:00 UTC
```

### Step 5: Complete the Reminder
```sql
UPDATE status_flags
SET value = true
WHERE key = 'feedback_submitted';
```

### Step 6: Watch Reminder Auto-Complete
You should see:
```
✅ Stop condition met for reminder 1
🏁 Reminder 1 marked as COMPLETED
```

---

## Python Requests Examples

If you prefer using Python:

```python
import requests

# Create reminder
response = requests.post(
    "http://127.0.0.1:8000/reminders/",
    json={
        "entity_type": "interviewer",
        "entity_id": "INT_100",
        "event_type": "feedback_form",
        "channel": "email",
        "schedule_type": "recurring",
        "interval_minutes": 1,
        "stop_condition_type": "db_check",
        "stop_condition_value": "feedback_submitted"
    }
)

print(response.json())

# List all reminders
response = requests.get("http://127.0.0.1:8000/reminders/")
print(response.json())
```

---

## Postman Collection

Import this JSON into Postman:

```json
{
  "info": {
    "name": "Scheduler Service",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create Reminder",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"entity_type\": \"interviewer\",\n  \"entity_id\": \"INT_100\",\n  \"event_type\": \"feedback_form\",\n  \"channel\": \"email\",\n  \"schedule_type\": \"recurring\",\n  \"interval_minutes\": 1,\n  \"stop_condition_type\": \"db_check\",\n  \"stop_condition_value\": \"feedback_submitted\"\n}"
        },
        "url": {"raw": "http://127.0.0.1:8000/reminders/"}
      }
    },
    {
      "name": "List Reminders",
      "request": {
        "method": "GET",
        "url": {"raw": "http://127.0.0.1:8000/reminders/"}
      }
    }
  ]
}
```