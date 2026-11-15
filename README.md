# RegRAG

**Un RAG sur les textes réglementaires IA et assurance (AI Act, DORA, RGPD, ACPR…), construit comme en entreprise : évalué, observé, sécurisé, et volontairement cassé pour apprendre à le réparer.**

> Statut : phase 0 (fondations) — la stack démarre, le RAG ne répond pas encore.

## Pourquoi ce projet
Un RAG de démo tient en 50 lignes. Un RAG de production doit aussi :
- lire correctement des PDF difficiles (tableaux, annexes, versions) ;
- prouver sa qualité avec des tests automatiques, à chaque modification ;
- tracer chaque réponse (documents utilisés, coût, latence) et pouvoir la rejouer ;
- survivre aux pannes (fournisseur LLM, base vectorielle) ;
- résister aux attaques (injection de prompt) et protéger les données personnelles.

## Démarrage

Prérequis : Docker (avec Compose) et `make`.

```bash
git clone https://github.com/tahabermaki/regrag.git && cd regrag
make up          # crée .env, construit les images et démarre tout
```

| Service | URL | Rôle |
| --- | --- | --- |
| API | http://localhost:8000/docs | FastAPI : questions, ingestion, santé |
| Santé | http://localhost:8000/health | État de chaque dépendance |
| Interface | http://localhost:8501 | Streamlit pour les utilisateurs métier |
| Qdrant | http://localhost:6333/dashboard | Base vectorielle |
| Grafana | http://localhost:3001 | Dashboards (`make up-obs`) |

`make` seul liste toutes les commandes.

## Architecture

```
Ingestion (asynchrone)   Sources PDF ─► Worker (Docling, chunking, hash) ─► Embeddings ─► Qdrant
                                              │                                              ▲
                                              ▼                                              │
                                          PostgreSQL (registre des documents et versions)   │
                                                                                             │
Requête (synchrone)      UI ─► API ─► Retrieval hybride (top 50) ─► Rerank (top 5) ─► LLM ─► réponse citée

Transverse               Langfuse (traces) · Prometheus/Grafana (latence, erreurs, coûts) · Ragas en CI
```

| Conteneur | Image | Rôle |
| --- | --- | --- |
| `api` | construite (`Dockerfile`) | Reçoit les questions |
| `worker` | construite (`Dockerfile`) | Ingère les documents en tâche de fond |
| `ui` | construite (`ui/Dockerfile`) | Interface Streamlit |
| `qdrant` | `qdrant/qdrant` | Vecteurs + recherche hybride |
| `postgres` | `postgres` | Registre des documents |
| `redis` | `redis` | File d'attente API → worker |
| `prometheus`, `grafana` | officielles | Métriques (profil `observability`) |

## Feuille de route

| Phase | Contenu | Critère de sortie |
| --- | --- | --- |
| 0 · Fondations ✅ | Repo, Docker, Makefile, CI | `make up` démarre tout |
| 1 · Ingestion | Docling, chunking, versions, idempotence | 30 docs indexés, zéro doublon |
| 2 · Retrieval et génération | Hybride, rerank, citations, refus | Hors corpus refusé, réponses citées |
| 3 · Évaluation | Golden set 150 questions, Ragas | `baseline.json` commitée |
| 4 · Observabilité | Langfuse, Grafana, replay | Chaque réponse a sa trace |
| 5 · CI/CD LLMOps | Gate qualité sur PR | Une PR dégradée est bloquée |
| 6 · Durcissement | Garde-fous, PII, budget, charge | p95 et coût mesurés |
| 7 · Game days | 13 incidents simulés | 13 postmortems |
| 8 · Déploiement | Démo publique, vidéos | Vidéos publiées |

## Structure du repo

```
src/regrag/     api, worker, ingestion, retrieval, generation, guardrails, observability
eval/           golden set et scripts d'évaluation
chaos/          un script par incident simulé
load/           tests de charge (Locust)
ops/            config Prometheus et Grafana
corpus/         manifeste des documents publics (les PDF ne sont pas dans Git)
docs/           ADR, runbooks, postmortems, fiche système
```

## Licence
MIT
