from typing import Union
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.models import *
import datetime


def creer_commande(id_client, id_articles_et_quantites):

    with Session(engine) as session:

        # checker si client existe

        statement = select(Clients).where(Clients.id == id_client)
        client = session.exec(statement).first()
        if client == None :
            return {"error": "client does not exist"}
        
        # creer dans la table commandes une commande avec un prix a 0

        commande = Commandes(client_id= id_client, status_id= 1 , prix= 0 , date= datetime.datetime.now())
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