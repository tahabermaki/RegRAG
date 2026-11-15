# ADR 0001 — Base vectorielle : Qdrant plutôt que pgvector

- **Date** : à remplir
- **Statut** : proposé

> Cet ADR est à rédiger par toi : si tu sais justifier ce choix, c'est que tu l'as compris.
> Réponds aux questions ci-dessous, puis réécris-les dans le format du template.

## Questions pour t'aider
1. Pourquoi a-t-on besoin d'une recherche **hybride** (sens + mots-clés) sur des textes juridiques ?
   Pense à une question comme « que dit l'article 50 ? ».
2. Qdrant sait-il faire du BM25 et de la fusion des résultats nativement ? Et pgvector ?
3. Comment change-t-on de modèle d'embedding sans couper le service ? (indice : alias de collection)
4. Qu'est-ce qu'on perd en ajoutant un service de plus au lieu de tout mettre dans Postgres ?
5. À partir de quel volume, ou dans quel contexte d'entreprise, changerais-tu d'avis ?

## Contexte

## Options envisagées

## Décision

## Conséquences
