# 08. API REST et MCP

> **Objet** : automatiser Open Notebook par son API REST (carnets, sources, questions, recherche) et le piloter depuis un assistant par le protocole MCP.
> **Prérequis** : [01. Installation](01-installation.md), [04. Chat et citations](04-chat-et-citations.md).
> **Version décrite** : Open Notebook 1.15.1 (API sur `127.0.0.1:5055`), serveur MCP tiers `open-notebook-mcp` 0.3.0 avec le SDK `mcp` 1.30.0, Ollama 0.40.15 (essais du 8 novembre faits sur 0.30.7 ; banc de référence rejoué sur 0.40.15) sur CPU, qwen3:4b-instruct, `num_ctx` 16384.
> **Statut des informations** : [Vérifié] observé ou mesuré le 2026-11-08 sur la machine d'essai (Intel Core Ultra 7 255H, sans GPU NVIDIA) ; [Source] documentation officielle ou code source au tag v1.15.1 ; [Estimation] calcul non mesuré ; [À tester] non documenté et non essayé.
> **Précautions** : le paquet MCP tiers a été relu avant installation ([relecture](../../outils/resultats/open-notebook/relecture-mcp.md)) ; seuls des outils de lecture ont été appelés, plus un appel d'écriture sur un carnet d'essai.

**Risques signalés.** Le serveur MCP tiers expose sans confirmation des outils de suppression (`delete_notebook`, `delete_source`…) et `update_settings`, qui peut par exemple rétablir un moteur d'extraction d'URL passant par un service tiers. Un assistant branché dessus peut donc effacer des données ou changer des réglages. Le mot de passe de l'API donne un accès complet : aucun rôle, aucun jeton limité [Source] (`api/auth.py`).

## Sommaire

