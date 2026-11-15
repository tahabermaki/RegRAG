"""Worker d'ingestion (arq + Redis).

Pourquoi un worker séparé : parser un PDF avec Docling peut prendre des minutes.
On ne veut pas bloquer l'API pendant ce temps. L'API dépose un travail dans
Redis, le worker le prend et le traite en tâche de fond, avec retries.

Phase 0 : une tâche `ping` pour vérifier que la chaîne API -> Redis -> worker marche.
Phase 1 : la tâche `ingest_document` (parsing, chunking, embeddings, upsert Qdrant).
"""

import logging

from arq.connections import RedisSettings

from regrag.config import get_settings
from regrag.observability.logging import setup_logging

settings = get_settings()
setup_logging(settings.log_level)
log = logging.getLogger("regrag.worker")


async def ping(ctx: dict) -> str:
    log.info("ping reçu")
    return "pong"


async def startup(ctx: dict) -> None:
    log.info("worker démarré")


class WorkerSettings:
    functions = [ping]
    on_startup = startup
    redis_settings = RedisSettings.from_dsn(settings.redis_url)
    max_tries = 3
