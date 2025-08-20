from sqlmodel import select
from app.models import Articles
from fastapi.testclient import TestClient
import json


# ---------- HELPERS ----------
def create_article(session, nom):
    """Ajoute un utilisateur directement en DB"""
    article = Articles(
        nom=f'{nom}',
        prix=10,
        categorie= "Plat",
        description="test de test",
        stock=10
    )
    session.add(article)
    session.commit()
    session.refresh(article)
    return article


# ---------- TESTS ----------

def test_creer_commande_no_article(auth_client: TestClient, session):
    id_client = 1
    commande_dict = {"9999999": 2}
    params = {
        "id_client": id_client,
        "id_articles_et_quantites": json.dumps(commande_dict)
    }
    response = auth_client.get("/commandes/creer/", params=params)
    assert response.status_code == 200
    assert response.json() == {"error": "product does not exist"}


def test_creer_commande_no_client(auth_client: TestClient, session):
    id_client = 9999999
    commande_dict = {"1": 2}
    params = {
        "id_client": id_client,
        "id_articles_et_quantites": json.dumps(commande_dict)
    }
    response = auth_client.get("/commandes/creer/", params=params)
    assert response.status_code == 200
    assert response.json() == {"error": "client does not exist"}


def test_creer_commande_no_dict(auth_client: TestClient, session):
    id_client = 1
    commande_dict = {"1": 2,}
    params = {
        "id_client": id_client,
        "id_articles_et_quantites": commande_dict
    }
    response = auth_client.get("/commandes/creer/", params=params)
    assert response.status_code == 200
    assert response.json() == {"error": "Invalid dict format"}


def test_creer_commande_ok(auth_client: TestClient, session):

    create_article(session,"article1")
    article = session.exec(select(Articles).where(Articles.nom == "article1")).first()

    id_client = 1
    commande_dict = {f"{article.id}": 2}
    params = {
        "id_client": id_client,
        "id_articles_et_quantites": json.dumps(commande_dict)
    }

    
    response = auth_client.get("/commandes/creer/", params=params)
    body = response.json()

    assert response.status_code == 200
    
    assert body["client_id"] == 1
    assert body["status_id"] == 1
    assert body["prix"] == 20