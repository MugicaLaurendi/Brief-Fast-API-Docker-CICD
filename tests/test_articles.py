from main import app
from sqlmodel import select, Session
from app.models import Clients, Roles, Articles
from app.security import get_password_hash
from fastapi.testclient import TestClient
from app.routers.clients import get_current_user


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
def test_create_article_ok(auth_client: TestClient, session):
    # S'assurer que le rôle "admin" existe (et récupérer son id)
    role = session.exec(select(Roles).where(Roles.nom == "user")).first()
    if not role:
        role = Roles(nom="user", permission="read")
        session.add(role)
        session.commit()
        session.refresh(role)

    # Créer un utilisateur admin en DB si besoin (pour que auth_client soit autorisé)
    _ = create_user(session, username="test_user", role_id=role.id)

    # Données d'article à créer
    data = {
        "nom": "Café",
        "prix": 5.25,
        "categorie": "Plat",
        "description": "Accord six terrain français.",
        "stock": 39
    }

    # Appel API
    response = auth_client.post("/articles/", json=data)

    # Vérifs
    assert response.status_code == 201


# ---------- TESTS LECTURE ----------
def test_read_article_not_found(auth_client: TestClient, session):
    response = auth_client.get("/articles/111111111111")
    assert response.status_code == 404
    assert response.json()["detail"] == "Article non trouvé"

def test_read_article_ok(auth_client: TestClient, session):
    # Création d’un article en DB
    article = Articles(
        nom="Café",
        prix=5.25,
        categorie="Plat",
        description="Accord six terrain français.",
        stock=39
    )
    session.add(article)
    session.commit()
    session.refresh(article)

    # Requête GET /articles/{id}
    response = auth_client.get(f"/articles/{article.id}")

    # Vérifs
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == article.id
    assert body["nom"] == "Café"
    assert float(body["prix"]) == 5.25
    assert body["categorie"] == "Plat"
    assert body["description"] == "Accord six terrain français."
    assert body["stock"] == 39


def test_read_articles_list(auth_client: TestClient, session):
    # Insérer des articles en DB
    article1 = Articles(
        nom="Café",
        prix=5.25,
        categorie="Plat",
        description="Accord six terrain français.",
        stock=39
    )
    article2 = Articles(
        nom="Thé",
        prix=3.10,
        categorie="Boisson",
        description="Infusion de qualité.",
        stock=50
    )
    session.add(article1)
    session.add(article2)
    session.commit()

    # Requête GET /articles/
    response = auth_client.get("/articles/")

    # Vérifs
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 2


def test_read_articles_forbidden(session):
    # Créer un rôle "guest" (non autorisé)
    role_guest = session.exec(select(Roles).where(Roles.nom == "guest")).first()
    if not role_guest:
        role_guest = Roles(nom="guest", permission="read")
        session.add(role_guest)
        session.commit()
        session.refresh(role_guest)

    # Créer un utilisateur avec ce rôle
    guest_user = create_user(session, "guestuser", role_id=role_guest.id)

    # Override current_user pour simuler un utilisateur connecté "guest"
    app.dependency_overrides[get_current_user] = lambda: guest_user

    client = TestClient(app)
    response = client.get("/articles/")  # Endpoint protégé par require_role([1])

    # Vérifs
    assert response.status_code == 403
    assert response.json()["detail"] == "Accès interdit"

    # Nettoyer les overrides
    app.dependency_overrides.clear()


