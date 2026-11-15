# Runbooks

Un runbook par alerte : quoi vérifier, dans quel ordre, et comment réparer.
Chaque alerte Grafana (phase 4) pointe vers son runbook.

## Exemple : `/health` répond `degraded`
1. `make ps` : quel service n'est pas `healthy` ?
2. `make logs s=<service>` : lire les dernières erreurs.
3. Le service est arrêté → `docker compose up -d <service>`.
4. Le service redémarre en boucle → vérifier la mémoire (`docker stats`) et l'espace disque.
5. Toujours en panne → restaurer le dernier snapshot (Qdrant) ou le dernier dump (Postgres).
