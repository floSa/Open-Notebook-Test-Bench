# Relecture avant essai — serveur MCP tiers `open-notebook-mcp`

Date : 2026-11-08. Lecture seule, rien installé ni exécuté. Sources relues :

- dépôt `Epochal-dev/open-notebook-mcp`, branche `main` au commit `a2cddbf` (2025-12-22) et branche `develop` au commit `3717a58` ;
- archives PyPI 0.3.0 téléchargées sans dépendances : wheel sha256 `3ee108092cb7fd0e1ee5e10aeec35bb7d0eb4fe9319d2af13270aab2c9cb744e`, sdist sha256 `4525535a8c62c78c77004636ad018e7b1bf7a8eadc3f703d9e915003f36e8127` (égales aux empreintes publiées par PyPI) ;
- wheels `mcp` 1.30.0 et 2.3.0 (pour vérifier la compatibilité du SDK) ;
- le code d'Open Notebook au tag `v1.15.1` (déjà relu, voir [cadrage-source.md](cadrage-source.md)).

Sauf mention, les renvois `server.py:N` désignent `src/open_notebook_mcp/server.py` (1 311 lignes, identique dans le dépôt, le wheel et le sdist).

## 1. Version, provenance, activité

| Point | Constat | Où |
|---|---|---|
| Dernière version PyPI | **0.3.0**, publiée le 2025-12-22 à 11:33 UTC. Versions précédentes 0.1.0, 0.1.1, 0.2.0, toutes le même jour. | API JSON PyPI |
| Tag Git | **Aucun tag** dans le dépôt (`git ls-remote --tags` vide). `main` est resté en 0.2.0 (`pyproject.toml:3`, `server.json:9,14`). La 0.3.0 correspond au commit `3717a58` de `develop`, qui ne change que les numéros de version (`pyproject.toml`, `server.json`). | `git ls-remote` ; `git diff main develop` |
| Archive PyPI vs dépôt | `__init__.py` et `server.py` **identiques octet pour octet** (wheel et sdist) au dépôt ; seule différence : `version = "0.3.0"` dans `pyproject.toml`. Le wheel ne contient que `__init__.py`, `server.py` et les métadonnées ; point d'entrée identique. | `diff` |
| Licence | MIT, « Copyright (c) 2025 Piotr Mrzygłosz ». Le champ `license` n'est pas renseigné dans les métadonnées PyPI. | `LICENSE:1-3` |
| Mainteneurs | Auteur déclaré : Piotr Mrzygłowski `<piotr@epochal.dev>` (`pyproject.toml:5-7`). Contributeurs GitHub : `PiotrAleksander` (15 commits) et `Copilot` (5 commits, code initial généré par l'agent Copilot, PR #1). **Propriétaire du projet PyPI : compte `WorldsDerived`**, différent du compte GitHub ; aucune publication de confiance (OIDC) visible pour PyPI (le workflow publie avec un jeton, `.github/workflows/publish-mcp.yml:40-43`). Le contenu publié étant identique au dépôt, cela ne change rien pour 0.3.0, mais rien ne garantit les versions futures. | API PyPI, API GitHub |
| Activité | 15 commits entre le 2025-12-09 et le 2025-12-22, **plus rien depuis** (≈ 11 mois). 49 étoiles, 13 forks. 8 issues/PR ouvertes non traitées, dont les deux bloquants ci-dessous (#11 crash avec `mcp>=2`, #7 et #10 `create_source` cassé ; la PR de correction #9 a été fermée sans fusion). | API GitHub |

## 2. Dépendances, lancement, transport, variables

- Dépendances : `httpx>=0.28.1`, `mcp[cli]>=1.23.2`, Python `>=3.12` (`pyproject.toml:9-13`). Le `uv.lock` fige `mcp 1.23.2` et `httpx 0.28.1`, mais il n'est pas utilisé par `pip`.
- **Bloquant n°1 : aucune borne haute sur `mcp`.** La dernière version de `mcp` est 2.3.0 (2026-10-02). En 2.x, `mcp.server.fastmcp` est un module piège qui lève `ModuleNotFoundError` (« pin 'mcp<2' to keep running v1 code », `mcp/server/fastmcp.py` du wheel 2.3.0). Or `server.py:11` fait `from mcp.server.fastmcp import FastMCP`. Un `pip install open-notebook-mcp` aujourd'hui installe `mcp` 2.3.0 et **le serveur plante au démarrage** (issue #11). Il faut contraindre `mcp<2` (dernière 1.x : 1.30.0).
- Commande : `open-notebook-mcp` → `open_notebook_mcp:main` (`pyproject.toml:24-25` ; `__init__.py:1` ; `server.py:1285`).
- Transport : **stdio par défaut** (`server.py:1288-1292`). Mode `MCP_TRANSPORT=streamable-http` prévu (`server.py:1294-1308`), mais il passe `host`, `port`, `path`… à `FastMCP.run()`, qui n'accepte que `transport` et `mount_path` en `mcp` 1.x (`mcp/server/fastmcp/server.py:295-299` du wheel 1.30.0) : **le mode HTTP lève `TypeError`** (issue #6). Seul stdio fonctionne.
- Variables lues :

| Variable | Défaut | Rôle | Où |
|---|---|---|---|
| `OPEN_NOTEBOOK_URL` | `http://localhost:5055` | base de l'API | `server.py:28-30` |
| `OPEN_NOTEBOOK_PASSWORD` | aucun | envoyé en `Authorization: Bearer …` | `server.py:32-34,458-461` |
| `MCP_TRANSPORT` | `stdio` | transport | `server.py:1288` |
| `HOST`, `PORT`, `MCP_PATH`, `STATELESS_HTTP`, `JSON_RESPONSE` | `127.0.0.1`, `8000`, `/mcp`, `1`, `1` | mode HTTP (cassé) | `server.py:1295-1299` |

  Pas de lecture de fichier `.env` par le serveur lui-même ; les variables doivent venir du client MCP.

## 3. Outils exposés et compatibilité avec l'API 1.15.1

33 outils (`@mcp.tool`). Toutes les requêtes passent par `make_request` (`server.py:434-499`) : JSON, délai **30 s** (`server.py:26,463`), redirections suivies, liste tronquée côté client pour les `limit`. Renvois Open Notebook = `api/routers/*.py` au tag v1.15.1.

| Outil (`server.py`) | Paramètres | Route appelée | Compatibilité 1.15.1 |
|---|---|---|---|
| `search_capabilities` (:381) | `query`, `detail`, `limit` | aucune (index local `CAPABILITIES`, :58-363) | OK |
| `list_notebooks` (:506) | `archived`, `order_by`, `limit` | GET `/api/notebooks` | OK (`notebooks.py:61`) |
| `get_notebook` (:539) | `notebook_id` | GET `/api/notebooks/{id}` | OK (`:238`) |
| `create_notebook` (:555) | `name`, `description` | POST `/api/notebooks` | OK (`:128`) |
| `update_notebook` (:576) | `notebook_id`, `name`, `description`, `archived` | PUT `/api/notebooks/{id}` | OK (`:278`) |
| `delete_notebook` (:608) | `notebook_id` | DELETE `/api/notebooks/{id}` | OK (`:419`), sources exclusives conservées (défaut `delete_exclusive_sources=false`) |
| `list_sources` (:628) | `notebook_id`, `limit`, `offset` | GET `/api/sources` | OK (`sources.py:257`) |
| `get_source` (:656) | `source_id` | GET `/api/sources/{id}` | OK (`:755`) |
| `create_source` (:672) | `notebook_id`, `type`, `url`, `title`, `embed` | POST `/api/sources` en **JSON** | **Cassé** : la route n'accepte que des champs de formulaire (`sources.py:186-198,639-644`) → 422. Il faudrait `/api/sources/json` (`:708`). De plus aucun paramètre `content` (type `text` impossible) ni fichier (type `upload` impossible). Issues #7, #10. |
| `update_source` (:708) | `source_id`, `title`, `topics` | PUT `/api/sources/{id}` | OK (`:905`) |
| `delete_source` (:736) | `source_id` | DELETE `/api/sources/{id}` | OK (`:1055`) |
| `list_notes` (:756) | `notebook_id`, `limit`, `offset` | GET `/api/notes` | OK (`notes.py:17`) ; `limit`/`offset` ignorés par l'API |
| `get_note` (:784) | `note_id` | GET `/api/notes/{id}` | OK (`:121`) |
| `create_note` (:800) | `notebook_id`, `title`, `content`, `topics` | POST `/api/notes` | OK (`:55`) ; `topics` n'existe pas dans `NoteCreate` (`api/models.py:218-224`), ignoré |
| `update_note` (:832) | `note_id`, `title`, `content`, `topics` | PUT `/api/notes/{id}` | OK (`:146`), `topics` ignoré |
| `delete_note` (:864) | `note_id` | DELETE `/api/notes/{id}` | OK (`:189`) |
| `search` (:884) | `query`, `type` (défaut `vector`), `notebook_id`, `limit` ≤ 50 | POST `/api/search` | OK (`search.py:25`) |
| `ask_question` (:917) | `question`, 3 IDs de modèles, `notebook_id` | POST `/api/search/ask` | Route présente (`search.py:140`) mais elle **répond en SSE** : le texte brut du flux est renvoyé dans `content` (`server.py:482-487`). Délai de 30 s presque toujours dépassé avec un LLM local (jusqu'à 5 recherches + 3 appels LLM). |
| `ask_simple` (:952) | idem | POST `/api/search/ask/simple` | OK (`search.py:202`) mais même limite de 30 s |
| `list_models` (:991) | `limit` | GET `/api/models` | OK (`models.py:173`) |
| `get_model` (:1013) | `model_id` | GET `/api/models/{id}` | **N'existe pas** en 1.15.1 (seuls DELETE `/models/{id}` et POST `/models/{id}/test`, `models.py:262,282`) → 405 |
| `create_model` (:1029) | `name`, `provider`, `type` | POST `/api/models` | OK (`models.py:205`), sans lien `credential` |
| `delete_model` (:1053) | `model_id` | DELETE `/api/models/{id}` | OK (`:262`) |
| `get_default_models` (:1069) | — | GET `/api/models/defaults` | OK (`:307`) |
| `list_chat_sessions` (:1086) | `notebook_id` (optionnel), `limit` | GET `/api/chat/sessions` | OK si `notebook_id` fourni ; il est **obligatoire** côté API (`chat.py:98`) → 422 sinon |
| `create_chat_session` (:1116) | `notebook_id`, `title` | POST `/api/chat/sessions` | OK (`chat.py:142`) |
| `get_chat_session` (:1138) | `session_id` | GET `/api/chat/sessions/{id}` | OK (`chat.py:182-184`) |
| `update_chat_session` (:1154) | `session_id`, `title` | PUT `/api/chat/sessions/{id}` | OK (`:240`) |
| `delete_chat_session` (:1178) | `session_id` | DELETE `/api/chat/sessions/{id}` | OK (`:287`) |
| `execute_chat` (:1194) | `session_id`, `message`, `context` (optionnel) | POST `/api/chat/execute` | Route OK (`chat.py:308`) mais `context` est **obligatoire** côté API (`chat.py:73-75`) → 422 si omis ; et 30 s de délai trop court pour un LLM local |
| `get_chat_context` (:1223) | `notebook_id`, `context_config` (optionnel) | POST `/api/chat/context` | OK (`chat.py:395`) si `context_config` fourni ; obligatoire côté API (`chat.py:88`) → 422 sinon |
| `get_settings` (:1253) | — | GET `/api/settings` | OK (`settings.py:14`) |
| `update_settings` (:1266) | `settings` (dict libre) | PUT `/api/settings` | OK (`settings.py:39`) |

Routes supprimées : le paquet **n'appelle pas** `POST /api/commands/jobs` (supprimé en 1.15.1, `CHANGELOG.md:28-29`) ni aucune route `/api/commands`. La seule route appelée absente de 1.15.1 est GET `/api/models/{id}`.

Bilan : lecture des carnets, sources, notes, recherche, modèles et sessions fonctionne ; `create_source` et `get_model` sont cassés ; `ask_*` et `execute_chat` sont limités par le délai de 30 s et par des paramètres requis présentés comme facultatifs. Aucun outil pour le statut de traitement, l'embedding, les transformations, les insights, les podcasts.

## 4. Sécurité

| Point | Constat | Où |
|---|---|---|
| Appels réseau | Uniquement `httpx` vers `OPEN_NOTEBOOK_URL` + chemin `/api/...`. Aucune autre URL dans le code du paquet. Les URL externes du dépôt sont dans `.devcontainer/` (pare-feu, outils), le workflow CI et la documentation, hors archive PyPI. | `server.py:455-472` |
| Redirections | `follow_redirects=True`. `httpx` retire l'en-tête `Authorization` si la redirection change d'origine ; risque faible avec une URL locale. | `server.py:463` |
| Télémétrie | Aucune dans le paquet. (Le SDK `mcp` 2.x dépend d'`opentelemetry-api`, sans exportateur ; non concerné avec `mcp<2`.) | — |
| Fichiers | Aucune écriture ni lecture de fichier, aucun `open()`. | `grep` |
| Exécution | Aucun `subprocess`, `os.system`, `eval`, `exec`, `compile`, `importlib`, `pickle`, `base64`. Code lisible, non obscurci. | `grep` |
| Mot de passe | Lu dans l'environnement, envoyé seulement en en-tête Bearer ; jamais journalisé (le journal `INFO` de `httpx` affiche l'URL, pas les en-têtes ; `server.py:13`). Il figure en clair dans la configuration du client MCP (variable `env`). | `server.py:32-34,458-461` |
| Messages d'erreur | Le `detail` de l'API est relayé au client (`server.py:489-499`) : pas de fuite du mot de passe. | — |
| Outils destructifs | `delete_notebook`, `delete_source`, `delete_note`, `delete_model`, `delete_chat_session` exposés **sans confirmation**. `update_settings` accepte un dictionnaire libre : un agent pourrait remettre le moteur d'URL en `auto` (repli vers Jina Reader, voir [relecture.md](relecture.md) point 9). | `server.py:608,736,864,1053,1178,1266` |
| Mode HTTP | Si un jour réparé, le `Makefile` le lance sur `0.0.0.0` sans authentification MCP. Ne pas l'utiliser. | `Makefile:10` |
| Fichiers hors archive | `examples.py`, `tests/`, `.devcontainer/` (pare-feu `iptables`, téléchargements GitHub), `Makefile` (cibles `bump-*` qui réécrivent `pyproject.toml`) ne sont pas dans le wheel. | — |

## 5. Verdict

**Installable sans risque pour un essai local, à deux conditions** : brider `mcp<2` (sinon plantage au démarrage) et n'utiliser que le transport stdio. Le code est court, lisible, sans réseau tiers, sans écriture de fichier ni exécution de commande ; l'archive PyPI est identique au dépôt. Ce n'est en revanche **pas un outil fiable pour le projet** : abandonné depuis décembre 2025, publié sur PyPI par un compte distinct de l'auteur, `create_source` et `get_model` cassés, délai de 30 s incompatible avec un LLM local pour `ask_*`/`execute_chat`. Pour un essai : lecture et recherche seulement, sur un carnet de test, en évitant les outils `delete_*` et `update_settings`.

### Installation bornée (non exécutée)

Depuis la racine du projet, dans un environnement séparé du reste :

```bash
python3.12 -m venv .venv-mcp
.venv-mcp/bin/pip install 'open-notebook-mcp==0.3.0' 'mcp[cli]>=1.23.2,<2' 'httpx==0.28.1'
.venv-mcp/bin/pip show mcp | grep Version   # doit afficher 1.x
```

Le wheel vérifié (sha256 ci-dessus) peut aussi être installé à la place du nom : `pip install /chemin/open_notebook_mcp-0.3.0-py3-none-any.whl 'mcp[cli]>=1.23.2,<2'`.

### Essai sans client graphique (SDK `mcp` 1.x en client stdio)

Script à placer hors du dossier du paquet (par exemple `outils/open-notebook/essai_mcp.py`) et à lancer avec `.venv-mcp/bin/python -I outils/open-notebook/essai_mcp.py`. Il lit le mot de passe dans `donnees/open-notebook/.env`, comme `outils/open-notebook/client.py`, et le passe au serveur par `env` (le client stdio ne transmet sinon que `HOME`, `PATH`… au sous-processus).

```python
"""Essai minimal du serveur MCP open-notebook-mcp en stdio : liste des outils puis un appel en lecture."""
import asyncio, json, sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

RACINE = Path(__file__).resolve().parents[2]
ENV = dict(l.split("=", 1) for l in (RACINE / "donnees/open-notebook/.env").read_text().splitlines()
           if "=" in l and not l.startswith("#"))

PARAMS = StdioServerParameters(
    command=str(Path(sys.executable).with_name("open-notebook-mcp")),
    env={"OPEN_NOTEBOOK_URL": "http://127.0.0.1:5055",
         "OPEN_NOTEBOOK_PASSWORD": ENV["OPEN_NOTEBOOK_PASSWORD"]},
)


async def main():
    async with stdio_client(PARAMS) as (lecture, ecriture):
        async with ClientSession(lecture, ecriture) as session:
            await session.initialize()
            outils = (await session.list_tools()).tools
            print(len(outils), "outils :", ", ".join(o.name for o in outils))
            assert any(o.name == "list_notebooks" for o in outils)
            res = await session.call_tool("list_notebooks", {"limit": 5})
            assert not res.isError, res.content
            print(json.dumps(json.loads(res.content[0].text), indent=2, ensure_ascii=False)[:2000])


asyncio.run(main())
```

Résultat attendu : `33 outils : …` puis la liste des carnets. Un second appel en lecture possible : `search` avec `{"query": "…", "type": "text", "limit": 5}`.

Pour le brancher ensuite à un client MCP (Claude Code, par exemple) : commande `<projet>/.venv-mcp/bin/open-notebook-mcp`, variables `OPEN_NOTEBOOK_URL=http://127.0.0.1:5055` et `OPEN_NOTEBOOK_PASSWORD`, transport stdio.
