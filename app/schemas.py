from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


# Modèle pour créer un client
class ClientCreate(BaseModel):
    nom: str
    prenom: str
    adresse: str
    telephone: str
    email: EmailStr
    username: str
    password: str  

# Modèle pour mettre à jour un client
class ClientUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

# Modèle pour afficher un client (réponse API)
class ClientRead(BaseModel):
    id: int
    nom: str
    prenom: str
    adresse: str
    telephone: str
    email: EmailStr
    username: str

    @field_validator('telephone', mode='before')
    @classmethod
    def telephone_to_str(cls, v):
        return str(v)
    
    class Config:
        from_attributes = True  # permet de convertir depuis un objet SQLModel


class ArticleCreate(BaseModel):
    nom: str
    prix: float
    categorie: str
    description: str
    stock: int

class ArticleRead(BaseModel):
    id: int
    nom: str
    prix: float
    categorie: str
    description: str
    stock: int

class ArticleUpdate(BaseModel):
    nom: Optional[str] = None
    prix: Optional[float] = None
    categorie: Optional[str] = None
    description: Optional[str] = None
    stock: Optional[int] = None

class ArticleNoId(BaseModel):
    nom: str
    prix: float
    categorie: str
    description: str
    stock: int

class CommandeWithArticlesNoIds(BaseModel):
    id: int
    date: datetime
    client_id: int
    prix : float
    articles: list[ArticleNoId]

