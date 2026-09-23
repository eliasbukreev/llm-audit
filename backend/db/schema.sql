CREATE TABLE IF NOT EXISTS sessions (
    id          TEXT PRIMARY KEY,
    repo_url    TEXT NOT NULL,
    repo_name   TEXT,
    repo_path   TEXT,
    results_dir TEXT,
    status      TEXT DEFAULT 'idle',
    error_msg   TEXT,
    created_at  TEXT DEFAULT (datetime('now')),
    updated_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS steps (
    id          TEXT PRIMARY KEY,
    session_id  TEXT REFERENCES sessions(id),
    status      TEXT DEFAULT 'pending',
    result_path TEXT,
    error       TEXT,
    started_at  TEXT,
    finished_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_steps_session ON steps(session_id);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);
