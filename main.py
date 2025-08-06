from fastapi import FastAPI, Query
import os
from contextlib import asynccontextmanager
from app.setup_db import setup_db
from app.routers.commandes import *
from app.models import *
import json

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("ENV", "local") == "local" and not os.path.exists("database.db"):
        setup_db()
    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/creercommande/")
def get_dict(id_client : int, id_articles_et_quantites: str = Query(...)):

    try:
        id_articles_et_quantites_parsed = json.loads(id_articles_et_quantites)
        
        return {"commande": creer_commande(id_client, id_articles_et_quantites_parsed)}
    
    except json.JSONDecodeError:

        return {"error": "Invalid dict format"}