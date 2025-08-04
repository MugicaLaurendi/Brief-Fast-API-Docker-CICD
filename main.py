from fastapi import FastAPI
import os
from contextlib import asynccontextmanager
from app.setup_db import setup_db
from app.models import engine, SQLModel 


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("ENV", "local") == "local" and not getattr(app.state, "_seeded", False):
        setup_db()
        app.state._seeded = True
    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)
