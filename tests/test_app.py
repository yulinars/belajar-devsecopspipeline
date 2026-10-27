"""Pengujian unit untuk aplikasi Flask."""

import pytest

from app import app, init_db


@pytest.fixture(name="client")
def client_fixture(tmp_path, monkeypatch):
    """Menyiapkan klien uji dengan database sementara."""
    monkeypatch.chdir(tmp_path)
    init_db()
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    """Endpoint health mengembalikan status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_about(client):
    """Endpoint about dapat diakses."""
    assert client.get("/about").status_code == 200


def test_login_berhasil(client):
    """Kredensial benar berhasil login."""
    response = client.post(
        "/", data={"username": "admin", "password": "supersecret"}
    )
    assert "Login Berhasil" in response.get_data(as_text=True)


def test_login_gagal(client):
    """Kredensial salah ditolak."""
    response = client.post("/", data={"username": "admin", "password": "salah"})
    assert "Login Gagal" in response.get_data(as_text=True)


def test_sql_injection_ditolak(client):
    """Payload SQL Injection tidak boleh berhasil login."""
    response = client.post(
        "/", data={"username": "' OR '1'='1' --", "password": "apa saja"}
    )
    assert "Login Gagal" in response.get_data(as_text=True)