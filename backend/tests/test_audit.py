def test_audit_start(client):
    r = client.post("/audit/start", json={"repo_url": "https://github.com/test/test"})
    assert r.status_code == 200
    data = r.json()
    assert "session_id" in data


def test_audit_start_invalid_url(client):
    r = client.post("/audit/start", json={"repo_url": "not-a-url"})
    assert r.status_code == 200


def test_audit_stream(client):
    r = client.get("/audit/placeholder/stream")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/event-stream")


def test_audit_results(client):
    r = client.get("/audit/placeholder/results")
    assert r.status_code == 200
    assert "files" in r.json()
