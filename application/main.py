from fastapi import FastAPI

from application.app.routers import commandes, clients, articles, auth, commandes_client
from application.app.models import *


app = FastAPI()

app.include_router(auth.router)

app.include_router(clients.router) # Clients router
app.include_router(articles.router) # Articles router
app.include_router(commandes_client.router) # Commandes client router

app.include_router(commandes.router) # Commandes router





