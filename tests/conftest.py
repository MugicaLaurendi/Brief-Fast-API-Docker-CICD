import pytest
from sqlmodel import SQLModel, create_engine, Session, select
from fastapi.testclient import TestClient
from main import app
from app.database_connection import get_session
from app.security import get_password_hash
from app.models import Clients, Roles

# Créer une base de données SQLite en mémoire pour les tests
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

# Fixture pour initialiser la DB avant chaque test
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Initialisation des rôles
        if not session.exec(select(Roles).where(Roles.nom == "admin")).first():
            session.add(Roles(id=1, nom="admin", permission="all"))
        if not session.exec(select(Roles).where(Roles.nom == "client")).first():
            session.add(Roles(id=3,nom="client", permission="read"))
            session.commit()
        yield session
    SQLModel.metadata.drop_all(engine)

# Fixture pour remplacer la session réelle par la session de test
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_test_session():
        return session
    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as test_client:
        yield test_client


# Fixture pour un client authentifié (admin)
@pytest.fixture(name="auth_client")
def auth_client_fixture(client: TestClient, session: Session):
    # Récupérer le rôle admin
    admin_role = session.exec(select(Roles).where(Roles.nom == "admin")).first()

    # Créer l'utilisateur admin si inexistant
    admin_user = session.exec(select(Clients).where(Clients.username == "testadmin")).first()
    if not admin_user:
        admin_user = Clients(
            nom="Admin",
            prenom="Test",
            adresse="1 rue admin",
            telephone="0600000000",
            email="testadmin@example.com",
            username="testadmin",
            password=get_password_hash("secret123"),
            role_id=admin_role.id
        )
        session.add(admin_user)
        session.commit()
        session.refresh(admin_user)

    # Connexion via l’endpoint d’auth pour récupérer le token
    response = client.post(
        "/auth/token",
        data={"username": "testadmin", "password": "secret123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]

     # Mettre à jour le header Authorization
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client