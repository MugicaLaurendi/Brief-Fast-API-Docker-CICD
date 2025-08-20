from application.main import app
from sqlmodel import select, Session
from application.app.models import Clients, Roles
from application.app.security import get_password_hash
from fastapi.testclient import TestClient
from application.app.routers.clients import get_current_user

# ---------- HELPERS ----------
def create_user(session, username, role_id=1, email=None):
    """Ajoute un utilisateur directement en DB"""
    user = Clients(
        nom="Test",
        prenom="User",
        adresse="123 rue test",
        telephone="0600000000",
        email=email or f"{username}@example.com",
        username=username,
        password=get_password_hash("password123"),
        role_id=role_id,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# ---------- TESTS CREATION ----------
def test_create_client_ok(auth_client: TestClient, session):
    # Vérifier si le rôle "user" existe déjà
    role = session.exec(select(Roles).where(Roles.nom == "user")).first()
    if not role:
        role = Roles(nom="user", permission="read")
        session.add(role)
        session.commit()
        session.refresh(role)

     # Créer un utilisateur de test directement en DB si nécessaire
    _ = create_user(session, username="test_user", role_id=role.id)

    data = {
        "nom": "Smith",
        "prenom": "Laura",
        "adresse": "1 rue de Paris",
        "telephone": "0600000000",
        "email": "Laura@example.com",
        "username": "LauraSmith",
        "password": "secret123",
        "role_id": role.id  # Associer le client au rôle existant
    }

    response = auth_client.post("/clients/", json=data)
    assert response.status_code == 200


# ---------- TESTS LECTURE ----------
def test_read_client_not_found(auth_client: TestClient):
    response = auth_client.get("/clients/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Client non trouvé"

def test_read_client_ok(auth_client: TestClient, session):
    user = create_user(session, "user1")
    response = auth_client.get(f"/clients/{user.id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == user.id
    assert body["username"] == "user1"

def test_read_clients_list(auth_client: TestClient, session):
    create_user(session, "user2")
    create_user(session, "user3")
    response = auth_client.get("/clients/")
    assert response.status_code == 200
    body = response.json()
    assert len(body) >= 2

def test_get_my_profile(auth_client: TestClient, session):
    # Créer un utilisateur de test
    user = create_user(session, "meuser")

    # Override current_user pour simuler l'utilisateur connecté
    app.dependency_overrides[get_current_user] = lambda: user

    response = auth_client.get("/clients/users/me")
    assert response.status_code == 200
    body = response.json()
    
    # Vérifier que les informations correspondent à l'utilisateur connecté
    assert body["id"] == user.id
    assert body["username"] == user.username
    assert body["email"] == user.email


def test_read_clients_forbidden(session):
    # Créer un rôle "guest" ou autre rôle non autorisé
    role_guest = session.exec(select(Roles).where(Roles.nom == "guest")).first()
    if not role_guest:
        role_guest = Roles(nom="guest", permission="read")
        session.add(role_guest)
        session.commit()
        session.refresh(role_guest)

    # Créer un utilisateur avec ce rôle
    guest_user = create_user(session, "guestuser", role_id=role_guest.id)

    # Override current_user pour qu'il soit cet utilisateur
    
    app.dependency_overrides[get_current_user] = lambda: guest_user

    client = TestClient(app)
    response = client.get("/clients/")  # Endpoint protégé par require_role([1,2])
    assert response.status_code == 403
    assert response.json()["detail"] == "Accès interdit"


# ---------- TESTS UPDATE ----------
def test_update_client_self(auth_client: TestClient, session):
    user = create_user(session, "selfuser")
    update_data = {"adresse": "Nouvelle adresse"}

    # Override current_user
    app.dependency_overrides[get_current_user] = lambda: user

    response = auth_client.put(f"/clients/{user.id}", json=update_data)
    assert response.status_code == 200
    body = response.json()
    assert body["adresse"] == "Nouvelle adresse"

def test_update_client_forbidden(client: TestClient, session):
   
    user1 = create_user(session, "userA", role_id=3)
    user2 = create_user(session, "userB", role_id=3)

    app.dependency_overrides[get_current_user] = lambda: user1

    response = client.put(f"/clients/{user2.id}", json={"prenom": "Hack"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Accès refusé"

# ---------- TESTS DELETE ----------
def test_delete_client_self(client: TestClient, session):
    user = create_user(session, "deluser")

    app.dependency_overrides[get_current_user] = lambda: user

    response = client.delete(f"/clients/{user.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Client supprimé avec succès"

def test_delete_other_client_forbidden(client: TestClient, session: Session):
    # Créer deux utilisateurs avec ton helper
    user1 = create_user(session, "user1", role_id=3)
    user2 = create_user(session, "user2", role_id=3)

    # Override current_user pour simuler la connexion de user1
    app.dependency_overrides[get_current_user] = lambda: user1

    # Appel DELETE
    response = client.delete(f"/clients/{user2.id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Accès refusé"

    # Nettoyage de l’override
    app.dependency_overrides.pop(get_current_user, None)


