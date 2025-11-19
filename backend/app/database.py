import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
db_file = os.environ.get("DATABASE_FILE", os.path.join(BASE_DIR, "test.db"))
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{db_file}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
