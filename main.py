from fastapi import FastAPI
import os
from contextlib import asynccontextmanager
from app.setup_db import setup_db
from app.models import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("ENV", "local") == "local" and not os.path.exists("database.db"):
        setup_db()
    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)
