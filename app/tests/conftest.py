import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database.database import Base, get_db_session
from app.main import app
import os
from dotenv import load_dotenv


load_dotenv()

# Test database URL
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/gql_test")

# Create test engine
engine = create_engine(TEST_DATABASE_URL)

# Create test SessionLocal
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after all tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():    
    # Create a new session for the test
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="session")
def get_app():
    # Override the get_db_session dependency
    def override_get_db_session():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db_session] = override_get_db_session
    return app


@pytest.fixture(scope="session")
def client(get_app):
    return TestClient(get_app)