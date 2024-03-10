from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from pydantic import BaseModel

from db import Base


class UserAnswerTable(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True)
    is_good = Column(Integer)
    sentence = Column(String)
    recommended_foodtype = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def get_is_good(cls, session, is_good: int):
        return session.query(cls).filter(cls.is_good == is_good).all()


class UserAnswer(BaseModel):
    is_good: int
    sentence: str
    recommended_foodtype: str

    class Config:
        orm_mode = True
