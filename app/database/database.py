from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Get database connection details from environment variables
DB_CONNECTION = os.getenv("DB_CONNECTION", "postgresql")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "postgres")

# Construct database URL
# example: postgresql://user:password@host:port/database
SQLALCHEMY_DATABASE_URL = f"{DB_CONNECTION}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session maker bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for database models
Base = declarative_base()


# Dependency function to get a database session
def get_db():  # noqa
    return SessionLocal()
