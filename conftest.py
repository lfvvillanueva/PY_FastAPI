from db import get_session
import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import StaticPool
from app.main import app

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url, 
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool
                       )

@pytest.fixture(name="session")
def session_fixture():
    from db import SQLModel
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_overrides():
        return session

    app.dependency_overrides[get_session] = get_session_overrides
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
