# Brief-Fast-API-Docker-CICD
Projet ecole Simplon

Vous êtes développeur·euse backend au sein d’une start‑up tech spécialisée dans les solutions métier.
Votre nouveau client, RestauSimplon, souhaite digitaliser la gestion de ses commandes.
Aujourd’hui, tout se fait sur papier : erreurs fréquentes et temps de traitement élevés.
## Objectifs principaux
 
 - Authentification/Autorisation par jetons (JWT) — Semaine 1.
 - Conteneurisation via Docker & Docker Compose — Semaine 2.
 - CI/CD & tests automatisés (GitHub Actions ou GitLab CI, pytest) — Semaine 3.

## Structure du projet

- application/ : code de l’API FastAPI
    - app/models.py : définition des modèles (clients, commandes, articles, etc.)
    - app/routers/ : routes pour l’authentification, les clients, les articles et les commandes
- main.py : point d’entrée de l’application
- initialiser_db/ : scripts pour initialiser et peupler la base de données
- tests/ : suite de tests unitaires et d’intégration (pytest)
- docker-compose.yml : configuration pour l’environnement de développement
- docker-compose_test.yml : configuration pour exécuter les tests en conteneur

## Pré‑requis

- Docker & Docker Compose
- (Optionnel) Python 3.12+ si vous lancez l’API hors Docker

## Configuration

```
# Pour le local seulement
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=postgres

SECRET_KEY="change-this-key-to-a-random-long-secret"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256
```

## Lancer l'application

```bash
docker compose up --build
```
#### Services disponibles :
- API FastAPI : http://localhost:8000
- pgAdmin : http://localhost:5050

La base de données est automatiquement initialisée grâce au service initialiser_db.

## Exécuter les tests

#### En local :

```bash
pytest
```
#### Via Docker (en utilisant l’environnement de test) :

```bash
docker compose -f docker-compose_test.yml up --build --exit-code-from app
```

## Points d’entrée de l’API

Les routes principales sont accessibles sous /articles, /clients, /commandes, et /auth pour l’authentification via :
- http://localhost:8000/docs