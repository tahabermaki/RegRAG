# Image de NOTRE code Python. Utilisée par deux services : api et worker
# (même image, commande de démarrage différente dans docker-compose.yml).

FROM python:3.12-slim

# Pas de fichiers .pyc, logs affichés immédiatement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# 1. D'abord les dépendances (couche mise en cache tant que requirements.txt ne change pas)
COPY requirements.txt .
RUN pip install -r requirements.txt

# 2. Ensuite le code
COPY src/ ./src/

# 3. On ne tourne jamais en root en production
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "regrag.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
