from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Update with env vars or pydantic settings in production
# Update with env vars or pydantic settings in production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pnas.db")

# Fix for Supabase/Render providing postgres:// instead of postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session
