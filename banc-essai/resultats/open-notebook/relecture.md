# Relecture avant installation — Open Notebook 1.15.1

Date : 2026-11-08. Lecture seule du dépôt `lfnovo/open-notebook` au tag `v1.15.1` (commit `5e285b7`), aucun code du dépôt exécuté hors des images Docker officielles. Synthèse détaillée avec renvois `fichier:ligne` : [cadrage-source.md](cadrage-source.md).

## Ce qui a été relu

| Élément | Fichier | Empreinte ou version |
|---|---|---|
| Compose officiel | `docker-compose.yml` (copie dans `outils/open-notebook/officiel/`) | sha256 `8ef83d69d06a…e17034` |
| Exemple de variables | `.env.example` (copie dans `outils/open-notebook/officiel/env.example`) | sha256 `bf7ff20e203e…392779` |
| Image de l'application | `lfnovo/open_notebook:1.15.1` | `sha256:e4e18f12653df5bf48674b7b187c4252be52238b4d706330fd30d9b177b95812`, 2,46 Go, construite le 2026-11-04 |
| Image de la base | `surrealdb/surrealdb:v2.7.0` (le compose officiel utilise l'étiquette flottante `v2`, qui pointe le 2026-11-08 sur la même empreinte) | `sha256:e5d7387e3727bbe2f7cd6d869e48cd34777272258572ead37c9656b25f745723` |
| Entrée du conteneur, supervisord, Dockerfile | `scripts/docker-entrypoint.sh`, `supervisord.conf`, `Dockerfile` | tag v1.15.1 |
| Authentification, CORS, routes | `api/auth.py`, `api/main.py`, `api/routers/*.py` | tag v1.15.1 |

## Points relevés et décision

| N° | Point | Décision dans ce dépôt |
|---|---|---|
| 1 | Ports 8502 et 5055 publiés sur toutes les interfaces ; API et interface écoutent sur `0.0.0.0` dans le conteneur. | Override : `127.0.0.1:8502` et `127.0.0.1:5055`. Vérifié après démarrage (`docker ps`). |
| 2 | Aucune authentification sans `OPEN_NOTEBOOK_PASSWORD`. | Mot de passe aléatoire généré (`openssl rand -hex 12`), rangé dans `donnees/IDENTIFIANTS-LOCAUX.txt`. |
| 3 | `/docs`, `/openapi.json`, `/health`, `/api/config` restent sans authentification. | Accepté (écoute locale seulement) ; signalé dans le manuel Exploitation. |
| 4 | Mot de passe stocké en clair dans le `localStorage` du navigateur. | Signalé dans le manuel Exploitation. |
| 5 | Clé de chiffrement d'exemple dans le compose ; sel PBKDF2 fixe commun. | Clé aléatoire de 256 bits (`openssl rand -hex 32`). |
| 6 | SurrealDB `root:root` par défaut, port publié sur 127.0.0.1:8000. | Identifiants générés ; port non publié (inutile, et 8000 est le port prévu pour vLLM dans le socle type). |
| 7 | `pull_policy: always` : nouvelle image à chaque démarrage. | `pull_policy: missing` et images figées par empreinte. |
| 8 | Appel sortant vers `raw.githubusercontent.com` à chaque `/api/config` (vérification de version, cache 24 h), sans option pour le couper. | Accepté, signalé. |
| 9 | Extraction d'URL en mode `auto` : repli possible vers Jina Reader (service tiers) sans clé. | Moteur d'URL réglé sur `simple` par `configurer.py`. |
| 10 | Docling (OCR des scans) et Crawl4AI s'installent au démarrage depuis PyPI et Hugging Face si activés. | Désactivés par défaut ; Docling essayé séparément et mesuré. |
| 11 | `Dockerfile` : `curl … nodesource | bash` au build, `uv:latest` non figé. | Concerne la construction de l'image par le projet, pas l'installation ici ; reproductibilité garantie par l'empreinte de l'image. |
| 12 | Liaison source-carnet non idempotente (arête en double si on relie deux fois). | Les scripts ne relient une source qu'une fois, à la création. |
| 13 | Le worker lit `SURREAL_NAMESPACE`/`SURREAL_DATABASE` avec un défaut `test` différent de l'API. | Variables fixées explicitement (comme le compose officiel). |
| 14 | Aucune bibliothèque de télémétrie trouvée. | Rien à faire. |
| 15 | Pas de serveur MCP officiel ; la documentation renvoie au paquet tiers `open-notebook-mcp`. | Relecture du paquet tiers avant tout essai (manuel API REST et MCP). |
