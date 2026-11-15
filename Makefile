# Raccourcis du projet. `make` seul affiche l'aide.
.DEFAULT_GOAL := help
COMPOSE := docker compose

.PHONY: help env up up-obs down restart logs ps build clean test lint fmt corpus ingest eval chaos replay

help: ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

env: ## Crée .env à partir de .env.example s'il n'existe pas
	@test -f .env || (cp .env.example .env && echo ".env créé — pense à mettre tes clés API")

# ---------- Cycle de vie ----------
up: env ## Démarre tous les services (cœur)
	$(COMPOSE) up -d --build
	@echo ""
	@echo "  API      http://localhost:8000/docs"
	@echo "  Santé    http://localhost:8000/health"
	@echo "  UI       http://localhost:8501"
	@echo "  Qdrant   http://localhost:6333/dashboard"

up-obs: env ## Démarre le cœur + Prometheus/Grafana
	$(COMPOSE) --profile observability up -d --build
	@echo "  Grafana  http://localhost:3001  (admin / admin)"

down: ## Arrête tout (les données sont conservées)
	$(COMPOSE) --profile observability down

restart: down up ## Redémarre tout

logs: ## Suit les logs de tous les services (make logs s=api pour un seul)
	$(COMPOSE) logs -f $(s)

ps: ## État des services
	$(COMPOSE) ps

build: ## Reconstruit les images de notre code
	$(COMPOSE) build

clean: ## ATTENTION : arrête tout ET supprime les données (volumes)
	$(COMPOSE) --profile observability down -v

# ---------- Qualité du code ----------
test: ## Lance les tests
	PYTHONPATH=src python -m pytest -q

lint: ## Vérifie le style du code
	ruff check src tests scripts ui eval

fmt: ## Formate le code
	ruff format src tests scripts ui eval

# ---------- Données et RAG (phases suivantes) ----------
corpus: ## Télécharge le corpus de démo dans data/raw
	python scripts/download_corpus.py

ingest: ## [Phase 1] Ingère les documents de data/raw
	@echo "Phase 1 : pas encore implémenté"

eval: ## [Phase 3] Lance l'évaluation sur le golden set
	@echo "Phase 3 : pas encore implémenté"

chaos: ## [Phase 7] Déclenche un incident (make chaos i=07-llm-outage)
	@echo "Phase 7 : pas encore implémenté"

replay: ## [Phase 4] Rejoue une requête de prod (make replay t=<trace_id>)
	@echo "Phase 4 : pas encore implémenté"
