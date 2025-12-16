from fastapi import FastAPI
from backend.core.config import settings
from backend.db.session import engine
from backend.db.base import Base
from backend.apis.v1 import route_auth, route_chat
from backend.services.tasks import start_scheduler, scheduler

# Create DB tables (Auto-migration)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# --- Life Cycle Events ---
@app.on_event("startup")
def startup_event():
    """Start the background task scheduler on app startup."""
    start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    """Shut down the scheduler when app stops."""
    scheduler.shutdown()

# --- Router Registration ---
app.include_router(route_auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(route_chat.router, prefix="/api/v1/chat", tags=["Chat"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "AI Chatbot Backend Running with Background Tasks"}