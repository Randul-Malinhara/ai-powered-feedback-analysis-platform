from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    feedback_text = Column(Text, nullable=False)
    sentiment = Column(String(20))
    confidence_scores = Column(Text)  # Stored as JSON text
    key_phrases = Column(Text)
    attachment_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Feedback(id={self.id}, name={self.name}, sentiment={self.sentiment})>"
