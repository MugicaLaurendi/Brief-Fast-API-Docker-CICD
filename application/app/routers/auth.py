from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from jose import JWTError, jwt

from app.models import Clients, Roles
from app.database_connection import get_session
from app.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    SECRET_KEY,
    ALGORITHM,
)

router = APIRouter(prefix="/auth", tags=["Authentification"])


# Connexion utilisateur
@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    user = db.exec(select(Clients).where(Clients.username == form_data.username)).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# Rafraîchir un access token via refresh token
@router.post("/refresh")
async def refresh_token(request: Request, db: Session = Depends(get_session)):
    body = await request.json()
    refresh_token = body.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token requis")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalide")

        user = db.exec(select(Clients).where(Clients.username == username)).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Utilisateur introuvable")

        new_access_token = create_access_token(data={"sub": user.username})
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token invalide ou expiré")


# Inscription client avec rôle "client" par défaut
@router.post("/register")
def register_client(client_data: dict, db: Session = Depends(get_session)):
    existing = db.exec(select(Clients).where(Clients.username == client_data["username"])).first()
    if existing:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà utilisé")

    role = db.exec(select(Roles).where(Roles.nom == "client")).first()
    if not role:
        raise HTTPException(status_code=500, detail="Rôle 'client' introuvable")

    client_data["password"] = get_password_hash(client_data["password"])
    client = Clients(**client_data, role_id=role.id)
    db.add(client)
    db.commit()
    db.refresh(client)

    return {"message": "Client enregistré avec succès"}
