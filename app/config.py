import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Supabase PostgreSQL connection
DATABASE_URL = (
    "postgresql+psycopg2://postgres:Fasthub@2025!@db.hsedfoiodcrxgsnzmlnb.supabase.co:5432/postgres"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
Base = declarative_base()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Application settings
class Settings:
    SECRET_KEY = os.getenv("SESSION_SECRET", "your-secret-key-here")
    MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY", "")
    MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET", "")
    MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE", "")
    MPESA_PASSKEY = os.getenv("MPESA_PASSKEY", "")
    MPESA_SANDBOX_URL = "https://sandbox.safaricom.co.ke"
    MPESA_PRODUCTION_URL = "https://api.safaricom.co.ke"
    MPESA_ENVIRONMENT = os.getenv("MPESA_ENVIRONMENT", "sandbox")

settings = Settings()
