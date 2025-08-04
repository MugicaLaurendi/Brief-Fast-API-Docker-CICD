from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime

class Clients(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    last_name : str
    name : str
    adress : str
    phone_number : int
    mail : str

class Users(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    role_id : int = Field(foreign_key="roles.id")
    username : str
    password : str

class Roles(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    name : str
    access : str

class Commandes(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    client_id : int = Field(foreign_key="clients.id")
    statut_id : int = Field(foreign_key="statuts.id")
    prix : float
    quantite : int
    date : datetime

class Statuts(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    statut : str

class CommandesArticles(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    commandes_id : int = Field(foreign_key="commandes.id")
    articles_id : int = Field(foreign_key="articles.id")

class Articles(SQLModel, table=True):
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