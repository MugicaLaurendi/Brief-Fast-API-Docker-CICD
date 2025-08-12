import os
from sqlmodel import SQLModel, create_engine, Session

# Récupération des variables depuis l'environnement
DB_HOST = os.getenv("DB_HOST", "database")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
DB_NAME = os.getenv("DB_NAME", "postgres")

# Chaîne de connexion PostgreSQL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)


# Ouverture session DB
def get_session():
    with Session(engine) as session:
        yield session