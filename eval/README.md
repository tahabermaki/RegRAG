# Évaluation (phase 3)

`golden_set.jsonl` : une question par ligne. Objectif 150 questions.

| Champ | Rôle |
| --- | --- |
| `category` | factuelle, article_precis, multi_documents, tableau, hors_corpus, version, adversariale |
| `expected_answer` | réponse attendue, ou `REFUS` |
| `source_doc` / `source_ref` | où se trouve la réponse : sert à évaluer le retrieval étape par étape |
| `reviewed` | `true` seulement après relecture humaine (obligatoire pour une question générée par IA) |

Trois niveaux de mesure : retrieval (le bon passage est-il dans le top 50 ? dans le top 5 après rerank ?),
génération (Ragas : faithfulness, answer relevancy) et métier (refus corrects, citations valides, latence, coût).
