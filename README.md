# Scheduler Service (Generic Reminder Engine)

## Overview

This project implements a **generic, database-driven scheduler** that can be integrated into any system requiring reminders, follow-ups, or repeated actions until a condition is satisfied.

Unlike traditional cron-based systems, this scheduler is **stateful, idempotent, and condition-aware**. Each reminder is treated as a first-class entity with its own lifecycle, schedule, and stop condition.

---

## Key Features

* ✅ Generic reminder model (usable across domains)
* ✅ Idempotent API (safe against duplicate requests)
* ✅ Time-based scheduling without cron jobs
* ✅ Database-driven stop conditions
* ✅ Automatic reminder completion
* ✅ Cloud-ready PostgreSQL backend
* ✅ FastAPI-based REST APIs

---

## Core Use Cases

Examples of supported use cases:

* Interview reminder emails to candidates
* Interviewer feedback reminder until form is submitted
* Periodic follow-ups until approval/action is completed
* SLA breach alerts
* Compliance or audit reminders

The system is **not limited** to emails — any notification channel can be plugged in.

---

## Architecture Overview

### High-Level Components

1. **FastAPI Application**

   * Exposes APIs to create and manage reminders

2. **PostgreSQL Database**

   * Stores reminder jobs and stop-condition flags

3. **Scheduler Worker**

   * Periodically polls the database
   * Evaluates due reminders
   * Triggers reminders
   * Stops reminders when conditions are met

---

## Data Model

### ReminderJob (`reminder_jobs` table)

Each reminder represents a scheduled job with the following attributes:

* Entity metadata (`entity_type`, `entity_id`)
* Event metadata (`event_type`, `channel`)
* Scheduling details (`schedule_type`, `interval_minutes`, `next_run_at`)
* Stop condition (`stop_condition_type`, `stop_condition_value`)
* Lifecycle status (`ACTIVE`, `PAUSED`, `COMPLETED`)

### StatusFlag (`status_flags` table)

Represents external business conditions that control reminder termination.

* `key`: Condition identifier (e.g., `feedback_submitted`)
* `value`: Boolean flag indicating completion

---

## Reminder Lifecycle

1. Reminder is created via API
2. Scheduler periodically checks for due reminders
3. Reminder is triggered when `next_run_at <= now`
4. Stop condition is evaluated
5. If condition met → reminder is marked `COMPLETED`
6. If not → reminder is rescheduled

---

## Idempotency

The system enforces **API-level idempotency**.

Only one ACTIVE reminder is allowed per:

* `entity_type`
* `entity_id`
* `event_type`

Duplicate API requests return the existing reminder instead of creating new ones.

---

## Stop Condition Logic

Stop conditions are evaluated dynamically during scheduler execution.

Currently supported:

* `db_check`: Checks a value in the `status_flags` table

This design allows easy extension to:

* API-based checks
* Webhook-based conditions
* Time-bound or retry-count-based stopping

---

## How to Run the Project

### 1. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```
DATABASE_URL=<your_postgres_connection_string>
```

### 4. Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

Swagger UI will be available at:

```
http://127.0.0.1:8000/docs
```

### 5. Start Scheduler Worker

In a separate terminal:

```bash
python -m app.scheduler.worker
```

---

## Example API Request

### Create Reminder

```json
{
  "entity_type": "interviewer",
  "entity_id": "INT_100",
  "event_type": "feedback_form",
  "channel": "email",
  "schedule_type": "recurring",
  "interval_minutes": 60,
  "stop_condition_type": "db_check",
  "stop_condition_value": "feedback_submitted"
}
```

---

## Testing Stop Conditions

1. Insert flag:

```sql
INSERT INTO status_flags (key, value)
VALUES ('feedback_submitted', false);
```

2. Scheduler triggers reminders periodically
3. Update flag:

```sql
UPDATE status_flags
SET value = true
WHERE key = 'feedback_submitted';
```

4. Scheduler auto-completes reminder

---

## Why This Design

* Avoids brittle cron jobs
* Centralized control via database
* Safe against retries and duplicates
* Easily extensible
* Production-aligned architecture

---

## Future Enhancements

* Pause / Resume reminder APIs
* Email/SMS/Slack adapters
* Retry limits and escalation policies
* Admin dashboard
* Alembic migrations

---

## Status

✅ Core functionality complete

This project is **demo-ready and production-shaped**.
