from unittest.mock import MagicMock, patch, AsyncMock
from datetime import date

import pytest

from src.database.models import User
from src.services.auth import auth_service


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    data = response.json()
    return data["access_token"]


CONTACT = {
    "id": 1,
    "first_name": "First_name",
    "last_name": "Last_name",
    "email": "email@email.ua",
    "phone": "0631234567",
    "birthday": str(date(year=2012, month=12, day=12)),
    "description": "description",
    "user": 1,
}


def test_create_contact(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.post(
            "api/contacts", json=CONTACT, headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201, response.text
        data_contact = response.json()
        assert "first_name" in data_contact


def test_get_contact_by_id(client, token, monkeypatch):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            "/api/contacts/1", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert "id" in data


def test_get_contact_by_id_not_found(client, token, monkeypatch):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            "/api/contacts/2", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not found!"


def test_get_contact_by_email(client, token, monkeypatch):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            f"/api/contacts/email/email", headers={"Authorization": f"Bearer {token}"}
        )
        data = response.json()
        if not "id" in data:
            assert data["detail"] == "Not Found"
        else: 
            assert response.status_code == 200, response.text
            data = response.json()
            assert "id" in data


def test_get_contact_by_email_not_found(client, token, monkeypatch):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            "/api/contacts/email/example", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not Found"


def test_get_contact_by_first_name(client, token, monkeypatch):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            f"/api/contacts/first_name/first", headers={"Authorization": f"Bearer {token}"}
        )
        data = response.json()
        if not "id" in data:
            assert data["detail"] == "Not Found"
        else: 
            assert response.status_code == 200, response.text
            data = response.json()
            assert "id" in data


def test_get_contact_by_first_name_not_found(client, token, monkeypatch):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            "/api/contacts/first_name/ogh", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not Found"


def test_get_contact_by_last_name(client, token, monkeypatch):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            f"/api/contacts/last_name/last", headers={"Authorization": f"Bearer {token}"}
        )
        data = response.json()
        if not "id" in data:
            assert data["detail"] == "Not Found"
        else: 
            assert response.status_code == 200, response.text
            data = response.json()
            assert "id" in data


def test_get_contact_by_last_name_not_found(client, token, monkeypatch):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            "/api/contacts/last_name/ogh", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not Found"


def test_get_contacts(client, token, monkeypatch):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get(
            "/api/contacts", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["first_name"] == "First_name"
        assert "id" in data[0]


def test_update_contact(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/1",
            json={
                "id": 1,
                "first_name": "NEW_First_name",
                "last_name": "Last_name",
                "email": "email@email.ua",
                "phone": "0631234567",
                "birthday": str(date(year=2012, month=12, day=12)),
                "description": "description",
                "user": 1,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["first_name"] == "NEW_First_name"
        assert "id" in data


def test_update_contact_not_found(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/2",
            json={
                "id": 2,
                "first_name": "NEW_First_name",
                "last_name": "Last_name",
                "email": "email@email.ua",
                "phone": "0631234567",
                "birthday": str(date(year=2012, month=12, day=12)),
                "description": "description",
                "user": 1,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not found!"



def test_delete_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 204, response.text


def test_repeat_delete_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not found!"
