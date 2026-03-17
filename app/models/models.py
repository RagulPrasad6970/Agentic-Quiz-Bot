from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    difficulty = Column(String)
    num_questions = Column(Integer)
    form_id = Column(String)
    form_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question_text = Column(String)
    options = Column(JSON)
    correct_answer = Column(String)
    explanation = Column(String)


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    quiz_id = Column(Integer)
    score = Column(Integer)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    email_sent = Column(Boolean, default=False)


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer)
    question_id = Column(Integer)
    user_answer = Column(String)
    is_correct = Column(Boolean)