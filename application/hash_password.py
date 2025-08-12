from sqlmodel import select
from app.models import Clients
from app.database_connection import get_session
from app.security import get_password_hash

def hash_existing_passwords():
    session = next(get_session())  # <-- la bonne façon ici
    clients = session.exec(select(Clients)).all()
    for client in clients:
        # Si le mot de passe n'est pas déjà hashé
        if not client.password.startswith("$2b$"):  # Bcrypt hash
            print(f"Hashing password for user: {client.username}")
            client.password = get_password_hash(client.password)
            session.add(client)
    session.commit()
    print("✅ Tous les mots de passe ont été hashés avec succès.")


