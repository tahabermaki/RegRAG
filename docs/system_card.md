# Fiche système — RegRAG

> À compléter au fil des phases. C'est l'équivalent d'une fiche d'audit appliquée à notre propre système.

## Usage prévu
Aider des auditeurs et responsables conformité à retrouver et comprendre des dispositions
réglementaires (AI Act, DORA, RGPD, Solvabilité II, publications ACPR…), avec citation systématique des sources.

## Hors périmètre
- Avis juridique ou décision engageante.
- Questions sans rapport avec le corpus : le système doit refuser.

## Données
Documents publics listés dans `corpus/manifest.yaml`, versionnés par hash SHA-256.

## Modèles
| Rôle | Modèle | Hébergement |
| --- | --- | --- |
| Embedding | bge-m3 | Local |
| Reranking | bge-reranker-v2-m3 | Local |
| Génération | Mistral (API), fallback OpenAI | Externe : des extraits de documents sont envoyés au fournisseur |

## Évaluation
Résultats sur le golden set (phase 3) : à remplir.

## Limites connues

## Risques et mesures
| Risque | Mesure | Test associé |
| --- | --- | --- |
| Hallucination | Citations obligatoires, seuil de refus | Questions hors corpus du golden set |
| Injection de prompt | Délimitation du contexte, validation de sortie | Incident 09 |
| Fuite de données personnelles | Masquage à l'ingestion et dans les traces | Incident 10 |

## Transparence
L'interface indique que l'utilisateur échange avec une IA et que les réponses ne valent pas avis juridique.
