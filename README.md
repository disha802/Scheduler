# Reminder Scheduler Service

A generic, condition-driven reminder orchestration system built using **FastAPI** and **PostgreSQL**. This service replaces rigid cron-based workflows with a flexible, state-aware scheduler that can be reused across domains such as HR, SaaS, and internal operations.

---

## Tech Stack

* **Python**: 3.12
* **Backend Framework**: FastAPI
* **Database**: PostgreSQL (Managed / Cloud)
* **ORM**: SQLAlchemy
* **Server**: Uvicorn

---

## Project Structure

```text
scheduler_app/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes/
│   │   └── reminders.py
│   ├── scheduler/
│   │   ├── worker.py
│   │   └── condition_checker.py
│   └── notifications/
│       └── email.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repo-url>
cd scheduler_app
```

### 2. Create and activate a virtual environment (Python 3.12)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>/<dbname>?sslmode=require
```

---

## Running the Application

```bash
uvicorn app.main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Notes

* This project is designed to be **cron-free** and condition-driven
* Scheduler logic runs as a background worker
* Notification channels are pluggable and extensible

---

## Future Enhancements

* Celery / Redis integration
* Role-based access control
* Webhook-based stop conditions
* Metrics and observability

---

# .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]

# Virtual environment
venv/
.env

# IDEs
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
```

---

# requirements.txt

```text
fastapi==0.110.0
uvicorn==0.29.0
sqlalchemy==2.0.29
psycopg2-binary==2.9.9
python-dotenv==1.0.1
pydantic==2.6.4
```

---

## Compatibility

All dependencies are pinned and verified to be compatible with **Python 3.12**.
