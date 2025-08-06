from fastapi import FastAPI, Query
import os
from contextlib import asynccontextmanager
from app.setup_db import setup_db
from app.routers import commandes, clients, articles
from app.models import *
import json

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("ENV", "local") == "local" and not os.path.exists("database.db"):
        setup_db()
    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)


app.include_router(commandes.router)
app.include_router(clients.router)
app.include_router(articles.router)
