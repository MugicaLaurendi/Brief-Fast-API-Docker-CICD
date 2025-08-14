import csv
from pathlib import Path
from sqlmodel import Session, insert
from datetime import datetime

from app.models import Roles, Status, Articles, Clients, Commandes, CommandesArticles
from app.database_connection import engine, init_db

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


def drop_id(rows):
    for r in rows:
        d = dict(r)
        d.pop("id", None)  # on enlève l'id s'il existe
        yield d

def setup_db(seed_csv=True):
    init_db()
    if not seed_csv:
        return
    with Session(engine) as session:
        # Tables où tu VEUX garder les id explicites (ex: dimensions, enums)
        session.execute(insert(Roles), drop_id(load_csv("roles.csv")))
        session.execute(insert(Status), drop_id(load_csv("status.csv")))

        # Tables avec PK auto → on enlève l'id
        session.execute(insert(Articles), list(drop_id(load_csv("articles.csv"))))
        session.execute(insert(Clients),  list(drop_id(load_csv("clients.csv"))))
        session.execute(insert(Commandes), list(drop_id(load_stock_commandes())))
        session.execute(insert(CommandesArticles), list(drop_id(load_csv("commandes_articles.csv"))))

        session.commit()
    print("---------------- DATABASE CREATED --------------------")