#  app/db/session.py

from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

#  Khoi tao Engine ket noi co so du lieu
engine = create_engine(
    settings.DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False}
)

# Khoi tao cac bang trong co so du lieu
def init_db():
    from app.db import models 
    SQLModel.metadata.create_all(engine)

# Dependency cho FastAPI
def get_session():
    with Session(engine) as session:
        yield session

# Context Manager cho Celery Worker
def SessionLocal():
    return Session(engine)