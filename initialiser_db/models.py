from sqlmodel import Field, SQLModel
from datetime import datetime
from pydantic.networks import EmailStr


class Clients(SQLModel, table=True):
    id          : int | None = Field(default=None, primary_key=True)
    role_id     : int = Field(foreign_key="roles.id")
    nom         : str
    prenom      : str
    adresse     : str
    telephone   : str
    email       : EmailStr
    username    : str
    password    : str

class Roles(SQLModel, table=True):
    id          : int | None = Field(default=None, primary_key=True)
    nom         : str
    permission  : str

class Commandes(SQLModel, table=True):
    id          : int | None = Field(default=None, primary_key=True)
    client_id   : int = Field(foreign_key="clients.id")
    status_id   : int = Field(foreign_key="status.id")
    prix        : float
    date        : datetime

class Status(SQLModel, table=True):
    id          : int | None = Field(default=None, primary_key=True)
    status      : str

class CommandesArticles(SQLModel, table=True):
    id             : int | None = Field(default=None, primary_key=True)
    commande_id    : int = Field(foreign_key="commandes.id")
    article_id     : int = Field(foreign_key="articles.id")
    quantite       : int

class Articles(SQLModel, table=True):
    id          : int | None = Field(default=None, primary_key=True)
    nom         : str
    prix        : float
    categorie   : str
    description : str
    stock       : int


