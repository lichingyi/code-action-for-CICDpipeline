import pytest
from app import create_app


def test_root_ok(monkeypatch):
    monkeypatch.setattr("socket.gethostbyname", lambda _: "127.0.0.1")
    app = create_app()
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.data.decode() == "127.0.0.1"


def test_root_error(monkeypatch):
    def boom(_):
        raise OSError("boom")
    monkeypatch.setattr("socket.gethostbyname", boom)
    app = create_app()
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 500
    assert b"Internal Server Error" in resp.data


def test_healthz():
    app = create_app()
    client = app.test_client()
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json["status"] == "ok"


def test_version_default(monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    app = create_app()
    client = app.test_client()
    resp = client.get("/version")
    assert resp.status_code == 200
    assert resp.json["version"] == "0.0.0"


def test_whoami_ok(monkeypatch):
    monkeypatch.setattr("socket.gethostname", lambda: "myhost")
    monkeypatch.setattr("socket.gethostbyname", lambda _: "10.0.0.5")
    app = create_app()
    client = app.test_client()
    resp = client.get("/whoami")
    assert resp.status_code == 200
    assert resp.json["hostname"] == "myhost"
    assert resp.json["ip"] == "10.0.0.5"