# app/models/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class FeedbackCreate(BaseModel):
    name: str
    email: EmailStr
    feedback_text: str
