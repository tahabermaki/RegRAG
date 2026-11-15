"""Tests de la phase 0 : l'API démarre et signale proprement une dépendance en panne."""

from fastapi.testclient import TestClient

from regrag.api.main import app

client = TestClient(app)


def test_live_is_always_ok():
    resp = client.get("/health/live")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_request_id_is_returned():
    resp = client.get("/health/live", headers={"X-Request-ID": "abc123"})
    assert resp.headers["X-Request-ID"] == "abc123"


def test_health_degrades_instead_of_crashing(monkeypatch):
    """Sans Qdrant/Postgres/Redis joignables, /health répond 503 'degraded', sans planter."""
    from regrag.api import main

    monkeypatch.setattr(main.settings, "qdrant_url", "http://127.0.0.1:1")
    monkeypatch.setattr(main.settings, "postgres_dsn", "postgresql://x:x@127.0.0.1:1/x")
    monkeypatch.setattr(main.settings, "redis_url", "redis://127.0.0.1:1/0")
    resp = client.get("/health")
    body = resp.json()
    assert resp.status_code == 503
    assert body["status"] == "degraded"
    assert {d["name"] for d in body["dependencies"]} == {"qdrant", "postgres", "redis"}
    assert all(d["status"] == "down" for d in body["dependencies"])


def test_ask_not_implemented_yet():
    resp = client.post("/ask", json={"question": "Que dit l'article 50 ?"})
    assert resp.status_code == 501
