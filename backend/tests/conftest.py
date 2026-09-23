import tempfile

import pytest


@pytest.fixture(autouse=True)
def _temp_db(monkeypatch):
    fd, path = tempfile.mkstemp(suffix=".db")
    import os

    os.close(fd)
    monkeypatch.setattr("app.config.settings.db_path", path)
    from app.database import init_db

    init_db()
    yield


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as c:
        yield c
