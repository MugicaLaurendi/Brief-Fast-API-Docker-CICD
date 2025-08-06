from typing import Union
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.models import *
from datetime import date
import datetime as dt
from fastapi import APIRouter, Depends, HTTPException
from typing import List
import json

router = APIRouter(prefix="/commandes", tags=["Commandes"])


@router.get("/creercommande/")
def creer_commande(id_client, id_articles_et_quantites, db: Session = Depends(get_session) ):

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


# ================================
# Consulter les commandes par date
# ================================
@router.get("/par-date/{date_commande}", response_model=List[Commandes])
def get_commandes_by_date(date_commande: date, session: Session = Depends(get_session)):
    commandes = session.exec(
        select(Commandes).where(Commandes.date == date_commande)
    ).all()

    if not commandes:
        raise HTTPException(status_code=404, detail="Aucune commande trouvée pour cette date")

    return commandes
