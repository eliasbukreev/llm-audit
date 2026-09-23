import asyncio


def test_audit_start(client):
    r = client.post("/audit/start", json={"repo_url": "https://github.com/test/test"})
    assert r.status_code == 200
    data = r.json()
    assert "session_id" in data


def test_audit_start_invalid_url(client):
    r = client.post("/audit/start", json={"repo_url": "not-a-url"})
    assert r.status_code == 200
    assert "session_id" in r.json()


def test_audit_stream(client):
    r = client.post("/audit/start", json={"repo_url": "https://github.com/test/test"})
    session_id = r.json()["session_id"]
    import app.api.audit as audit_mod

    audit_mod.event_bus[session_id] = asyncio.Queue()
    audit_mod.event_bus[session_id].put_nowait({"step": "complete", "status": "done"})
    r = client.get(f"/audit/{session_id}/stream")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/event-stream")


def test_audit_results(client):
    r = client.post("/audit/start", json={"repo_url": "https://github.com/test/test"})
    session_id = r.json()["session_id"]
    r = client.get(f"/audit/{session_id}/results")
    assert r.status_code == 200
    assert "files" in r.json()
