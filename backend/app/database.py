import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime

from app.config import settings


def get_conn():
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    schema_path = settings.schema_path
    with open(schema_path) as f:
        schema = f.read()
    with get_conn() as conn:
        conn.executescript(schema)


@contextmanager
def session_scope():
    conn = get_conn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def create_session(
    repo_url: str,
    repo_name: str | None = None,
    repo_path: str | None = None,
) -> str:
    session_id = uuid.uuid4().hex
    now = datetime.now().isoformat()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO sessions "
            "(id, repo_url, repo_name, repo_path, status, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (session_id, repo_url, repo_name, repo_path, "running", now, now),
        )
    return session_id


def get_session(session_id: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
        if row is None:
            return None
        return dict(row)


def update_session(session_id: str, **kwargs) -> None:
    if not kwargs:
        return
    set_clause = ", ".join(f"{k} = ?" for k in kwargs)
    kwargs["updated_at"] = datetime.now().isoformat()
    kwargs["session_id"] = session_id
    with get_conn() as conn:
        conn.execute(
            f"UPDATE sessions SET {set_clause}, updated_at = ? WHERE id = ?",
            list(kwargs.values()),
        )


def create_step(session_id: str, step_id: str, step_name: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO steps (id, session_id, status, started_at) "
            "VALUES (?, ?, ?, datetime('now'))",
            (step_id, session_id, "pending"),
        )


def update_step(
    session_id: str,
    step_id: str,
    status: str,
    result_path: str | None = None,
    error: str | None = None,
) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE steps SET status = ?, result_path = ?, error = ?, "
            "finished_at = datetime('now') WHERE session_id = ? AND id = ?",
            (status, result_path, error, session_id, step_id),
        )
