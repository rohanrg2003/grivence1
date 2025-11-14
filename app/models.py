# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True, nullable=False)
    email = Column(String(256), nullable=True)
    hashed_password = Column(String(256), nullable=False)

    grievances = relationship("Grievance", back_populates="user")

class Grievance(Base):
    __tablename__ = "grievances"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(256), default="Internet down")
    description = Column(Text)
    category = Column(String(64), default="Other")
    status = Column(String(32), default="submitted")
    attachment_path = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="grievances")
