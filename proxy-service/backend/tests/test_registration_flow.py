from app.routers import auth as auth_router


def test_register_creates_user_and_returns_activation_key(client, monkeypatch):
    monkeypatch.setattr(
        auth_router.send_activation_email_task,
        "delay",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(auth_router.auth, "get_password_hash", lambda _password: "stub-hash")

    response = client.post(
        "/api/register",
        json={
            "email": "user@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["email"] == "user@example.com"
    assert payload["activation_key"]
    assert payload["is_active"] is True
