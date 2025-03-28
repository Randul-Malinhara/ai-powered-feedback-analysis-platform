from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import AZURE_SQL_CONN_STR
from app.models.feedback import Base, Feedback

# Set up SQLAlchemy engine and session
engine = create_engine(AZURE_SQL_CONN_STR, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(engine)


def save_feedback(feedback: Feedback):
    """
    Save a feedback record to the database.
    """
    session = SessionLocal()
    try:
        session.add(feedback)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error saving feedback: {e}")
    finally:
        session.close()


def get_all_feedbacks():
    """
    Retrieve all feedback records.
    """
    session = SessionLocal()
    try:
        feedbacks = session.query(Feedback).order_by(Feedback.created_at.desc()).all()
        return feedbacks
    except Exception as e:
        print(f"Error retrieving feedbacks: {e}")
        return []
    finally:
        session.close()
