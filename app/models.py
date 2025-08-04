from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime

class clients(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    last_name : str
    name : str
    adress : str
    phone_number : int
    mail : str

class users(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    role_id : int = Field(foreign_key="roles.id")
    username : str
    password : str

class roles(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    name : str
    access : str

class commandes(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    client_id : int = Field(foreign_key="clients.id")
    statut_id : int = Field(foreign_key="statuts.id")
    prix : float
    quantite : int
    date : datetime

class statuts(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    statut : str

class commandes_articles(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    commandes_id : int = Field(foreign_key="commandes.id")
    articles_id : int = Field(foreign_key="articles.id")

class articles(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    name : str
    price : int
    category : str
    description: str
    stock : int


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)