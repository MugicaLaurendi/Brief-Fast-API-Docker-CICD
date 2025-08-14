from setup_db import setup_db
from hash_password import hash_existing_passwords
from database_connection import get_session, init_db, engine
from sqlmodel import SQLModel, Session
from sqlalchemy import inspect

# init_db
# session = get_session

def is_database_empty(session: Session) -> bool:

    insp = inspect(engine)
    table_names = insp.get_table_names()

    print(table_names)
    
    if not table_names :
        return True
    else : False



if is_database_empty(Session):

    print("La base est vide")
    print("---------------- CREATION D'UNE BASE DONNEES ------------------")

    setup_db()
    hash_existing_passwords()
else:
    print("Il y a déjà des données")