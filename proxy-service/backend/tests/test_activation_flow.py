from datetime import datetime, timedelta

from app import models


def test_activation_assigns_vm_and_consumes_key(client, db_session):
    user = models.User(
        email="desktop@example.com",
        password_hash="stub-hash",
        activation_key="desktop-key",
        activation_key_expires=datetime.utcnow() + timedelta(days=1),
    )
    vm = models.VirtualMachine(
        name="proxy-1",
        host="127.0.0.1",
        port=1080,
        protocol="socks5",
        is_active=True,
    )
    db_session.add_all([user, vm])
    db_session.commit()

    response = client.post("/api/activate-key", json={"key": "desktop-key"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["host"] == "127.0.0.1"
    assert payload["port"] == 1080
    assert payload["protocol"] == "socks5"
    assert payload["status"] == "connected"
    assert payload["access_token"]

    db_session.refresh(user)
    db_session.refresh(vm)
    assert user.activation_key is None
    assert user.activation_key_expires is None
    assert vm.current_user_id == user.id


def test_websocket_reports_current_connection_status(client, db_session):
    user = models.User(
        email="ws@example.com",
        password_hash="stub-hash",
        activation_key="ws-key",
        activation_key_expires=datetime.utcnow() + timedelta(days=1),
    )
    vm = models.VirtualMachine(
        name="proxy-ws",
        host="127.0.0.1",
        port=8080,
        protocol="http",
        is_active=True,
    )
    db_session.add_all([user, vm])
    db_session.commit()

    response = client.post("/api/activate-key", json={"key": "ws-key"})
    token = response.json()["access_token"]

    with client.websocket_connect(f"/ws/status?token={token}") as websocket:
        payload = websocket.receive_json()

    assert payload["status"] == "connected"
    assert payload["vm"]["name"] == "proxy-ws"
    assert payload["vm"]["protocol"] == "http"


def test_disconnect_releases_vm(client, db_session):
    user = models.User(
        email="disconnect@example.com",
        password_hash="stub-hash",
        activation_key="disconnect-key",
        activation_key_expires=datetime.utcnow() + timedelta(days=1),
    )
    vm = models.VirtualMachine(
        name="proxy-2",
        host="127.0.0.1",
        port=3128,
        protocol="https",
        is_active=True,
    )
    db_session.add_all([user, vm])
    db_session.commit()

    activation_response = client.post("/api/activate-key", json={"key": "disconnect-key"})
    token = activation_response.json()["access_token"]

    response = client.post(
        "/api/disconnect",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "disconnected"

    db_session.refresh(vm)
    assert vm.current_user_id is None
