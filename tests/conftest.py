
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv


from main import app, get_db
from models import Base

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL") 

if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL is missing")

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