# ---------- TESTS UPDATE ----------
def test_update_article_ok(auth_client: TestClient, session):
    # S'assurer d'avoir un rôle admin (id=1 attendu par require_role([1]))
    role_admin = session.get(Roles, 1)
    if not role_admin:
        role_admin = Roles(id=1, nom="admin", permission="all")
        session.add(role_admin)
        session.commit()
        session.refresh(role_admin)

    # Créer un utilisateur admin et override le current_user
    admin_user = create_user(session, "admin_update", role_id=1)
    app.dependency_overrides[get_current_user] = lambda: admin_user

    # Créer un article en DB
    art = Articles(
        nom="Café",
        prix=5.25,
        categorie="Plat",
        description="Accord six terrain français.",
        stock=39
    )
    session.add(art)
    session.commit()
    session.refresh(art)

    # Données de mise à jour (PUT)
    update_data = {
        "nom": "Café BIO",
        "prix": 5.90,
        "categorie": "Boisson",
        "description": "Arabica bio torréfié.",
        "stock": 45
    }

    # Appel API
    resp = auth_client.put(f"/articles/{art.id}", json=update_data)
    assert resp.status_code == 200
    body = resp.json()

    # Vérifs
    assert body["id"] == art.id
    assert body["nom"] == "Café BIO"
    assert float(body["prix"]) == 5.90
    assert body["categorie"] == "Boisson"
    assert body["description"] == "Arabica bio torréfié."
    assert body["stock"] == 45

    # Cleanup override
    app.dependency_overrides.clear()


def test_update_article_forbidden(client: TestClient, session):
    # Créer un rôle "guest" (non autorisé)
    role_guest = session.exec(select(Roles).where(Roles.nom == "guest")).first()
    if not role_guest:
        role_guest = Roles(nom="guest", permission="read")
        session.add(role_guest)
        session.commit()
        session.refresh(role_guest)

    # Créer un utilisateur guest
    guest_user = create_user(session, "guest_user", role_id=role_guest.id)

    # Créer un article en DB
    art = Articles(
        nom="Café",
        prix=5.25,
        categorie="Plat",
        description="Accord six terrain français.",
        stock=39,
    )
    session.add(art)
    session.commit()
    session.refresh(art)

    # Simuler que le user connecté = guest_user
    app.dependency_overrides[get_current_user] = lambda: guest_user

    # Tentative de modification
    response = client.put(f"/articles/{art.id}", json={"nom": "Hacké"})

    assert response.status_code == 403
    assert response.json()["detail"] == "Accès interdit"

    # Cleanup
    app.dependency_overrides.clear()


# ---------- TESTS DELETE ----------
def test_delete_article_ok(client: TestClient, session):
    role_admin = session.get(Roles, 1) or Roles(id=1, nom="admin", permission="all")
    session.add(role_admin); session.commit(); session.refresh(role_admin)

    admin_user = create_user(session, "deladmin", role_id=1)
    app.dependency_overrides[get_current_user] = lambda: admin_user

    art = Articles(
            nom="Chocolat", 
            prix=2.50, 
            categorie="Dessert",
            description="Tablette de chocolat noir", 
            stock=10
    )
    session.add(art); session.commit(); session.refresh(art)

    resp = client.delete(f"/articles/{art.id}")
    assert resp.status_code == 204

    # l'article doit être supprimé
    assert session.get(Articles, art.id) is None

    app.dependency_overrides.clear()


def test_delete_article_forbidden(client: TestClient, session: Session):
    # Créer un rôle "guest" (non autorisé à delete)
    role_guest = session.exec(select(Roles).where(Roles.nom == "guest")).first()
    if not role_guest:
        role_guest = Roles(nom="guest", permission="read")
        session.add(role_guest)
        session.commit()
        session.refresh(role_guest)

    # Créer un utilisateur guest
    user = create_user(session, "user_guest", role_id=role_guest.id)

    # Créer un article en DB
    art = Articles(
        nom="Jus d'orange",
        prix=2.20,
        categorie="Boisson",
        description="Pur jus",
        stock=12,
    )
    session.add(art)
    session.commit()
    session.refresh(art)

    # Override pour simuler la connexion du guest
    app.dependency_overrides[get_current_user] = lambda: user

    # Tentative de suppression (doit être refusée)
    resp = client.delete(f"/articles/{art.id}")
    assert resp.status_code == 403
    # Ajuste le message selon ta fonction require_role (refusé vs interdit)
    assert resp.json()["detail"] in ("Accès refusé", "Accès interdit")

    # L’article doit toujours exister
    assert session.get(Articles, art.id) is not None

    # Nettoyage override
    app.dependency_overrides.pop(get_current_user, None)

