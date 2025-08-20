from app.security import create_refresh_token
from tests.test_clients import create_user
from uuid import uuid4


# -----------------------------
# Tests d'enregistrement
# -----------------------------

def test_register_client_success(client):
    # Générer un username unique pour éviter les conflits
    username = f"user_{uuid4().hex[:6]}"
    email = f"{username}@example.com"

    payload = {
        "nom": "Test",
        "prenom": "User",
        "adresse": "123 rue test",
        "telephone": "0101010101",
        "email": email,
        "username": username,
        "password": "password123"
    }

    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Client enregistré avec succès"}


def test_register_existing_username(client, session):
    create_user(session, "existing")

    payload = {
        "nom": "Test",
        "prenom": "User",
        "adresse": "123 rue test",
        "telephone": "0101010101",
        "email": "test2@example.com",
        "username": "existing",
        "password": "password123"
    }

    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Nom d'utilisateur déjà utilisé"


# -----------------------------
# Tests de connexion
# -----------------------------
def test_login_success(client, session):
    create_user(session, "testuser")

    response = client.post("/auth/token", data={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, session):
    create_user(session, "testuser2")

    response = client.post("/auth/token", data={
        "username": "testuser2",
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/auth/token", data={
        "username": "notexists",
        "password": "whatever"
    })
    assert response.status_code == 401


# -----------------------------
# Tests refresh token
# -----------------------------
def test_refresh_token_success(client, session):
    user = create_user(session, "testrefresh")

    refresh_token = create_refresh_token({"sub": user.username})
    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid(client):
    response = client.post("/auth/refresh", json={"refresh_token": "faketoken"})
    assert response.status_code == 401
