# this have database stuff
# 10:18
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

DB_URL = "sqlite:///./instagram_backend/db.sql"

engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()



from sqlalchemy import event

@event.listens_for(Session, "after_commit")
def after_commit(session):
    print("After commit event triggered")

@event.listens_for(Session, "before_commit")
def before_commit(session):
    print("Before commit event triggered")
