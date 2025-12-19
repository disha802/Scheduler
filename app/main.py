from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db, close_db
from app.routes.reminders import router as reminder_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title="Reminder Scheduler",
    description="Generic reminder engine with Tortoise ORM",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware (for UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reminder_router, prefix="/reminders", tags=["Reminders"])


@app.get("/")
def health():
    return {
        "status": "Scheduler API running",
        "version": "2.0.0",
        "orm": "Tortoise ORM"
    }