
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from App.main import app
from App.config import settings
from App.database import get_db
from App.database import Base

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
     # delete and create tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def overrideget_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrideget_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "pwittoeck@gmail.com", "password": "Welkom01"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201   
    print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user