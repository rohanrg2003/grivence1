from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash, verify_password

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_grievance(db: Session, user_id: int, grievance: schemas.GrievanceCreate, category: str = None, attachment_path: str = None):
    db_g = models.Grievance(user_id=user_id, title=grievance.title, description=grievance.description, category=category, attachment_path=attachment_path)
    db.add(db_g)
    db.commit()
    db.refresh(db_g)
    return db_g

def get_grievance(db: Session, grievance_id: int):
    return db.query(models.Grievance).filter(models.Grievance.id == grievance_id).first()

def list_grievances_for_user(db: Session, user_id: int, skip=0, limit=100):
    return db.query(models.Grievance).filter(models.Grievance.user_id == user_id).offset(skip).limit(limit).all()
