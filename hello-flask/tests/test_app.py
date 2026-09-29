from app.app import app


def client():
    app.config.update(TESTING=True)
    return app.test_client()


def test_index_returns_message_and_version():
    resp = client().get("/")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["message"] == "Hello from the Raspberry Pi"
    assert "version" in body


def test_healthz_is_ok():
    resp = client().get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}
