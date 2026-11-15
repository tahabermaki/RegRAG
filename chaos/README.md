# Incidents simulés (phase 7)

Un script par incident du catalogue. Chaque incident suit le même cycle :
**provoquer → détecter avec les outils → diagnostiquer soi-même → corriger → postmortem** (`docs/postmortems/`).

| # | Script prévu | Incident |
| --- | --- | --- |
| 01 | `01_broken_tables.py` | Tableaux détruits au parsing |
| 02 | `02_stale_version.py` | Version périmée ou doublons |
| 03 | `03_embedding_swap.py` | Changement d'embedding sans réindexation |
| 04 | `04_out_of_corpus.py` | Hallucination hors corpus |
| 05 | `05_context_overflow.py` | Contexte tronqué |
| 06 | `06_latency_spike.py` | Latence qui explose |
| 07 | `07_llm_outage.py` | Panne ou rate limit du fournisseur LLM |
| 08 | `08_cost_blowup.py` | Explosion des coûts |
| 09 | `09_prompt_injection.py` | Injection de prompt dans un document |
| 10 | `10_pii_leak.py` | Fuite de données personnelles |
| 11 | `11_prompt_regression.py` | Régression après changement de prompt |
| 12 | `12_query_drift.py` | Dérive des questions |
| 13 | `13_vector_db_down.sh` | Base vectorielle indisponible |

Règle d'apprentissage : **cherche la cause toi-même dans les traces avant de demander la solution à une IA.**

L'incident 13 est déjà testable : `docker compose stop qdrant`, puis ouvre http://localhost:8000/health.
