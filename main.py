from fastapi import FastAPI
import os
from contextlib import asynccontextmanager

from app.setup_db import setup_db
from app.routers import commandes, clients, articles
from app.models import *


# Initialisation de l'application FastAPI et création de la base de données(sauf si existante)
@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("ENV", "local") == "local" and not os.path.exists("database.db"):
        setup_db()
    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(commandes.router) # Commandes router
app.include_router(clients.router) # Clients router
app.include_router(articles.router) # Articles router
