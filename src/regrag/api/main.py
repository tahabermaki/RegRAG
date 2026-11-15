"""API FastAPI de RegRAG.

Phase 0 : santé du système + endpoints prévus (non implémentés).
Les endpoints métier arrivent en phase 1 (/ingest) et phase 2 (/ask).
"""

import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from regrag import __version__
from regrag.api.health import check_dependencies
from regrag.config import get_settings
from regrag.observability.logging import request_id_var, setup_logging

settings = get_settings()
setup_logging(settings.log_level)
log = logging.getLogger("regrag.api")

app = FastAPI(
    title="RegRAG",
    version=__version__,
    description="Assistant RAG sur textes réglementaires IA et assurance.",
)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Chaque requête reçoit un identifiant, renvoyé dans l'en-tête X-Request-ID."""
    rid = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:16]
    request_id_var.set(rid)
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response


# ---------- Santé ----------
@app.get("/health/live", tags=["santé"])
async def live() -> dict:
    return {"status": "ok"}


@app.get("/health", tags=["santé"])
async def health() -> JSONResponse:
    report = await check_dependencies(settings)
    report["version"] = __version__
    code = 200 if report["status"] == "ok" else 503
    if code != 200:
        log.warning("health degraded: %s", report["dependencies"])
    return JSONResponse(report, status_code=code)


# ---------- Métier (à venir) ----------
class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000)


@app.post("/ask", tags=["rag"], status_code=501)
async def ask(_: AskRequest) -> dict:
    """Phase 2 : retrieval hybride -> rerank -> génération avec citations."""
    return {"detail": "Pas encore implémenté (phase 2)."}


@app.post("/ingest", tags=["rag"], status_code=501)
async def ingest() -> dict:
    """Phase 1 : met un document en file pour le worker d'ingestion."""
    return {"detail": "Pas encore implémenté (phase 1)."}
