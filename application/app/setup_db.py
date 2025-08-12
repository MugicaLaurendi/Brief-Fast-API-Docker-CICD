import csv
from pathlib import Path
from sqlmodel import Session, insert
from datetime import datetime

from app.models import engine, init_db, Roles, Status, Articles, Clients, Commandes, CommandesArticles


CSV_DIR = Path(__file__).parent.parent / "csv"

def load_csv(csv_name):
    path = CSV_DIR / csv_name
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [{k: v.strip() for k, v in row.items()} for row in reader]
    return rows

def load_stock_commandes():
    for r in load_csv("commandes.csv"):
        dt = r["date"].strip()
        try:
            r["date"] = datetime.fromisoformat(dt)
        except ValueError:
            r["date"] = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        yield r

def setup_db(seed_csv=True):
    # Création des tables
    init_db()
    if not seed_csv:
        return
    with Session(engine) as session:
        session.execute(insert(Roles), load_csv("roles.csv"))
        session.execute(insert(Articles), load_csv("articles.csv"))
        session.execute(insert(Status), load_csv("status.csv"))
        session.execute(insert(Clients), load_csv("clients.csv"))
        session.execute(insert(Commandes), list(load_stock_commandes()))
        session.execute(insert(CommandesArticles), load_csv("commandes_articles.csv"))
        session.commit()

    print("---------------- DATABASE CREATED --------------------")
