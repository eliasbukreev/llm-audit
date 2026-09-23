import os
import sqlite3
from contextlib import contextmanager
from app.config import DB_PATH


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    schema_path = os.path.join(os.path.dirname(__file__), "db", "schema.sql")
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
