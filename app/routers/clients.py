from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from app.models import Clients, Roles, get_session
from app.schemas import ClientCreate, ClientUpdate, ClientRead



router = APIRouter(prefix="/clients", tags=["Clients"])



# ===========================
#    CRUD COMPLET DES CLIENTS
# ===========================

# Lire tous les clients
@router.get("/", response_model=List[ClientRead])
def read_clients(session: Session = Depends(get_session)):
    return session.exec(select(Clients)).all()


# Lire un client par ID
@router.get("/{client_id}", response_model=ClientRead)
def read_client(client_id: int, session: Session = Depends(get_session)):
    client = session.get(Clients, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client


# Créer un client (inscription)
@router.post("/", response_model=ClientRead)
def create_client(client_data: ClientCreate, session: Session = Depends(get_session)):
    # Vérifier si email déjà utilisé
    existing_email = session.exec(select(Clients).where(Clients.email == client_data.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    # Récupérer l'ID du rôle "client"
    role_client = session.exec(
        select(Roles).where(Roles.nom == "client")
    ).first()
    if not role_client:
        raise HTTPException(status_code=500, detail="Rôle 'client' introuvable en base")

    # Créer le client avec le role_id trouvé
    new_client = Clients(**client_data.model_dump(), role_id=role_client.id)

    session.add(new_client)
    session.commit()
    session.refresh(new_client)
    return new_client


# Modifier un client
@router.put("/{client_id}", response_model=ClientRead)
def update_client(client_id: int, updated_client: ClientUpdate, session: Session = Depends(get_session)):
    db_client = session.get(Clients, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    for field, value in updated_client.model_dump(exclude_unset=True).items():
        setattr(db_client, field, value)

    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client


# Supprimer un client
@router.delete("/{client_id}")
def delete_client(client_id: int, session: Session = Depends(get_session)):
    client = session.get(Clients, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    session.delete(client)
    session.commit()
    return {"message": "Client supprimé avec succès"}