1. [Principes de l'API](#1-principes-de-lapi)
2. [Créer un carnet et ajouter une source](#2-créer-un-carnet-et-ajouter-une-source)
3. [Poser une question](#3-poser-une-question)
4. [Rechercher](#4-rechercher)
5. [Brancher un client MCP](#5-brancher-un-client-mcp)
6. [Dépannage](#dépannage)
7. [Sources](#sources)

## 1. Principes de l'API

### Essentiel

- Toutes les routes sont sous `http://127.0.0.1:5055/api` ; la documentation interactive est sur `http://127.0.0.1:5055/docs` [Source] (`api/main.py`).
- Authentification : en-tête `Authorization: Bearer <mot de passe>`, le même que pour l'interface [Vérifié].
- Les exemples de ce manuel sont dans `exemples/open-notebook/` ; leurs sorties réelles sont dans [sorties_verifiees.txt](../../exemples/open-notebook/sorties_verifiees.txt). Ils lisent le mot de passe dans la variable `ON_MDP`, sinon dans `donnees/open-notebook/.env`.

État et authentification [Testée] :

```bash
bash exemples/open-notebook/01_etat_api.sh
```

### Pour aller plus loin

| Besoin | Méthode et route |
|---|---|
| Carnets | `GET`, `POST /api/notebooks` ; `DELETE /api/notebooks/{id}?delete_exclusive_sources=true` |
| Sources | `POST /api/sources` (formulaire multipart) ; `GET /api/sources/{id}` ; `GET /api/sources/{id}/status` |
| Chat | `POST /api/chat/sessions`, `POST /api/chat/context`, `POST /api/chat/execute` |
| Recherche | `POST /api/search` ; « Demander » : `POST /api/search/ask/simple` |
| Notes, transformations | `POST /api/notes` ; `POST /api/transformations/execute` ; `POST /api/sources/{id}/insights` |
| Modèles | `POST /api/credentials`, `POST /api/models`, `PUT /api/models/defaults` |

Routes relevées dans le code [Source] ([synthèse](../../outils/resultats/open-notebook/cadrage-source.md)) ; celles du tableau ont toutes été appelées par les scripts de `outils/open-notebook/` [Vérifié].

## 2. Créer un carnet et ajouter une source

### Essentiel

Exemple [Testée] : crée le carnet « Exemple API », y ajoute la note du CSE et attend la fin du traitement.

```bash
bash exemples/open-notebook/02_creer_carnet_et_source.sh
```

Trois pièges, tous rencontrés ou relevés :

1. `POST /api/sources` n'accepte qu'un **formulaire multipart** (`-F` avec curl), pas du JSON [Vérifié] (le serveur MCP tiers échoue justement là, section 5).
2. Sans `embed=true`, la source n'a pas d'embeddings : elle n'apparaît pas dans la recherche vectorielle [Source] (`api/routers/sources.py`).
3. Le statut `completed` signifie « texte extrait », pas « embeddings calculés » : l'embedding est une seconde tâche. Attendre `embedded_chunks > 0` dans `GET /api/sources/{id}` [Source] (`commands/source_commands.py`), comme le fait l'exemple.

### Pour aller plus loin

Avec `async_processing=false` (valeur par défaut), l'appel bloque jusqu'à 300 s [Source]. Ne pas relier deux fois une source au même carnet par `POST /api/notebooks/{nb}/sources/{src}` : le contrôle de doublon de cette route ne fonctionne pas et crée un lien en double [Source] (`api/routers/notebooks.py:352-364`).

## 3. Poser une question

### Essentiel

Exemple [Testée] (bibliothèque standard Python seulement) :

```bash
python3 exemples/open-notebook/03_poser_question.py "Exemple API" "Quel est le montant de la prime d'intéressement ?"
```

Étapes : créer une session (`/api/chat/sessions`), construire le contexte en choisissant le mode de chaque source (`/api/chat/context`), envoyer la question avec ce contexte (`/api/chat/execute`). La réponse renvoie tout l'historique de la session ; la réponse est le dernier message de type `ai`, et les citations sont les motifs `[source:…]` du texte [Vérifié].

### Pour aller plus loin

La réponse n'est pas diffusée au fil de l'eau par cette route ; sur CPU, prévoir un délai d'attente long côté client (l'exemple accepte 900 s).

## 4. Rechercher

### Essentiel

Exemple [Testée] :

```bash
bash exemples/open-notebook/04_rechercher.sh "prime d'intéressement"
```

`type` vaut `text` (mots) ou `vector` (sens) ; `minimum_score` (0,2 par défaut) ne s'applique qu'à la recherche vectorielle [Source]. Les différences mesurées sont dans [Recherche](06-recherche.md).

### Pour aller plus loin

Nettoyage des exemples 02 et 03 [Testée] :

```bash
bash exemples/open-notebook/05_supprimer_carnet.sh
```

## 5. Brancher un client MCP

### Essentiel

Open Notebook 1.15.1 n'a pas de serveur MCP officiel ; sa documentation renvoie au paquet tiers `open-notebook-mcp` [Source] (`docs/5-CONFIGURATION/mcp-integration.md`). Version 0.3.0 relue puis installée dans l'environnement du dépôt [Testée] :

```bash
uv pip install --python .venv/bin/python "open-notebook-mcp==0.3.0" "mcp<2"
```

La contrainte `mcp<2` est indispensable : le paquet ne fixe pas de borne haute, et le SDK `mcp` 2.x casse son import [Source] ([relecture](../../outils/resultats/open-notebook/relecture-mcp.md)).

Essai avec un client MCP minimal en stdio [Testée] :

```bash
.venv/bin/python exemples/open-notebook/06_client_mcp.py
```

Résultat [Vérifié] ([sortie](../../exemples/open-notebook/sorties_verifiees.txt)) :

| Appel | Résultat |
|---|---|
| liste des outils | 33 outils (carnets, sources, notes, chat, recherche, modèles, réglages) |
| `list_notebooks` | correct |
| `search` (plein texte) | correct |
| `create_source` | échec : « Field required … type » ; le serveur envoie du JSON à une route qui attend un formulaire |

Configuration pour un client MCP (Claude Desktop, Claude Code, autre) [À tester] : commande `<dépôt>/.venv/bin/open-notebook-mcp`, transport stdio, variables `OPEN_NOTEBOOK_URL=http://127.0.0.1:5055` et `OPEN_NOTEBOOK_PASSWORD=<mot de passe>`.

### Pour aller plus loin

D'après la relecture du code [Source] : le mode HTTP du serveur ne démarre pas avec le SDK 1.x ; `get_model` appelle une route absente de la 1.15.1 ; les outils de question coupent au bout de 30 s, ce qui est court pour un modèle sur CPU ; le projet n'a pas reçu de commit depuis onze mois. Pour un usage durable, appeler l'API REST directement (sections 2 à 4) est plus sûr.

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| `422` en ajoutant une source en JSON sur `/api/sources` | la route n'accepte qu'un formulaire multipart | `curl -F …`, ou `POST /api/sources/json` pour un texte ou un lien |
| MCP `create_source` : « Field required … type » | défaut du serveur MCP tiers 0.3.0 | ajouter la source par l'API REST |
| MCP `create_source` : « notebook_id Field required » | paramètre obligatoire du serveur | passer l'identifiant du carnet |
| La source est « completed » mais introuvable en recherche vectorielle | embedding pas encore calculé, ou `embed` absent | attendre `embedded_chunks > 0` ; ajouter `embed=true` |

## Sources

- API : http://127.0.0.1:5055/docs (OpenAPI de l'instance) ; code : https://github.com/lfnovo/open-notebook/tree/v1.15.1/api
- Serveur MCP tiers : https://github.com/Epochal-dev/open-notebook-mcp, paquet PyPI `open-notebook-mcp` 0.3.0 ; [relecture](../../outils/resultats/open-notebook/relecture-mcp.md)
- Exemples : `exemples/open-notebook/01_etat_api.sh` à `06_client_mcp.py`, [sorties vérifiées](../../exemples/open-notebook/sorties_verifiees.txt)
