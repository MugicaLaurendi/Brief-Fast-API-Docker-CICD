# Brief-Fast-API-Docker-CICD
Projet ecole Simplon

Vous êtes développeur·euse backend au sein d’une start‑up tech spécialisée dans les solutions métier.
Votre nouveau client, RestauSimplon, souhaite digitaliser la gestion de ses commandes.
Aujourd’hui, tout se fait sur papier : erreurs fréquentes et temps de traitement élevés.
Votre mission consiste à réaliser une API REST complète sous FastAPI pour gérer les articles du menu, les clients et les commandes, tout en intégrant :
 
 - Authentification/Autorisation par jetons (JWT) — Semaine 1.
 - Conteneurisation via Docker & Docker Compose — Semaine 2.
 - CI/CD & tests automatisés (GitHub Actions ou GitLab CI, pytest) — Semaine 3.

## Fichiers

Le projet est composé de plusieurs fichiers.

### app/
 - modeles.py -> definition des tables
 - setup_db -> Charger les sql dans les tables (pour pas partir de rien faut pas déconner)

### roots
 - main.py -> lancer le projet

## Lancer l'application

```bash
fastapi dev main.py
```


table user role -> commande client
table permission -> tel role tel droit

table=false




