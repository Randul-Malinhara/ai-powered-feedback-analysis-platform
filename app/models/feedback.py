from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    feedback_text = Column(Text)
    sentiment = Column(String(20))
    confidence_scores = Column(Text)  # storing as text (e.g., JSON string)
    key_phrases = Column(Text)
    attachment_url = Column(String(255), nullable=True)
    created_at = Column(DateTime)
    
    def __repr__(self):
        return f"<Feedback(id={self.id}, name={self.name}, sentiment={self.sentiment})>"
