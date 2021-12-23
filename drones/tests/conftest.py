from typing import Generator

import pytest
from app.database import SessionLocal
from app.main import app
from app.settings import get_settings
from fastapi.testclient import TestClient

settings = get_settings()


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
