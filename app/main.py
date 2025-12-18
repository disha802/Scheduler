from fastapi import FastAPI
from app.routes.reminders import router as reminder_router

app = FastAPI(title="Reminder Scheduler")

app.include_router(reminder_router, prefix="/reminders", tags=["Reminders"])

@app.get("/")
def health():
    return {"status": "Scheduler API running"}
