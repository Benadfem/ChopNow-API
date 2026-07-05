import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Fetch your database credentials securely from your environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Benadfem")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "chopnow_db")

# 2. Construct the standard PostgreSQL connection URL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# 3. Create the SQLAlchemy Engine
engine = create_engine(DATABASE_URL)

# 4. Create a SessionLocal class. Each instance of this class will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Create a Base class. Our database models (Tables) will inherit from this later.
Base = declarative_base()

# Helper dependency to handle opening and closing database sessions automatically
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()