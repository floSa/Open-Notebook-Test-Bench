# A3. Automatiser par l'API et MCP

> **Objet** : automatiser Open Notebook par son API REST (carnets, sources, questions, recherche, modèles) et le piloter depuis un assistant par le protocole MCP.
> **Prérequis** : Open Notebook installé et branché au service LLM central ([Installer Open Notebook](../manuel/02-installer-open-notebook.md)) ; avoir posé une question dans un carnet ([Discuter avec les sources](../manuel/06-discuter-avec-les-sources.md)) ; notions de [fonctionnement interne](A5-fonctionnement-interne.md).
> **Version décrite** : Open Notebook 1.15.1 (API sur `127.0.0.1:5055`), modèles du service LLM central (`chat`, `embed`, `transcribe`) depuis le 12 novembre 2026 ; serveur MCP tiers `open-notebook-mcp` 0.3.0 avec le SDK `mcp` 1.30.0. Les sorties des exemples datent du 8 novembre 2026 : ancienne pile (Ollama sur CPU, qwen3:4b-instruct, bge-m3), modèles différents.
> **Statut des informations** : [Vérifié] observé ou mesuré sur la machine d'essai, avec un renvoi au résultat brut (8 novembre 2026 : ancienne pile ; 12 novembre 2026 : service LLM central) ; [Source] documentation officielle ou code source au tag v1.15.1 ; [Estimation] calcul ou déduction non mesurés ; [À tester] non documenté et non essayé.
> **Précautions** : le paquet MCP tiers a été relu avant installation ([relecture](../../../outils/resultats/open-notebook/relecture-mcp.md)) ; seuls des outils de lecture ont été appelés, plus un appel d'écriture sur un carnet d'essai. Le mot de passe de l'API n'est jamais écrit dans une commande : les exemples le lisent dans `donnees/open-notebook/.env`.

**Risques signalés.** Le serveur MCP tiers expose sans confirmation des outils de suppression (`delete_notebook`, `delete_source`, etc.) et `update_settings`. Ce dernier peut par exemple rétablir un moteur d'extraction de liens qui passe par un service tiers. Un assistant branché dessus peut donc effacer des données ou changer des réglages. Le mot de passe de l'API donne un accès complet : aucun rôle, aucun jeton limité [Source] (`api/auth.py`).

## Sommaire

