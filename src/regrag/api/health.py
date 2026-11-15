"""Vérification des dépendances (Qdrant, Postgres, Redis).

Deux sondes, comme en production (Kubernetes, load balancers) :
- /health/live  : le processus tourne-t-il ? (ne teste rien d'externe)
- /health       : peut-il servir des requêtes ? (teste chaque dépendance)
Une dépendance en panne donne "degraded" plutôt qu'un crash : c'est la base
de la dégradation contrôlée (incident 13 du catalogue).
"""

import asyncio
import time

import httpx
import psycopg
import redis.asyncio as aioredis

from regrag.config import Settings

TIMEOUT_S = 2.0


async def _timed(name: str, coro) -> dict:
    start = time.perf_counter()
    try:
        await asyncio.wait_for(coro, timeout=TIMEOUT_S)
        status, error = "ok", None
    except Exception as exc:  # noqa: BLE001 - on veut tout capturer ici
        status, error = "down", f"{type(exc).__name__}: {exc}"[:200]
    return {
        "name": name,
        "status": status,
        "latency_ms": round((time.perf_counter() - start) * 1000, 1),
        "error": error,
    }


async def _check_qdrant(url: str) -> None:
    async with httpx.AsyncClient(timeout=TIMEOUT_S) as client:
        resp = await client.get(f"{url}/readyz")
        resp.raise_for_status()


async def _check_postgres(dsn: str) -> None:
    async with await psycopg.AsyncConnection.connect(dsn, connect_timeout=2) as conn:
        await conn.execute("SELECT 1")


async def _check_redis(url: str) -> None:
    client = aioredis.from_url(url, socket_connect_timeout=TIMEOUT_S)
    try:
        await client.ping()
    finally:
        await client.aclose()


async def check_dependencies(settings: Settings) -> dict:
    results = await asyncio.gather(
        _timed("qdrant", _check_qdrant(settings.qdrant_url)),
        _timed("postgres", _check_postgres(settings.postgres_dsn)),
        _timed("redis", _check_redis(settings.redis_url)),
    )
    overall = "ok" if all(r["status"] == "ok" for r in results) else "degraded"
    return {"status": overall, "dependencies": results}
