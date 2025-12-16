from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.db.session import SessionLocal
from backend.db.models.chat import ChatHistory

# Initialize the scheduler
scheduler = BackgroundScheduler()

def delete_old_chat_history():
    """
    Deletes chat history older than 30 days.
    Designed to run as a scheduled background task.
    """
    db: Session = SessionLocal()
    try:
        # Calculate the date 30 days ago from now
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        # Delete records older than the cutoff date
        deleted_count = db.query(ChatHistory).filter(ChatHistory.timestamp < cutoff_date).delete()
        db.commit()
        
        print(f"[Background Task] Maintenance complete. Deleted {deleted_count} old chat records.")
    except Exception as e:
        print(f"[Background Task] Error cleaning up chat history: {e}")
    finally:
        db.close()

def start_scheduler():
    """Configures and starts the background scheduler."""
    # Add job to run daily (interval of 24 hours)
    scheduler.add_job(delete_old_chat_history, 'interval', days=1)
    scheduler.start()
    
    
def send_verification_email(email: str):
    """Mock background task to send email."""
    print(f"📧 [Background Task] Sending verification email to {email}...")
    # In real app: integration with SMTP or SendGrid would go here.