1. [Principes de l'API](#1-principes-de-lapi)
2. [Brancher les modèles par l'API](#2-brancher-les-modèles-par-lapi)
3. [Créer un carnet et ajouter une source](#3-créer-un-carnet-et-ajouter-une-source)
4. [Poser une question](#4-poser-une-question)
5. [Rechercher](#5-rechercher)
6. [Brancher un client MCP](#6-brancher-un-client-mcp)
7. [Dépannage](#dépannage)
8. [Sources](#sources)

## 1. Principes de l'API

### Essentiel

- Toutes les routes sont sous `http://127.0.0.1:5055/api`. La documentation interactive est sur `http://127.0.0.1:5055/docs` [Source] (`api/main.py`).
- Authentification : en-tête `Authorization: Bearer <mot de passe>`, le même mot de passe que pour l'interface. Sans cet en-tête, l'API répond `401 {"detail":"Missing authorization header"}` [Vérifié] le 12 novembre 2026 ([vérification minimale](../../../outils/resultats/open-notebook/verif-minimale-2026-11-12.json)).
- Le mot de passe est dans `donnees/IDENTIFIANTS-LOCAUX.txt` et dans `donnees/open-notebook/.env` (variable `OPEN_NOTEBOOK_PASSWORD`).
- Les exemples sont dans `exemples/open-notebook/`. Ils lisent le mot de passe dans la variable `ON_MDP`, sinon dans `donnees/open-notebook/.env`. Leurs sorties réelles sont dans [sorties_verifiees.txt](../../../exemples/open-notebook/sorties_verifiees.txt).

Sorties des exemples : elles datent du 8 novembre 2026, sur l'ancienne pile (Ollama sur CPU, qwen3:4b-instruct, bge-m3 servi par Ollama). Les réponses et les scores de recherche dépendent du modèle : ils sont à rejouer sur le service LLM central [À tester]. Commande qui rejoue un exemple et ajoute sa sortie au fichier [Aide] :

```bash
bash exemples/open-notebook/lancer_tous.sh 01_etat_api.sh 02_creer_carnet_et_source.sh
```

État et authentification [Testée] :

```bash
bash exemples/open-notebook/01_etat_api.sh
```

Sortie du 8 novembre 2026 [Vérifié] ([sortie](../../../exemples/open-notebook/sorties_verifiees.txt)) : `{"status":"healthy"}`, `{"auth_enabled":true,...}`, HTTP 401 sans mot de passe, HTTP 200 avec.

Appel minimal à la main, pour lister les carnets [Aide] :

```bash
curl -s -H "Authorization: Bearer <mot de passe>" http://127.0.0.1:5055/api/notebooks
```

### Pour aller plus loin

| Besoin | Méthode et route |
|---|---|
| Carnets | `GET`, `POST /api/notebooks` ; `DELETE /api/notebooks/{id}?delete_exclusive_sources=true` |
| Sources | `POST /api/sources` (formulaire multipart) ; `GET /api/sources/{id}` ; `GET /api/sources/{id}/status` |
| Chat | `POST /api/chat/sessions`, `POST /api/chat/context`, `POST /api/chat/execute` |
| Recherche | `POST /api/search` ; « Demander » : `POST /api/search/ask/simple` |
| Notes, transformations | `POST /api/notes` ; `POST /api/transformations/execute` ; `POST /api/sources/{id}/insights` |
| Modèles | `POST /api/credentials`, `POST /api/credentials/{id}/test`, `POST /api/models`, `PUT /api/models/defaults` |
| Réglages | `GET`, `PUT /api/settings` |

Routes relevées dans le code [Source] ([synthèse](../../../outils/resultats/open-notebook/cadrage-source.md)). Celles du tableau ont toutes été appelées par les scripts de `outils/open-notebook/` [Vérifié] ; les routes des modèles et des réglages l'ont été le 12 novembre 2026 sur le service LLM central ([configuration](../../../outils/resultats/open-notebook/configuration-2026-11-12.json)).

## 2. Brancher les modèles par l'API

### Essentiel

Le script `outils/open-notebook/configurer.py` fait par l'API ce que la page **Modèles** fait à la souris. Il est rejouable. Il est lancé par l'installateur [Testée] ([journal](../../../outils/resultats/open-notebook/installation-2026-11-12.log)) :

```bash
python3 outils/open-notebook/configurer.py --voix
```

Ce qu'il crée, relevé le 12 novembre 2026 [Vérifié] ([configuration](../../../outils/resultats/open-notebook/configuration-2026-11-12.json)) :

| Élément | Valeur |
|---|---|
| Fournisseur | « OpenAI Compatible » (`openai_compatible`), configuration nommée `llm-central` |
| Base URL | `http://llm-central:8080/v1` (adresse vue depuis le conteneur, réseau `llm-net`) |
| Modalités | `language`, `embedding`, `speech_to_text` |
| Clé | présente (`has_api_key: true`), lue dans le `.env` du dépôt (`LLM_CENTRAL_KEY`), jamais affichée |
| Test de connexion | « Connected. 9 models available: chat, embed, rerank (+6 more) » |
| Modèles enregistrés | `chat` (language), `embed` (embedding), `transcribe` (speech_to_text) |
| Synthèse vocale | configuration `speaches-voix` sur `rag-speaches`, modèle `speaches-ai/Kokoro-82M-v1.0-ONNX` (text_to_speech) |
| Défauts | `chat` pour le chat, les transformations, les outils et le large contexte ; `embed` ; `transcribe` ; Kokoro |

Le même passage a retiré les anciennes configurations `llm-service-chat` et `llm-service-embed` (ancienne pile vLLM) et l'ancien modèle de transcription `Systran/faster-whisper-small` de `rag-speaches` [Vérifié] (même fichier, clé `retires`).

### Pour aller plus loin

- Le modèle `rerank` du service central n'est pas enregistrable : l'API n'accepte que les types `language`, `embedding`, `text_to_speech`, `speech_to_text`, et le code indique « Reranking is out of scope (#1087) » [Vérifié] ([relevé](../../../outils/resultats/open-notebook/reranker-2026-11-12.txt)).
- La transcription d'un fichier audio n'utilise pas la Base URL enregistrée : elle lit `OPENAI_COMPATIBLE_BASE_URL_STT` et `OPENAI_COMPATIBLE_API_KEY_STT`, fixées dans `outils/open-notebook/compose.override.yml` [Vérifié] sur l'ancienne pile ([journal](../../../outils/resultats/open-notebook/essai-audio-scan-2026-11-08.log)).

## 3. Créer un carnet et ajouter une source

### Essentiel

Exemple [Testée] : crée le carnet « Exemple API », y ajoute la note du CSE et attend la fin du traitement.

```bash
bash exemples/open-notebook/02_creer_carnet_et_source.sh
```

Sortie du 8 novembre 2026, ancienne pile [Vérifié] ([sortie](../../../exemples/open-notebook/sorties_verifiees.txt)) : `statut : completed, passages : 1`.

Trois pièges, tous rencontrés ou relevés :

1. `POST /api/sources` n'accepte qu'un **formulaire multipart** (`-F` avec curl), pas du JSON [Vérifié] (le serveur MCP tiers échoue justement là, section 6).
2. Sans `embed=true`, la source n'a pas d'embeddings : elle n'apparaît pas dans la recherche vectorielle [Source] (`api/routers/sources.py`).
3. Le statut `completed` signifie « texte extrait », pas « embeddings calculés » : l'embedding est une seconde tâche. Il faut attendre `embedded_chunks > 0` dans `GET /api/sources/{id}` [Source] (`commands/source_commands.py`), comme le fait l'exemple.

Sur le service LLM central, la même suite (création d'un carnet, ajout d'une source, attente des embeddings) a pris 5,4 s pour une page de 594 caractères [Vérifié] le 12 novembre 2026 ([vérification minimale](../../../outils/resultats/open-notebook/verif-minimale-2026-11-12.json)).

### Pour aller plus loin

Avec `async_processing=false` (valeur par défaut), l'appel bloque jusqu'à 300 s [Source]. Il ne faut pas relier deux fois une source au même carnet par `POST /api/notebooks/{nb}/sources/{src}` : le contrôle de doublon de cette route ne fonctionne pas et crée un lien en double [Source] (`api/routers/notebooks.py:352-364`).

## 4. Poser une question

### Essentiel

Exemple [Testée] (bibliothèque standard Python seulement) :

```bash
python3 exemples/open-notebook/03_poser_question.py "Exemple API" "Quel est le montant de la prime d'intéressement ?"
```

Étapes : créer une session (`/api/chat/sessions`), construire le contexte en choisissant le mode de chaque source (`/api/chat/context`), envoyer la question avec ce contexte (`/api/chat/execute`). La réponse renvoie tout l'historique de la session. La réponse est le dernier message de type `ai`. Les citations sont les motifs `[source:…]` du texte [Vérifié].

Sortie du 8 novembre 2026, ancienne pile (qwen3:4b-instruct) [Vérifié] ([sortie](../../../exemples/open-notebook/sorties_verifiees.txt)) : contexte de 199 jetons, réponse « Le montant de la prime d'intéressement 2025 est de 1 150 euros par salarié. » avec une citation.

Sur le service LLM central (`chat`), une question du même type par l'API a répondu en 9,9 s, avec une citation correcte, pour un contexte de 208 jetons [Vérifié] le 12 novembre 2026 ([vérification minimale](../../../outils/resultats/open-notebook/verif-minimale-2026-11-12.json)).

### Pour aller plus loin

La réponse n'est pas diffusée au fil de l'eau par cette route. Le modèle `chat` réfléchit avant de répondre (réflexion activée par défaut dans le service central) : prévoir un délai d'attente long côté client. L'exemple accepte 900 s, comme `ESPERANTO_LLM_TIMEOUT` dans l'override.

## 5. Rechercher

### Essentiel

Exemple [Testée] :

```bash
bash exemples/open-notebook/04_rechercher.sh "prime d'intéressement"
```

`type` vaut `text` (mots) ou `vector` (sens). `minimum_score` (0,2 par défaut) ne s'applique qu'à la recherche vectorielle [Source]. Les différences mesurées sont dans [Qualité et performances](A1-qualite-et-performances.md).

Sortie du 8 novembre 2026, ancienne pile (bge-m3 servi par Ollama) [Vérifié] ([sortie](../../../exemples/open-notebook/sorties_verifiees.txt)) : en `text`, la note du CSE seule ; en `vector`, la note du CSE en tête (0,57), puis deux autres documents (0,37 et 0,36). Le premier lancement de ce jour-là a échoué sur une apostrophe mal protégée dans le script, corrigée depuis (même fichier). Les scores vectoriels changent avec le service d'embedding (bge-m3 Q8_0 sur llama.cpp) : à rejouer [À tester].

### Pour aller plus loin

Nettoyage des exemples 02 et 03 [Testée] :

```bash
bash exemples/open-notebook/05_supprimer_carnet.sh
```

## 6. Brancher un client MCP

### Essentiel

Open Notebook 1.15.1 n'a pas de serveur MCP officiel. Sa documentation renvoie au paquet tiers `open-notebook-mcp` [Source] (`docs/5-CONFIGURATION/mcp-integration.md`). La version 0.3.0 a été relue, puis installée dans l'environnement Python du dépôt [Testée] :

```bash
uv pip install --python .venv/bin/python "open-notebook-mcp==0.3.0" "mcp<2"
```

La contrainte `mcp<2` est indispensable : le paquet ne fixe pas de borne haute, et le SDK `mcp` 2.x casse son import [Source] ([relecture](../../../outils/resultats/open-notebook/relecture-mcp.md)).

Essai avec un client MCP minimal en stdio [Testée] :

```bash
.venv/bin/python exemples/open-notebook/06_client_mcp.py
```

Résultat du 8 novembre 2026 [Vérifié] ([sortie](../../../exemples/open-notebook/sorties_verifiees.txt)). Le client MCP ne parle qu'à l'API : ces résultats ne dépendent pas du service de modèles, sauf pour les outils de question, non appelés.

| Appel | Résultat |
|---|---|
| liste des outils | 33 outils (carnets, sources, notes, chat, recherche, modèles, réglages) |
| `list_notebooks` | correct |
| `search` (plein texte) | correct |
| `create_source` | échec : « Field required … type » ; le serveur envoie du JSON à une route qui attend un formulaire |

Configuration pour un client MCP (Claude Desktop, Claude Code, autre) [À tester] : commande `<dépôt>/.venv/bin/open-notebook-mcp`, transport stdio, variables `OPEN_NOTEBOOK_URL=http://127.0.0.1:5055` et `OPEN_NOTEBOOK_PASSWORD=<mot de passe>`.

### Pour aller plus loin

D'après la relecture du code [Source] : le mode HTTP du serveur ne démarre pas avec le SDK 1.x ; `get_model` appelle une route absente de la 1.15.1 ; les outils de question coupent au bout de 30 s, ce qui est court pour un modèle qui réfléchit avant de répondre ; le projet n'a reçu aucun commit depuis onze mois. Pour un usage durable, appeler l'API REST directement (sections 3 à 5) est plus sûr.

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| `401 Missing authorization header` | mot de passe actif | ajouter l'en-tête `Authorization: Bearer <mot de passe>` |
| `422` en ajoutant une source en JSON sur `/api/sources` | la route n'accepte qu'un formulaire multipart | `curl -F …`, ou `POST /api/sources/json` pour un texte ou un lien |
| MCP `create_source` : « Field required … type » | défaut du serveur MCP tiers 0.3.0 | ajouter la source par l'API REST |
| MCP `create_source` : « notebook_id Field required » | paramètre obligatoire du serveur | passer l'identifiant du carnet |
| La source est « completed » mais introuvable en recherche vectorielle | embedding pas encore calculé, ou `embed` absent | attendre `embedded_chunks > 0` ; ajouter `embed=true` |
| Le client coupe avant la réponse | réflexion de `chat`, réponse non diffusée au fil de l'eau | délai d'attente client de plusieurs minutes (l'exemple 03 accepte 900 s) |
| `POST /api/models` refuse le type `rerank` | aucun reranker accepté par Open Notebook 1.15.1 | rien à faire : le modèle `rerank` du service central reste inutilisé |

## Sources

- API : http://127.0.0.1:5055/docs (OpenAPI de l'instance) ; code : https://github.com/lfnovo/open-notebook/tree/v1.15.1/api ; [synthèse du code](../../../outils/resultats/open-notebook/cadrage-source.md)
- Serveur MCP tiers : https://github.com/Epochal-dev/open-notebook-mcp, paquet PyPI `open-notebook-mcp` 0.3.0 ; [relecture](../../../outils/resultats/open-notebook/relecture-mcp.md)
- Exemples : `exemples/open-notebook/01_etat_api.sh` à `06_client_mcp.py`, `lancer_tous.sh` ; [sorties vérifiées](../../../exemples/open-notebook/sorties_verifiees.txt) (ancienne pile, 8 novembre 2026)
- Branchement au service central : `outils/open-notebook/configurer.py` ; [configuration du 12 novembre 2026](../../../outils/resultats/open-notebook/configuration-2026-11-12.json), [vérification minimale](../../../outils/resultats/open-notebook/verif-minimale-2026-11-12.json), [relevé du reranker](../../../outils/resultats/open-notebook/reranker-2026-11-12.txt)
- Termes techniques : [glossaire](../../glossaire.md)
