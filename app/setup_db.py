import csv
from pathlib import Path
from sqlmodel import Session, insert
from app.models import engine, init_db, roles, statuts, articles, users, clients, commandes, commandes_articles


CSV_DIR = Path(__file__).parent.parent / "csv"

def _load_csv(model, csv_name, fieldnames):
    path = CSV_DIR / csv_name
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [{k: v.strip() for k, v in row.items()} for row in reader]
    return rows

def setup_db(seed_csv=True):
    # Création des tables
    init_db()
    if not seed_csv:
        return
    with Session(engine) as session:
        session.execute(insert(articles), _load_csv(articles, "articles.csv", None))
        session.execute(insert(roles), _load_csv(roles, "roles.csv", None))
        session.execute(insert(statuts), _load_csv(statuts, "statuts.csv", None))
        session.execute(insert(users), _load_csv(users, "users.csv", None))
        session.execute(insert(clients), _load_csv(clients, "clients.csv", None))
        session.execute(insert(commandes), _load_csv(commandes, "commandes.csv", None))
        session.execute(insert(commandes_articles), _load_csv(commandes_articles, "commandes_articles.csv", None))
        session.commit()
