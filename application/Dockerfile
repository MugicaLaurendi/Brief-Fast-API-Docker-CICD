FROM python:3.12

# Installer les dépendances système nécessaires pour psycopg2 et compilation
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
 && rm -rf /var/lib/apt/lists/*


# Créer un utilisateur non-root
RUN useradd -m appuser


WORKDIR /application


# Copier uniquement le fichier requirements
COPY --chown=appuser:appuser ./requirements.txt /application/requirements.txt

# Installer les dépendances sans cache
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /application/requirements.txt


COPY --chown=appuser:appuser . .

# Passer à l'utilisateur non-root
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
