from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import join
from datetime import date, datetime, time
import datetime as dt
from typing import List
import json

from application.app.models import Clients, Commandes, CommandesArticles, Articles
from application.app.database_connection import get_session
from application.app.schemas import CommandeWithArticlesNoIds
from application.app.security import require_role



router = APIRouter(prefix="/commandes", tags=["Commandes"])



# ===========================
#    GESTION DES COMMANDES
# ===========================


# creer une nouvelle commande
@router.get("/creer/", dependencies=[Depends(require_role([1,2]))])
def creer_commande(id_client, id_articles_et_quantites, db: Session = Depends(get_session)):

    with db as session:
        
        try:
            id_articles_et_quantites = json.loads(id_articles_et_quantites)
        
        except json.JSONDecodeError:

            return {"error": "Invalid dict format"}
        
        # checker si client existe
        statement = select(Clients).where(Clients.id == id_client)
        client = session.exec(statement).first()
        if client == None :
            return {"error": "client does not exist"}
        
        # creer dans la table commandes une commande avec un prix a 0

        commande = Commandes(client_id= id_client, status_id= 1 , prix= 0 , date= dt.datetime.now())
        commande_id = 0
        session.add(commande)
        session.commit()
        commande_id = commande.id

        
        # creer les lignes correspondantes dans la table commandes_articles

        for id_article, quantite in id_articles_et_quantites.items() :

            commande_article = CommandesArticles(commande_id= commande_id, article_id= int(id_article), quantite= quantite)
            session.add(commande_article)

        session.commit()
        
        # recuperer le prix de chaque article et calculer le prix total

        prix_commande_article = []

        for id_article, quantite in id_articles_et_quantites.items() :

            statement = select(Articles).where(Articles.id == id_article)
            is_article = session.exec(statement).first()
            
            if is_article == None :
                return {"error": "product does not exist"}

            article = session.exec(statement).first()
            prix_articles = article.prix * quantite
            prix_commande_article.append(prix_articles)
        
        prix_total = sum(prix_commande_article)

        # enregistrer le prix dans la table commandes

        commande.prix = prix_total
        session.add(commande)
        session.commit()
        
        # retourner la ligne correspondante de la table commandes

        statement = select(Commandes).where(Commandes.id == commande.id)
        final_commande = session.exec(statement).first()
        return final_commande


# Consulter les commandes par date
@router.get("/par_date/{date_commande}", response_model=List[Commandes], dependencies=[Depends(require_role([1,2]))])
def get_commandes_by_date(date_commande: date, session: Session = Depends(get_session)):
    start_datetime = datetime.combine(date_commande, time.min)
    end_datetime = datetime.combine(date_commande, time.max)

    commandes = session.exec(
        select(Commandes).where(Commandes.date >= start_datetime, Commandes.date <= end_datetime)
    ).all()

    if not commandes:
        raise HTTPException(status_code=404, detail="Aucune commande trouvée pour cette date")

    return commandes


# Consulter les commandes par client
@router.get("/par_client/{client_id}", response_model=List[CommandeWithArticlesNoIds], dependencies=[Depends(require_role([1,2,3]))])
def get_commandes_by_client_with_articles(
    client_id: int,
    session: Session = Depends(get_session),
):
    j = (
        join(Commandes, CommandesArticles, Commandes.id == CommandesArticles.commande_id)
        .join(Articles, CommandesArticles.article_id == Articles.id)
    )

    stmt = (
        select(Commandes, Articles)
        .select_from(j)
        .where(Commandes.client_id == client_id)
    )

    rows = session.exec(stmt).all()
    if not rows:
        raise HTTPException(status_code=404, detail="Aucune commande pour ce client")

    commandes_map = {}
    for commande, article in rows:
        cmd = commandes_map.setdefault(commande.id, {
            "commande": commande,
            "articles": []
        })
        cmd["articles"].append(article)

    result = []
    for data in commandes_map.values():
        result.append({
            "id": data["commande"].id,
            "date": data["commande"].date,
            "client_id": data["commande"].client_id,
            "prix": data["commande"].prix,
            "articles": data["articles"]
        })

    return result


# Modifier le statut d'une commande
@router.put("/modifier_statut", dependencies=[Depends(require_role([1,2]))])
def update_client(commande_id: int, nouveau_status: int, session: Session = Depends(get_session)):

    statement = select(Commandes).where(Commandes.id == commande_id)
    commande = session.exec(statement).first()

    if not commande:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    commande.status_id = nouveau_status

    session.add(commande)
    session.commit()
    
    statement = select(Commandes).where(Commandes.id == commande_id)
    commande_final = session.exec(statement).first()
    return commande_final