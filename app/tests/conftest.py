import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database.database import Base
from app.main import app
from app.models.user import User
import os
from dotenv import load_dotenv

load_dotenv()


# Test database URL
SQLALCHEMY_TEST_DATABASE_URL = (
    f"{os.getenv('DB_CONNECTION')}://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

# Create test engine
test_engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

# Create test SessionLocal
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Create all tables
    Base.metadata.create_all(bind=test_engine)

    

@pytest.fixture(scope="function")
def db_session():    
    # Create a new session for the test
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client():
    return TestClient(app)