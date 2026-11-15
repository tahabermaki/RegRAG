"""Configuration centralisée.

Règle du projet : TOUT ce qui change le comportement du RAG (modèles, k, seuils)
vit ici et est lu depuis l'environnement. Un changement de config passe par les
mêmes gates qualité qu'un changement de code.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Stockage
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "regrag_v1"
    postgres_dsn: str = "postgresql://regrag:regrag@localhost:5432/regrag"
    redis_url: str = "redis://localhost:6379/0"

    # Modèles
    embedding_model: str = "BAAI/bge-m3"
    reranker_model: str = "BAAI/bge-reranker-v2-m3"
    llm_model: str = "mistral/mistral-small-latest"
    llm_fallback_model: str = "openai/gpt-4o-mini"

    # Paramètres du RAG
    retrieval_top_k: int = 50
    rerank_top_k: int = 5
    refusal_threshold: float = 0.3

    # Observabilité
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
