# Open Notebook v1.15.1 — cadrage par lecture du code source

- Dépôt : `https://github.com/lfnovo/open-notebook`, tag `v1.15.1` (commit `5e285b7`, « chore(release): 1.15.1 (#1541) »), cloné en `--depth 1`, lu sans rien exécuter.
- Version déclarée : `pyproject.toml:3` → `version = "1.15.1"`.
- Image Docker : la CI pousse le tag **sans `v`** : `lfnovo/open_notebook:1.15.1` (et `1.15.1-single` pour la variante tout-en-un avec SurrealDB embarqué), plus `v1-latest` pour les releases stables (`.github/workflows/build-and-release.yml:30-36` extraction de version depuis `pyproject.toml`, `:103` et `:117` construction des tags, `:195`/`:210` variante `-single`).
- Toutes les références sont de la forme `fichier:ligne`, chemins relatifs à la racine du dépôt.

---

## 1. Déploiement Docker

### 1.1 `docker-compose.yml` officiel (contenu exact, `docker-compose.yml:1-62`)

```yaml
services:
  surrealdb:
    image: surrealdb/surrealdb:v2
    # Credentials default to root:root for a zero-config local setup. Before
    # exposing this instance to a network, set SURREAL_USER / SURREAL_PASSWORD
    # in a .env file (see .env.example) — they are applied here and to the
    # open_notebook service below, so the two always stay in sync.
    # List (exec) form so each interpolated value stays a single argument —
    # a password containing spaces would otherwise be split into several.
    command: ["start", "--log", "info", "--user", "${SURREAL_USER:-root}", "--pass", "${SURREAL_PASSWORD:-root}", "rocksdb:/mydata/mydatabase.db"]
    user: root  # Required for bind mounts on Linux
    ports:
      # Bound to localhost only: the open_notebook service reaches this over
      # the internal compose network regardless, so the host port is purely
      # for local debugging (e.g. Surrealist, `surreal sql`). Exposing this
      # on 0.0.0.0 would let anyone who can reach the host connect with the
      # default root:root credentials.
      - "127.0.0.1:8000:8000"
    volumes:
      - ./surreal_data:/mydata
    environment:
      - SURREAL_EXPERIMENTAL_GRAPHQL=true
    restart: always
    pull_policy: always

  open_notebook:
    image: lfnovo/open_notebook:v1-latest
    ports:
      - "8502:8502"  # Web UI
      - "5055:5055"  # REST API
    environment:
      # REQUIRED: Change this to your own secret string
      # This encrypts your API keys in the database
      - OPEN_NOTEBOOK_ENCRYPTION_KEY=change-me-to-a-secret-string

      # Database connection. SURREAL_USER / SURREAL_PASSWORD default to root:root
      # for local use; override them in a .env file before exposing the instance
      # (the same values configure the surrealdb service above).
      - SURREAL_URL=ws://surrealdb:8000/rpc
      - SURREAL_USER=${SURREAL_USER:-root}
      - SURREAL_PASSWORD=${SURREAL_PASSWORD:-root}
      - SURREAL_NAMESPACE=open_notebook
      - SURREAL_DATABASE=open_notebook

      # OPTIONAL: heavy extraction runtimes, installed on first startup when
      # enabled (downloads are cached on the ./notebook_data volume, so only the
      # first boot is slow). See docs/5-CONFIGURATION/environment-reference.md.
      # - OPEN_NOTEBOOK_ENABLE_DOCLING=true    # Docling engine + OCR + image sources (large ML stack)
      # - OPEN_NOTEBOOK_ENABLE_CRAWL4AI=true   # local Crawl4AI (bundles a Chromium browser)
      # - CRAWL4AI_API_URL=http://crawl4ai:11235  # use a remote Crawl4AI server instead (no local install)
      # - CRAWL4AI_API_TOKEN=${CRAWL4AI_API_TOKEN}  # bearer token for that server (required by Crawl4AI >= 0.9.0)

      # OPTIONAL: max concurrent background tasks the worker processes at once
      # (default 5). Set to 1 for sequential processing on single-GPU / local
      # LLM setups to avoid overloading the model with parallel requests.
      # - OPEN_NOTEBOOK_WORKER_MAX_TASKS=1
    volumes:
      - ./notebook_data:/app/data
    depends_on:
      - surrealdb
    restart: always
    pull_policy: always
```

Points clés :

| Élément | Valeur | Source |
|---|---|---|
| Image SurrealDB | `surrealdb/surrealdb:v2` (tag flottant majeur v2, pas de version figée) | `docker-compose.yml:3` ; le binaire de l'image `-single` est aussi copié depuis `surrealdb/surrealdb:v2` (`Dockerfile:66`) |
| Stockage SurrealDB | RocksDB, `rocksdb:/mydata/mydatabase.db`, volume `./surreal_data:/mydata` | `docker-compose.yml:10,20` |
| Port SurrealDB | `127.0.0.1:8000:8000` (localhost seulement) | `docker-compose.yml:18` |
| Ports Open Notebook | `8502` (UI Next.js) et `5055` (API FastAPI), **publiés sur toutes les interfaces** | `docker-compose.yml:29-30` |
| Volume données appli | `./notebook_data:/app/data` (uploads, podcasts, checkpoints SQLite du chat, caches) | `docker-compose.yml:58` ; dossiers créés par `open_notebook/config.py:5-20` |
| Image appli | `lfnovo/open_notebook:v1-latest` → à remplacer par `lfnovo/open_notebook:1.15.1` pour figer | `docker-compose.yml:27` |
| `pull_policy: always` | sur les deux services : re-tire l'image à chaque `up` | `docker-compose.yml:24,62` |

Processus dans le conteneur (supervisord, `supervisord.conf`) :
- `api` : `uvicorn api.main:app --host %(ENV_API_HOST)s --port 5055` (`supervisord.conf:12`), avec `ENV API_HOST=0.0.0.0` dans l'image (`Dockerfile:107`).
- `worker` : `surreal-commands-worker --import-modules commands --max-tasks ${OPEN_NOTEBOOK_WORKER_MAX_TASKS:-5}` (`supervisord.conf:25`). C'est lui qui traite sources, embeddings, insights et podcasts.
- `frontend` : `node server.js`, `HOSTNAME=${FRONTEND_BIND_HOST:-0.0.0.0}`, port 8502, variables passées `API_URL,NEXT_PUBLIC_API_URL,INTERNAL_API_URL` (`supervisord.conf:39-42`).
- Entrée : `scripts/docker-entrypoint.sh` installe Docling / Crawl4AI au démarrage si `OPEN_NOTEBOOK_ENABLE_DOCLING` / `OPEN_NOTEBOOK_ENABLE_CRAWL4AI` sont vrais (`scripts/docker-entrypoint.sh:58-113`), puis lance supervisord (`Dockerfile:140-141`).
- Migrations de schéma SurrealDB lancées automatiquement au démarrage de l'API, avec 12 tentatives de connexion (`api/main.py:85-87,164-180,202-208`). Dernière migration : `open_notebook/database/migrations/25.surrealql`.

Exemple Ollama officiel (`examples/docker-compose-ollama.yml:29-55`) : ajoute un service `ollama/ollama:latest` publié sur `11434:11434` et met `OLLAMA_API_BASE=http://ollama:11434` (variable de repli dépréciée) ; le commentaire `:11` indique de configurer Ollama dans l'UI avec l'URL `http://ollama:11434`.

**Pour le banc (Ollama dans un conteneur `rag-ollama`)** : le conteneur `open_notebook` doit être sur le même réseau Docker que `rag-ollama` (réseau externe déclaré dans le compose), sinon le nom ne résout pas. La Base URL à donner est `http://rag-ollama:11434` pour le fournisseur `ollama` (`docs/5-CONFIGURATION/ollama.md:48-55`), ou `http://rag-ollama:11434/v1` pour `openai_compatible` (`docs/5-CONFIGURATION/openai-compatible.md:11-31`, la doc exige le chemin d'API, en général `/v1`).

### 1.2 Variables d'environnement obligatoires et utiles

Obligatoires en pratique :

| Variable | Rôle | Source |
|---|---|---|
| `OPEN_NOTEBOOK_ENCRYPTION_KEY` (ou `_FILE`) | Clé (n'importe quelle chaîne) dérivée en clé Fernet par PBKDF2-HMAC-SHA256 600 000 itérations, sel fixe `open-notebook-credential-v1`. Sans elle, création de credential refusée (`require_encryption_key`) ; l'API démarre quand même avec un avertissement. | `open_notebook/utils/encryption.py:64-118` ; `api/main.py:193-198` ; `api/routers/credentials.py:172` |
| `SURREAL_URL` | `ws://surrealdb:8000/rpc` | `open_notebook/database/repository.py:42-51` |
| `SURREAL_USER` | Aucun défaut côté API (signin échoue) ; `test` côté file de jobs | `open_notebook/database/repository.py:92` ; `docs/5-CONFIGURATION/environment-reference.md:59` |
| `SURREAL_PASSWORD` (alias `SURREAL_PASS`) | défaut `root` côté API, `test` côté jobs | `open_notebook/database/repository.py:56` ; `environment-reference.md:60` |
| `SURREAL_NAMESPACE`, `SURREAL_DATABASE` | défaut `open_notebook` côté API, **`test` côté worker** → à toujours fixer explicitement, sinon les jobs ne sont jamais traités | `open_notebook/database/repository.py:59-66` ; `docs/5-CONFIGURATION/database.md:17` |

Utiles pour le banc :

| Variable | Défaut | Rôle | Source |
|---|---|---|---|
| `OPEN_NOTEBOOK_PASSWORD` (ou `_FILE`) | non défini = auth désactivée | Mot de passe UI + API (Bearer) | `api/auth.py:24,37-38` |
| `CORS_ORIGINS` | `*` | Origines autorisées | `api/main.py:73-80` |
| `API_URL` | auto (`http://<hôte de la page>:5055`) | Adresse de l'API **vue par le navigateur** (frontend) | `frontend/src/app/config/route.ts:65` ; `environment-reference.md:74` |
| `INTERNAL_API_URL` | `http://localhost:5055` | Où le serveur Next.js relaie `/api/*` | `frontend/next.config.ts:32` |
| `API_HOST` | `0.0.0.0` (image) / `127.0.0.1` (source) | Interface d'écoute de l'API | `Dockerfile:107` ; `run_api.py:18` |
| `FRONTEND_BIND_HOST` | `0.0.0.0` | Interface d'écoute Next.js | `supervisord.conf:39` |
| `OPEN_NOTEBOOK_WORKER_MAX_TASKS` | `5` | Jobs parallèles du worker ; `1` recommandé avec Ollama mono-GPU | `supervisord.conf:25` ; `docs/5-CONFIGURATION/ollama.md:142` |
| `ESPERANTO_LLM_TIMEOUT` | `180` (forcé par l'appli si vide) | Timeout de chaque appel LLM (s) | `open_notebook/config.py:38-47` |
| `ESPERANTO_EMBEDDING_TIMEOUT` | `60` | Timeout embedding | `environment-reference.md:108` |
| `OPEN_NOTEBOOK_CHUNK_SIZE` | `400` tokens (min 100) | Taille des chunks | `open_notebook/utils/chunking.py:33-57` |
| `OPEN_NOTEBOOK_CHUNK_OVERLAP` | 15 % de la taille (60) | Recouvrement | `open_notebook/utils/chunking.py:60-85` |
| `OPEN_NOTEBOOK_MIN_CHUNK_SIZE` | `5` tokens | Chunks plus courts ignorés | `open_notebook/utils/chunking.py:88-112` |
| `OPEN_NOTEBOOK_EMBEDDING_BATCH_SIZE` | `50` | Textes par requête d'embedding | `open_notebook/utils/embedding.py:31` |
| `OPEN_NOTEBOOK_MAX_UPLOAD_SIZE_MB` | `100` | Taille max de corps de requête | `api/middleware.py:9-31` |
| `LOGURU_LEVEL` | `DEBUG` | Verbosité | `environment-reference.md:214` |
| `OLLAMA_API_BASE` | — (déprécié) | Repli si aucun credential Ollama en base | `open_notebook/ai/provider_registry.py:256-261` ; `api/credentials_service.py:137` |
| `OPENAI_COMPATIBLE_BASE_URL`, `OPENAI_COMPATIBLE_API_KEY` (+ suffixes `_LLM`, `_EMBEDDING`, `_STT`, `_TTS`) | — (déprécié) | Repli OpenAI compatible | `api/routers/models.py:166-169` ; `open_notebook/ai/model_discovery.py:744-746` |

### 1.3 Liste complète des variables lues par le code Python (grep `os.environ` / `getenv`, hors tests)

| Variable | Fichier:ligne | Rôle |
|---|---|---|
| `SURREAL_URL` | `open_notebook/database/repository.py:42` ; `open_notebook/utils/proxy.py:55` | URL WebSocket SurrealDB ; aussi ajoutée à `NO_PROXY` |
| `SURREAL_ADDRESS`, `SURREAL_PORT` | `repository.py:48,50` ; `proxy.py:57` | Repli historique si `SURREAL_URL` absent |
| `SURREAL_USER` | `repository.py:92` | Utilisateur DB |
| `SURREAL_PASSWORD`, `SURREAL_PASS` | `repository.py:56` | Mot de passe DB (défaut `root`) |
| `SURREAL_NAMESPACE`, `SURREAL_DATABASE` | `repository.py:36` via `_get_env_or_default` (`:59-66`) | Namespace / base |
| `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` (et minuscules) | `open_notebook/utils/proxy.py:99,118` | Proxy sortant ; l'appli ajoute les hôtes SurrealDB à `NO_PROXY` |
| `CORS_ORIGINS` | `api/main.py:73` | CORS |
| `API_HOST`, `API_PORT`, `API_RELOAD` | `run_api.py:18-20` | Lancement depuis les sources uniquement (l'image fixe 5055) |
| `TIKTOKEN_CACHE_DIR` | `open_notebook/config.py:27` ; `open_notebook/utils/token_utils.py:12` | Cache d'encodage tiktoken (`o200k_base`, `token_utils.py:28`) |
| `ESPERANTO_LLM_TIMEOUT` | `open_notebook/config.py:43-44` | Timeout LLM, mis à 180 s si vide |
| `OPEN_NOTEBOOK_ENCRYPTION_KEY[_FILE]`, `OPEN_NOTEBOOK_PASSWORD[_FILE]` | `open_notebook/utils/encryption.py:44,61` (fonction générique `get_secret_from_env`) | Secrets ; la variante `_FILE` est prioritaire |
| `OPEN_NOTEBOOK_MAX_UPLOAD_SIZE_MB` | `api/middleware.py:20` | Taille max |
| `OPEN_NOTEBOOK_CHUNK_SIZE`, `OPEN_NOTEBOOK_CHUNK_OVERLAP`, `OPEN_NOTEBOOK_MIN_CHUNK_SIZE` | `open_notebook/utils/chunking.py:35,62,97` | Découpage |
| `OPEN_NOTEBOOK_EMBEDDING_BATCH_SIZE` | `open_notebook/utils/embedding.py:31` | Lot d'embeddings |
| `ESPERANTO_SSL_CA_BUNDLE`, `ESPERANTO_SSL_VERIFY` | `open_notebook/utils/ssl_config.py:34,40` (noms des constantes) | TLS vers fournisseurs |
| `CRAWL4AI_API_URL` | `open_notebook/utils/runtime_capabilities.py:49,54` | Crawl4AI distant |
| `PLAYWRIGHT_BROWSERS_PATH`, `LOCALAPPDATA` | `runtime_capabilities.py:62,80` | Détection Chromium |
| Clés fournisseurs `<PROVIDER>_API_KEY` (OPENAI, ANTHROPIC, GOOGLE/GEMINI, GROQ, MISTRAL, DEEPSEEK, XAI, OPENROUTER, DASHSCOPE, MINIMAX, NOVITA, SILICONFLOW, ZAI, PPQ, COHERE, VOYAGE, ELEVENLABS, DEEPGRAM) et `*_BASE_URL` | `open_notebook/ai/key_provider.py:127,155-167,263-267` ; `open_notebook/ai/model_discovery.py:308-316,428,452,588,610,645,692` ; `api/credentials_service.py:172-203` | Repli déprécié par variables d'env ; **les credentials stockés en base sont réinjectés dans `os.environ`** au provisioning (`key_provider.py:155-267`) |
| `OLLAMA_API_BASE` | `open_notebook/ai/model_discovery.py:495` (défaut `http://localhost:11434`) ; `api/credentials_service.py:137` | Repli Ollama |
| `OMLX_API_BASE`, `OMLX_API_KEY` | `model_discovery.py:881-883` ; `credentials_service.py:140-146` | oMLX |
| `OPENAI_COMPATIBLE_BASE_URL[_LLM/_EMBEDDING/_STT/_TTS]`, `OPENAI_COMPATIBLE_API_KEY[...]` | `api/routers/models.py:166-169` ; `model_discovery.py:744-746` | OpenAI compatible (repli) |
| `ANTHROPIC_COMPATIBLE_BASE_URL`, `ANTHROPIC_COMPATIBLE_API_KEY` | `open_notebook/ai/models.py:61-62` ; `api/routers/models.py:456-457` | Anthropic compatible |
| `AZURE_OPENAI_*` (API_KEY, ENDPOINT, API_VERSION, ENDPOINT_LLM/EMBEDDING/STT/TTS, suffixes `_<MODE>`) | `api/routers/models.py:141-150` ; `open_notebook/ai/connection_tester.py:100-102` ; `key_provider.py:216-242` | Azure |
| `VERTEX_PROJECT`, `VERTEX_LOCATION`, `GOOGLE_APPLICATION_CREDENTIALS` | `key_provider.py:187-195` ; `credentials_service.py:153-155` ; `api/routers/models.py:433` | Vertex |

Variables lues **hors code Python de l'appli** (bibliothèques, shell, frontend) — la liste complète documentée est `docs/5-CONFIGURATION/environment-reference.md` :
- Shell / supervisord : `OPEN_NOTEBOOK_WORKER_MAX_TASKS` (`supervisord.conf:25`), `FRONTEND_BIND_HOST` (`:39`), `OPEN_NOTEBOOK_ENABLE_DOCLING`, `OPEN_NOTEBOOK_ENABLE_CRAWL4AI`, `UV_CACHE_DIR`, `PLAYWRIGHT_BROWSERS_PATH`, `HF_HOME` (`scripts/docker-entrypoint.sh:49-51,58,76-77`).
- Frontend : `API_URL`, `NEXT_PUBLIC_API_URL` (`frontend/src/app/config/route.ts:65`), `INTERNAL_API_URL` (`frontend/next.config.ts:32`, `frontend/src/app/api/_sse-proxy.ts:3`), `NEXT_PUBLIC_API_TIMEOUT_MS` (compilé au build, `frontend/src/lib/api/client.ts:16`), `NEXT_ALLOWED_DEV_ORIGINS` (dev).
- Bibliothèques (esperanto, content-core, surreal-commands, podcast-creator, LangSmith) : `ESPERANTO_EMBEDDING_TIMEOUT`, `ESPERANTO_TTS_TIMEOUT`, `ESPERANTO_STT_TIMEOUT`, `CCORE_STT_TIMEOUT`, `CCORE_AUDIO_SEGMENT_MINUTES`, `CCORE_AUDIO_CONCURRENCY`, `CCORE_YOUTUBE_PROXY`, `CCORE_YOUTUBE_COOKIES_FILE`, `FIRECRAWL_API_KEY`, `FIRECRAWL_API_URL`, `JINA_API_KEY`, `CRAWL4AI_API_TOKEN`, `TTS_BATCH_SIZE`, `SURREAL_COMMANDS_RETRY_*`, `LOGURU_LEVEL`, `LANGSMITH_*`/`LANGCHAIN_*` (`environment-reference.md:102-218`).
- Variables sans effet : `API_CLIENT_TIMEOUT`, `SURREAL_COMMANDS_MAX_TASKS`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `LOGLEVEL`, `RUST_LOG`, `HOSTNAME` (`environment-reference.md:268-278`).

---

## 2. Configuration des modèles par l'API REST

Préfixe global : toutes les routes sont sous `/api` (`api/main.py:383-406`). Swagger : `GET /docs`, schéma `GET /openapi.json` (non protégés, `api/main.py:239-247`).

### 2.1 Fournisseurs supportés

Liste fermée validée à la création d'un credential (`api/models.py:591-616`) : `openai, anthropic, google, groq, mistral, deepseek, xai, openrouter, dashscope, minimax, novita, siliconflow, zai, ppq, cohere, voyage, elevenlabs, deepgram, ollama, omlx, azure, vertex, openai_compatible, anthropic_compatible`.

- `ollama` : modalités `language`, `embedding` seulement (pas de TTS/STT) (`open_notebook/ai/provider_registry.py:256-261`).
- `openai_compatible` : toutes modalités (language, embedding, text_to_speech, speech_to_text) (`provider_registry.py:302-308`).
- Métadonnées à l'exécution : `GET /api/providers` (`api/routers/providers.py:23`).

### 2.2 Créer un credential (fournisseur + Base URL)

`POST /api/credentials` → 201 (`api/routers/credentials.py:168-218`, schéma `api/models.py:678-711`)

```json
{"name": "ollama-banc", "provider": "ollama",
 "modalities": ["language", "embedding"],
 "base_url": "http://rag-ollama:11434",
 "num_ctx": 32768}
```
Variante OpenAI compatible :
```json
{"name": "ollama-oai", "provider": "openai_compatible",
 "modalities": ["language", "embedding"],
 "base_url": "http://rag-ollama:11434/v1", "api_key": "ollama"}
```
- Champs : `name` (obligatoire), `provider` (obligatoire, liste ci-dessus), `modalities`, `api_key` (chiffré), `base_url`, `endpoint`, `api_version`, `endpoint_llm|embedding|stt|tts`, `project`, `location`, `credentials_path`, `num_ctx` (Ollama seulement ; vide = 8192 côté esperanto, `open_notebook/domain/credential.py:79-83`).
- La Base URL est validée (`http/https` seulement ; IP privées et localhost autorisées ; link-local 169.254.x et métadonnées cloud refusées) (`open_notebook/utils/url_validation.py:43-80`), puis passée telle quelle à esperanto dans `config["base_url"]` (`open_notebook/domain/credential.py:101-141`, en particulier `:111-112`), et revalidée avant chaque usage (`open_notebook/ai/models.py:223-232`).
- Réponse `CredentialResponse` : `id`, `name`, `provider`, `modalities`, `base_url`, …, `num_ctx`, `has_api_key`, `created`, `updated`, `model_count`, `decryption_error` — jamais la clé (`api/models.py:735-757`).
- Autres : `GET /api/credentials[?provider=]`, `GET /api/credentials/{id}`, `PUT /api/credentials/{id}`, `DELETE /api/credentials/{id}` (supprime aussi les modèles liés, réponse `deleted_models`), `GET /api/credentials/status`, `GET /api/credentials/env-status`, `POST /api/credentials/migrate-from-env`, `POST /api/credentials/migrate-encryption` (`api/routers/credentials.py:82-531`).

### 2.3 Tester / découvrir / enregistrer des modèles

- `POST /api/credentials/{id}/test` → dict `{provider, success, message}` ; pour Ollama interroge `base_url` (`api/credentials_service.py:256-281`).
- `POST /api/credentials/{id}/discover` → `{credential_id, provider, discovered: [{name, provider, model_type, description}]}` ; pour Ollama appelle `GET <base_url>/api/tags` et devine le type (`api/routers/credentials.py:432-461` ; `api/credentials_service.py:486-508`). Pour openai_compatible : `GET <base_url>/models`.
- `POST /api/credentials/{id}/register-models` (`api/routers/credentials.py:464-478` ; `api/credentials_service.py:752-796`) :
```json
{"models": [
  {"name": "qwen3:8b", "provider": "ollama", "model_type": "language"},
  {"name": "nomic-embed-text", "provider": "ollama", "model_type": "embedding"}]}
```
  → `{"created": 2, "existing": 0}`. Les modèles sont liés au credential ; doublons (nom+type, insensible à la casse) ignorés. **Ne renvoie pas les IDs** : faire ensuite `GET /api/models?type=language` / `GET /api/models/by-provider/ollama`.

### 2.4 Créer un modèle directement

`POST /api/models` (`api/routers/models.py:205-259`, schéma `api/models.py:97-108`)
```json
{"name": "qwen3:8b", "provider": "ollama", "type": "language", "credential": "credential:xxxx"}
```
- `type` ∈ `language | embedding | text_to_speech | speech_to_text` (`api/routers/models.py:210`) ; doublon → 400.
- Réponse `ModelResponse` : `{id: "model:…", name, provider, type, credential, created, updated}` (`api/models.py:111-118`).
- Sans `credential`, le modèle utilise le repli variables d'environnement (`open_notebook/ai/models.py:244-248`).
- `GET /api/models[?type=]`, `DELETE /api/models/{id}`, `POST /api/models/{id}/test` → `{success, message}` (`api/routers/models.py:173,262,282`).
- Découverte/synchro par fournisseur : `GET /api/models/discover/{provider}`, `POST /api/models/sync/{provider}`, `POST /api/models/sync` (`api/routers/models.py:535-640`) — ces chemins passent par le provisioning (credential en base ou env).

### 2.5 Modèles par défaut

- `GET /api/models/defaults` / `PUT /api/models/defaults` (`api/routers/models.py:307-384`, schéma `api/models.py:121-128`) :
```json
{"default_chat_model": "model:…", "default_transformation_model": "model:…",
 "large_context_model": "model:…", "default_tools_model": "model:…",
 "default_embedding_model": "model:…",
 "default_text_to_speech_model": null, "default_speech_to_text_model": null}
```
  Mise à jour partielle selon la **présence** du champ ; `null` efface, sauf pour `default_chat_model` et `default_embedding_model` qui ne peuvent pas être vidés (`api/routers/models.py:333-361`).
- Équivalent « Auto-assign Defaults » : `POST /api/models/auto-assign` → `{assigned: {slot: model_id}, skipped: [...], missing: [...]}` (`api/routers/models.py:752-850`). **Ne remplit que les deux slots obligatoires** (chat + embedding) s'ils sont vides (`:792-802`) ; choix par priorité de fournisseur (`ollama` avant `openai_compatible`, `api/routers/models.py:91-105`) puis préférences de nom, sinon le premier modèle trié par `provider, name`. Les slots transformation/tools/large_context/TTS/STT restent vides et retombent sur le modèle de chat.
- Usage des slots : chat → `chat` ; Ask (stratégie/réponses/synthèse) → `tools` sauf modèles explicites ; contexte > 105 000 tokens → `large_context` (`open_notebook/ai/provision.py:19-34`).

---

## 3. Endpoints métier

### 3.1 Carnets (notebooks) — `api/routers/notebooks.py`

| Méthode | Chemin | Corps / params | Réponse | Ligne |
|---|---|---|---|---|
| GET | `/api/notebooks` | `?archived=&order_by=updated desc` | liste `NotebookResponse` | `:61` |
| POST | `/api/notebooks` | `{"name": "Banc", "description": ""}` | `{id, name, description, archived, created, updated, source_count, note_count}` (`api/models.py:7-28`) | `:128` |
| GET | `/api/notebooks/{id}` | | `NotebookResponse` | `:238` |
| PUT | `/api/notebooks/{id}` | `{name?, description?, archived?}` | `NotebookResponse` | `:278` |
| POST | `/api/notebooks/{nb}/sources/{src}` | — | `{"message": "Source linked to notebook successfully"}` | `:344` |
| DELETE | `/api/notebooks/{nb}/sources/{src}` | — | message | `:387` |
| GET | `/api/notebooks/{id}/delete-preview` | | `{note_count, exclusive_source_count, shared_source_count, …}` | `:207` |
| DELETE | `/api/notebooks/{id}` | `?delete_exclusive_sources=false` | `{message, deleted_notes, deleted_sources, unlinked_sources, deleted_chat_sessions}` | `:419` |

Anomalie relevée : le test d'idempotence de la liaison cherche `out = $source_id AND in = $notebook_id` (`api/routers/notebooks.py:352-358`) alors que la relation est créée `source->reference->notebook` (`:364`) et supprimée avec `out = $notebook_id AND in = $source_id` (`:396`) ; aucun index unique sur `reference` (`open_notebook/database/migrations/1.surrealql:54`) : le test ne correspond jamais, **un second appel crée une arête en double**. Ne pas re-lier une source déjà liée à la création.

### 3.2 Sources — `api/routers/sources.py`

**`POST /api/sources`** accepte uniquement des champs de **formulaire** (multipart/form-data), pas du JSON (`api/routers/sources.py:186-254,639-705`) :

| Champ form | Type | Remarque |
|---|---|---|
| `type` | `upload` \| `link` \| `text` | obligatoire |
| `notebooks` | chaîne JSON `["notebook:abc"]` (max 50) | ou `notebook_id` (déprécié), pas les deux (`api/models.py:362-379`) |
| `file` | fichier | pour `upload` |
| `url` | | pour `link` (validation SSRF, `sources.py:434-443`) |
| `content` | | pour `text` |
| `title` | | optionnel |
| `transformations` | chaîne JSON d'IDs | insights générés après extraction |
| `embed` | `"true"/"false"` | **défaut false** : sans `embed=true`, pas de recherche vectorielle |
| `delete_source` | `"true"/"false"` | supprime le fichier après extraction |
| `async_processing` | `"true"/"false"` | **défaut false** : en synchrone, l'API attend jusqu'à 300 s (`sources.py:602-608`) |

Exemple : `curl -F type=upload -F file=@doc.pdf -F 'notebooks=["notebook:abc"]' -F embed=true -F async_processing=true http://localhost:5055/api/sources`

**`POST /api/sources/json`** : même modèle en JSON (`SourceCreate`, `api/models.py:331-360`), pour `link` et `text` (pas d'upload binaire ; `file_path` doit être sous `/app/data/uploads`, `sources.py:452-459`) (`api/routers/sources.py:708-713`) :
```json
{"type": "text", "content": "…", "title": "T", "notebooks": ["notebook:abc"], "embed": true, "async_processing": true}
```

Réponse `SourceResponse` (`api/models.py:387-403`) : `{id: "source:…", title, topics, asset, full_text, embedded, embedded_chunks, file_available, created, updated, command_id, status, processing_info, notebooks}`. En asynchrone : `status: "new"`, `command_id: "command:…"`, `processing_info: {"async": true, "queued": true}` (`sources.py:536-545`).

**Suivi du traitement** :
- `GET /api/sources/{id}/status` → `{status, message, processing_info, command_id}` avec `status` ∈ `queued | running | completed | failed | unknown` (`api/routers/sources.py:843-901` ; `api/models.py:459-465`).
- Équivalent générique : `GET /api/commands/jobs/{command_id}` → `{job_id, status, result, error_message, created, updated, progress}` (`api/routers/commands.py:14-37`).
- **Piège** : `completed` = extraction + sauvegarde terminées, pas l'embedding. L'embedding est soumis comme **un autre job** `embed_source` (`open_notebook/graphs/source.py:320-327` → `open_notebook/domain/notebook.py:538-580` ; `commands/source_commands.py:138-145` « embedding is fire-and-forget »). Les transformations aussi (`docs/3-USER-GUIDE/adding-sources.md:74`). Critère fiable : `GET /api/sources/{id}` → `embedded_chunks > 0` (compte des lignes `source_embedding`, `open_notebook/domain/notebook.py:502-510`) et, pour les insights, `GET /api/sources/{id}/insights`.
- Relancer : `POST /api/sources/{id}/retry` (`sources.py:934`). Embedding manuel : `POST /api/embed` `{"item_id": "source:…", "item_type": "source", "async_processing": true}` → `{success, message, item_id, item_type, command_id}` (`api/routers/embedding.py:16` ; `api/models.py:244-259`). Re-embedding global : `POST /api/embeddings/rebuild` `{"mode": "all"}` puis `GET /api/embeddings/rebuild/{command_id}/status` (`api/routers/embedding_rebuild.py:19,128`).

Autres : `GET /api/sources?notebook_id=&limit=50(max 100)&offset=&sort_by=&sort_order=` (`sources.py:257`), `GET /api/sources/{id}` (`:755`), `GET /api/sources/{id}/download` (`:824`), `PUT /api/sources/{id}` `{title?, topics?}` (`:905`), `DELETE /api/sources/{id}` → `{"message": "Source deleted successfully"}` (`:1055`).

### 3.3 Chat dans un carnet — `api/routers/chat.py`

**Ce n'est pas un RAG par similarité** : le contexte est composé explicitement, source par source, puis injecté entier dans le prompt système (`prompts/chat/system.jinja:18-24`). Aucun top-k vectoriel dans le chat de carnet.

1. Créer une session : `POST /api/chat/sessions` `{"notebook_id": "notebook:abc", "title": "t", "model_override": null}` → `{id: "chat_session:…", title, notebook_id, created, updated, message_count, model_override}` (`api/routers/chat.py:35-61,142-181`).
2. Construire le contexte : `POST /api/chat/context` (`chat.py:395-418`)
```json
{"notebook_id": "notebook:abc",
 "context_config": {"sources": {"source:s1": "full content", "source:s2": "insights", "source:s3": "not in"},
                    "notes": {"note:n1": "full content"}}}
```
   → `{context: {sources: [...], notes: [...]}, token_count, char_count}`. `insights` = id+titre+insights ; `full content` = id+titre+insights+`full_text` (`open_notebook/domain/notebook.py:480-500`) ; sans `context_config`, toutes les sources en mode court (`open_notebook/utils/context_builder.py:262-352`).
3. Envoyer : `POST /api/chat/execute` (`chat.py:70-83,308-392`)
```json
{"session_id": "chat_session:…", "message": "Question ?", "context": {"sources": [...], "notes": [...]}, "model_override": null}
```
   (le frontend passe exactement le `context` renvoyé à l'étape 2, `frontend/src/lib/hooks/use-notebook-chat.ts:133-173`).
   Réponse **non streamée** : `{session_id, messages: [{id, type: "human"|"ai", content, timestamp: null}, ...]}` = **tout l'historique** de la session (`api/routers/_chat_shared.py:25-29,82-94`). La réponse est le dernier message `type: "ai"`.
- **Citations** : uniquement dans le texte, sous forme `[source:xxxx]`, `[note:xxxx]`, `[insight:xxxx]`, demandées par le prompt (`prompts/chat/system.jinja:30-47`). Aucun champ structuré de citations, pas de numéro de page ni de chunk.
- Sessions : `GET /api/chat/sessions?notebook_id=` (obligatoire), `GET /api/chat/sessions/{id}` (avec messages), `PUT /api/chat/sessions/{id}` `{title?, model_override?}`, `DELETE /api/chat/sessions/{id}` → `{success, message}` (`chat.py:97,184,240,287`).
- Chat sur une seule source (SSE) : `POST /api/sources/{src}/chat/sessions` `{"source_id": "...", "title": ...}` puis `POST /api/sources/{src}/chat/sessions/{sid}/messages` `{"message": "..."}` → flux `text/event-stream` d'événements `user_message`, `ai_message`, `context_indicators` (`{sources, insights, notes}`), `complete`, `error` (`api/routers/source_chat.py:93,375-428,432`). Contexte de la source tronqué à 50 000 tokens (`open_notebook/graphs/source_chat.py:82-85`).

### 3.4 Recherche — `POST /api/search` (`api/routers/search.py:25-74`, schéma `api/models.py:39-81`)

```json
{"query": "…", "type": "vector", "limit": 100, "search_sources": true, "search_notes": true,
 "minimum_score": 0.2, "notebook_id": "notebook:abc"}
```
- `type` : `text` (BM25 SurrealDB sur titres, `full_text`, chunks, insights, notes) ou `vector` (cosinus) ; `limit` 1–1000 (défaut 100) ; `minimum_score` 0–1 (défaut 0.2, vecteur seulement) ; portée `notebook_id` et/ou `notebook_ids` (max 50, vide = toute la base).
- Réponse : `{results: [...], total_count, search_type}`. Vectoriel : chaque résultat `{id, parent_id, title, similarity, matches: [contenus des chunks]}` (`open_notebook/database/migrations/24.surrealql:90-161`) ; regroupé par `id` (= la source, pas le chunk), trié par similarité (`open_notebook/domain/notebook.py:888-935`). Texte : `{id, parent_id, title, relevance}` (`migrations/25.surrealql`).
- Vectoriel exige un modèle d'embedding par défaut (sinon 400, `search.py:31-37`) ; seuls les vecteurs de même dimension que la requête sont comparés (`migrations/24.surrealql:107`) → changer de modèle d'embedding impose un rebuild.

### 3.5 Ask (question sur la base) — `api/routers/search.py`

- `POST /api/search/ask` (SSE) et `POST /api/search/ask/simple` (JSON) (`search.py:140,202`), corps (`api/models.py:84-88`) :
```json
{"question": "…", "strategy_model": "model:…", "answer_model": "model:…", "final_answer_model": "model:…", "notebook_id": "notebook:abc"}
```
  Les trois modèles sont **obligatoires** (IDs). Réponse simple : `{answer, question}` (`api/models.py:91-93`). SSE : événements `strategy` (`reasoning`, `searches[]`), `answer`, `final_answer`, `complete`, `error` (`search.py:77-137`).
- Fonctionnement : l'LLM de stratégie produit jusqu'à 5 recherches (`open_notebook/graphs/ask.py:49-52`) ; chacune fait une recherche vectorielle **top 10**, score min 0.2 par défaut (`ask.py:134-140`) ; sorties plafonnées à 8192 tokens (`ask.py:27`).

### 3.6 Notes — `api/routers/notes.py`

- `POST /api/notes` `{"title": "t", "content": "…", "note_type": "human", "notebook_id": "notebook:abc"}` → `{id, title, content, note_type, created, updated, command_id}` (`notes.py:55-113` ; `api/models.py:218-240`). Une note `ai` sans titre reçoit un titre généré par LLM. L'embedding de la note est lancé en tâche de fond (`command_id`).
- `GET /api/notes?notebook_id=`, `GET/PUT/DELETE /api/notes/{id}` (`notes.py:17,121,146,189`).
- Insight → note : `POST /api/insights/{id}/save-as-note` `{"notebook_id": "..."}` (`api/routers/insights.py:63`).

### 3.7 Transformations — `api/routers/transformations.py`

- `GET /api/transformations` (`:37`) ; préchargées : « Dense Summary », « Simple Summary »… (`open_notebook/database/migrations/5.surrealql:89,143`).
- `POST /api/transformations` `{"name": "n", "title": "T", "description": "d", "prompt": "…", "apply_default": false, "model_id": null}` (`:58` ; `api/models.py:140-152`).
- `POST /api/transformations/execute` (synchrone, sur un texte libre) `{"transformation_id": "transformation:…", "input_text": "…", "model_id": null}` → `{output, transformation_id, model_id}` (`:93-136` ; `api/models.py:184-201`).
- Sur une source (asynchrone, produit un insight) : `POST /api/sources/{id}/insights` `{"transformation_id": "...", "model_id": null}` → 202 `{status: "pending", source_id, transformation_id, command_id}` ; refusé si la source n'a pas de texte (`api/routers/sources.py:1104-1150`).
- `GET/PUT/DELETE /api/transformations/{id}`, `GET/PUT /api/transformations/default-prompt` (`:139,160,185,207,256`).

### 3.8 Podcasts

- Profils de locuteurs : `POST /api/speaker-profiles` (`api/routers/speaker_profiles.py:68-97`)
```json
{"name": "duo", "description": "", "voice_model": "model:tts…",
 "speakers": [{"name": "Alice", "voice_id": "alloy", "backstory": "…", "personality": "…"}]}
```
  1 à 4 locuteurs, champs `name`, `voice_id`, `backstory`, `personality` obligatoires (`open_notebook/podcasts/models.py:150-163`). `voice_model` = modèle `text_to_speech` (Ollama n'en fournit pas → openai_compatible type Speaches, `docs/5-CONFIGURATION/local-tts.md`).
- Profils d'épisode : `POST /api/episode-profiles` (`api/routers/episode_profiles.py:120-169`)
```json
{"name": "court", "speaker_config": "speaker_profile:…", "outline_llm": "model:…", "transcript_llm": "model:…",
 "language": "fr-FR", "default_briefing": "…", "num_segments": 5, "max_tokens": 8192}
```
  `num_segments` 3–20 (`open_notebook/podcasts/models.py:85-90`). Profils préchargés (`tech_discussion`, `solo_expert`, `business_analysis` / `tech_experts`, …) configurés pour OpenAI (`migrations/7.surrealql:56-144`).
- Génération : `POST /api/podcasts/generate` (`api/routers/podcasts.py:124-154` ; `api/podcast_service.py:12-30`)
```json
{"episode_profile": "court", "speaker_profile": "duo", "episode_name": "ep1", "notebook_id": "notebook:abc", "content": null, "briefing_suffix": null}
```
  `episode_profile` est cherché **par nom** (`podcast_service.py:48`), `speaker_profile` par ID ou nom. Avec `notebook_id`, tout le carnet (texte intégral + insights + notes) est envoyé (`open_notebook/domain/notebook.py:74-114`). Réponse `{job_id, status: "submitted", message, episode_profile, episode_name}`.
- Statut : `GET /api/podcasts/jobs/{job_id}` → `{job_id, status, result, error_message, created, updated, progress}` (`api/podcast_service.py:116-137`).
- Épisodes : `GET /api/podcasts/episodes`, `GET /api/podcasts/episodes/{id}` (`{…, audio_file, audio_url, transcript, outline, job_status, error_message}`), `GET /api/podcasts/episodes/{id}/audio`, `POST …/{id}/retry`, `DELETE …/{id}` (`api/routers/podcasts.py:173,256,315,349,400`).
- CRUD profils : `GET/PUT/DELETE /api/{episode|speaker}-profiles/{id}`, `POST …/{id}/duplicate`.

### 3.9 Suppression (récapitulatif)

`DELETE /api/notebooks/{id}?delete_exclusive_sources=true`, `DELETE /api/sources/{id}`, `DELETE /api/notes/{id}`, `DELETE /api/chat/sessions/{id}`, `DELETE /api/insights/{id}`, `DELETE /api/transformations/{id}`, `DELETE /api/models/{id}`, `DELETE /api/credentials/{id}`, `DELETE /api/podcasts/episodes/{id}`, `DELETE /api/commands/jobs/{job_id}` (annule un job, `api/routers/commands.py:62`).

### 3.10 Divers

- `GET /api/settings` / `PUT /api/settings` : moteurs d'extraction, OCR Docling, option d'embedding par défaut (`ask|always|never`, utilisée par l'UI, pas par l'API), suppression auto des fichiers (`api/routers/settings.py:14,39` ; `open_notebook/domain/content_settings.py:8-47`).
- `GET /api/capabilities` → `{docling_available, crawl4ai_available, crawl4ai_remote_configured}` (`api/routers/capabilities.py:31`).
- `GET /health` → `{"status": "healthy"}` (`api/main.py:414-416`).
- `POST /api/commands/jobs` (soumission générique) a été **supprimé** en 1.15.1 (`CHANGELOG.md`, section 1.15.1 « Removed »).

---

## 4. Authentification

- Middleware `PasswordAuthMiddleware` (`api/auth.py:12-82`), activé seulement si `OPEN_NOTEBOOK_PASSWORD` (ou `OPEN_NOTEBOOK_PASSWORD_FILE`) est défini (`:24,37-38`).
- En-tête attendu : `Authorization: Bearer <mot de passe en clair>` (`:49-68`), comparaison à temps constant (`:71-72`). Erreurs 401 : `Missing authorization header`, `Invalid authorization header format`, `Invalid password`.
- Exemptés : `/`, `/health`, `/docs`, `/openapi.json`, `/redoc`, `/api/auth/status`, `/api/config` et toutes les requêtes `OPTIONS` (`api/main.py:237-248` ; `api/auth.py:44-46`).
- `GET /api/auth/status` → `{auth_enabled, message}` (`api/routers/auth.py:13-26`).
- Interface : écran de connexion qui teste le mot de passe en appelant `GET /api/notebooks` avec `Bearer <password>` (`frontend/src/lib/stores/auth-store.ts:73-92`), puis le **stocke en clair dans `localStorage`** (clé `auth-storage`, persist zustand, `auth-store.ts:211-216`) et l'ajoute à chaque requête (`frontend/src/lib/api/client.ts:44`). Pas de session, pas de jeton dérivé, pas de limitation des tentatives.
- Pas d'utilisateurs ni de rôles (choix « mono-utilisateur », `docs/7-DEVELOPMENT/decisions/PDR-001-single-user-first.md`).

---

## 5. Découpage, top-k, historique

| Paramètre | Valeur par défaut | Où | Source |
|---|---|---|---|
| Taille de chunk | 400 tokens (tiktoken `o200k_base`), min 100 | env `OPEN_NOTEBOOK_CHUNK_SIZE`, lu à l'import (redémarrage requis) | `open_notebook/utils/chunking.py:33-57,116` ; `open_notebook/utils/token_utils.py:28` |
| Recouvrement | 15 % = 60 tokens | env `OPEN_NOTEBOOK_CHUNK_OVERLAP` | `chunking.py:60-85,117` |
| Chunk minimal | 5 tokens | env `OPEN_NOTEBOOK_MIN_CHUNK_SIZE` | `chunking.py:88-112` |
| Découpeurs | HTML / Markdown par en-têtes, sinon `RecursiveCharacterTextSplitter` selon le type détecté | code | `chunking.py:23-27,127+` |
| Lot d'embeddings | 50 | env `OPEN_NOTEBOOK_EMBEDDING_BATCH_SIZE` | `open_notebook/utils/embedding.py:31` |
| Top-k chat de carnet | **aucun** : pas de recherche, contexte choisi manuellement (insights ou texte intégral) | code | `open_notebook/utils/context_builder.py:262-352` ; `prompts/chat/system.jinja:18-24` |
| Top-k Ask | 10 résultats par recherche, ≤ 5 recherches, score min 0.2 | en dur | `open_notebook/graphs/ask.py:49-52,134-140` ; `open_notebook/domain/notebook.py:893` |
| `/api/search` | `limit` 100, `minimum_score` 0.2 | paramètres de requête | `api/models.py:67-75` |
| Historique de chat | **complet, jamais tronqué** (`add_messages`), persistant dans SQLite `/app/data/sqlite-db/checkpoints.sqlite` | code | `open_notebook/graphs/chat.py:22-27,95-105` ; `open_notebook/config.py:8-10` |
| Bascule « large context » | si prompt (système + historique) > 105 000 tokens → modèle `large_context` | en dur | `open_notebook/ai/provision.py:23-28` |
| Tokens de sortie | chat 8192, Ask 8192, podcast 8192 par défaut | en dur / profil | `open_notebook/graphs/chat.py:46,69` ; `ask.py:27` ; `CHANGELOG.md` 1.15.0 |
| Contexte Ollama | `num_ctx` 8192 par défaut, réglable par credential | credential | `open_notebook/domain/credential.py:79-83` ; `docs/5-CONFIGURATION/ollama.md:114-120` |
| Contexte chat sur une source | tronqué à 50 000 tokens | en dur | `open_notebook/graphs/source_chat.py:85` |
| Timeout LLM | 180 s | env `ESPERANTO_LLM_TIMEOUT` | `open_notebook/config.py:38-47` |

Conséquence pour un banc RAG : avec Ollama à `num_ctx` 8192 et un carnet en « full content », le prompt est tronqué silencieusement par Ollama ; augmenter `num_ctx` ou utiliser « insights ».

---

## 6. Extraction des contenus

- Moteur : **content-core** (`content-core>=2.2.1,<3`, `pyproject.toml:40`), appelé via `extract_content(url=…, file_path=…, content=…, config=ContentCoreConfig(...))` (`open_notebook/graphs/source.py:8,184-292`).
- Moteur document : `auto` (Docling s'il est installé, sinon extraction simple), `docling`, `simple` ; moteur URL : `auto` (Firecrawl → Jina → Crawl4AI → simple/BeautifulSoup), `firecrawl`, `jina`, `crawl4ai`, `simple` (`open_notebook/domain/content_settings.py:10-15` ; `docs/3-USER-GUIDE/content-processing-engines.md:30-71`). Un moteur choisi mais non installé retombe sur `auto` (`open_notebook/graphs/source.py:67-85`).
- **Docling n'est pas dans l'image par défaut** : il s'installe au démarrage avec `OPEN_NOTEBOOK_ENABLE_DOCLING=true` (`scripts/docker-entrypoint.sh:58-71`, plusieurs centaines de Mo à quelques Go, téléchargés depuis PyPI / Hugging Face).
- Formats acceptés (`docs/3-USER-GUIDE/adding-sources.md:38-47`) : PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX, ODT, ODS, ODP, EPUB, TXT, MD, HTML, HTM ; audio MP3, WAV, M4A, AAC ; vidéo MP4, AVI, MOV, WMV ; images JPG, JPEG, PNG, TIFF **seulement avec Docling**. Contrôle préalable par content-core, 415 si non supporté (`api/routers/sources.py:49-72`).
- **OCR des PDF scannés** : uniquement via Docling avec `docling_ocr` (vrai par défaut) (`open_notebook/domain/content_settings.py:22-28` ; `adding-sources.md:47`). Options `docling_formulas`, `docling_vision` (désactivées).
- **Audio/vidéo** : transcription via le modèle STT par défaut (`default_speech_to_text_model`), transmis à content-core en `audio_provider`/`audio_model` (`open_notebook/graphs/source.py:223-235`). Sans modèle STT, échec. Découpage en segments de 10 min, 3 en parallèle (`CCORE_AUDIO_SEGMENT_MINUTES`, `CCORE_AUDIO_CONCURRENCY`), timeout 3600 s (`environment-reference.md:112,172-173`). Ollama ne fournit pas de STT → passer par un serveur OpenAI compatible (Speaches/faster-whisper, `docs/5-CONFIGURATION/local-stt.md:5-24`).
- YouTube : transcriptions, langues préférées réglables (`content_settings.py:44-47`).

---

## 7. MCP

- **Aucun serveur MCP dans le dépôt** (aucun paquet ni dépendance `mcp` dans `pyproject.toml`).
- La doc renvoie à un serveur **tiers** maintenu par l'équipe « Epochal » : paquet PyPI `open-notebook-mcp`, dépôt `github.com/Epochal-dev/open-notebook-mcp`, listé au registre MCP (`docs/5-CONFIGURATION/mcp-integration.md:162-176`).
- Configuration type : `"command": "uvx", "args": ["open-notebook-mcp"]`, env `OPEN_NOTEBOOK_URL=http://localhost:5055`, `OPEN_NOTEBOOK_PASSWORD=…` (`mcp-integration.md:29-42,82-85`). Il s'appuie sur l'API REST. Non audité ici (hors dépôt).

---

## 8. Points de sécurité relevés

1. **Ports exposés sur toutes les interfaces** : `8502:8502` et `5055:5055` sans `127.0.0.1` (`docker-compose.yml:29-30`) ; API liée à `0.0.0.0` (`Dockerfile:107`), frontend aussi (`supervisord.conf:39`). Pour un banc local : publier en `127.0.0.1:5055:5055` / `127.0.0.1:8502:8502`.
2. **Pas de mot de passe par défaut** : sans `OPEN_NOTEBOOK_PASSWORD`, l'API (y compris création de credentials, lecture des sources) est ouverte (`api/auth.py:37-38`).
3. **CORS `*` par défaut** (`api/main.py:73-80`), avertissement au démarrage seulement ; `allow_credentials` désactivé dans ce cas.
4. `/docs`, `/openapi.json`, `/redoc`, `/api/config` hors authentification (`api/main.py:237-248`) ; `/api/config` révèle la version et l'état de la base.
5. Mot de passe envoyé tel quel en Bearer (pas de jeton dérivé) et **stocké en clair dans le `localStorage`** du navigateur (`frontend/src/lib/stores/auth-store.ts:92,211-216`) ; pas de limitation des essais ; HTTP sans TLS par défaut.
6. **Clé de chiffrement d'exemple** `change-me-to-a-secret-string` dans le compose (`docker-compose.yml:34`) ; sel PBKDF2 fixe et commun à toutes les installations (`open_notebook/utils/encryption.py:114-118`) : la sécurité repose sur l'entropie de la clé. Les clés déchiffrées sont recopiées dans `os.environ` du processus (`open_notebook/ai/key_provider.py:155-267`).
7. SurrealDB `root:root` par défaut, mais port lié à `127.0.0.1` (`docker-compose.yml:10,18`).
8. **Appels réseau sortants** :
   - Vérification de version : `GET https://raw.githubusercontent.com/lfnovo/open-notebook/main/pyproject.toml` à chaque appel de `/api/config`, cache 24 h, timeout 10 s (`api/routers/config.py:26,42-81` ; `open_notebook/utils/version_utils.py:36-43`). Pas de variable pour la couper.
   - Extraction d'URL en mode `auto` : peut passer par Jina Reader (service tiers) **même sans clé** (« without it, requests are sent unauthenticated », `environment-reference.md:167` ; chaîne `content-processing-engines.md:65`) → fixer le moteur URL à `simple` via `PUT /api/settings` pour un banc sans fuite.
   - Docling / Crawl4AI : téléchargements PyPI, Hugging Face, Chromium au démarrage s'ils sont activés (`scripts/docker-entrypoint.sh`).
   - YouTube, sites web des sources de type `link`, fournisseurs d'IA configurés.
   - LangSmith seulement si `LANGSMITH_TRACING=true` (`environment-reference.md:215`).
9. **Télémétrie** : aucune bibliothèque d'analytics (PostHog, Sentry…) trouvée dans le code Python ni le frontend. `NEXT_TELEMETRY_DISABLED` n'est pas positionné dans le `Dockerfile` (la télémétrie Next.js concerne le build/dev, pas le serveur standalone — non vérifié à l'exécution). Les polices `next/font/google` sont intégrées au build (`frontend/src/app/layout.tsx:6`).
10. Garde-fous présents : validation SSRF des URL (link-local et métadonnées cloud refusées, DNS épinglé) (`open_notebook/utils/url_validation.py:43-80`), confinement des fichiers dans `uploads/` contre LFI (`api/routers/sources.py:452-459,716-738`), noms de fichiers anti-traversée (`:117-156`), erreurs tronquées à 200 caractères (`:75-84`), taille max de requête (`api/middleware.py`). Les IP privées sont volontairement autorisées (appli auto-hébergée), donc une URL de source peut viser le réseau interne (dont `rag-ollama`).
11. L'image installe des paquets au démarrage (`curl … nodesource | bash` au build, `Dockerfile:77` ; `uv pip install` à l'exécution si Docling activé) et `uv:latest` non figé (`Dockerfile:39,82`) : reproductibilité limitée.
12. Bug fonctionnel : liaison source↔carnet non idempotente (cf. §3.1, `api/routers/notebooks.py:352-364`).

---

## 9. CHANGELOG 1.14.0 → 1.15.1 (`CHANGELOG.md:10-119`)

**1.15.1 (2026-11-03)** — `CHANGELOG.md:10-33`
- Documentation entièrement réécrite à partir du code (installation unique sur le `docker-compose.yml`, `environment-reference.md` devient la liste de référence, fonctionnalités inventées retirées).
- Corrigé : variables sans effet retirées de la doc (`API_CLIENT_TIMEOUT`) ; un dépassement de `ESPERANTO_LLM_TIMEOUT` n'est plus présenté comme une erreur de connexion ; repli `SURREAL_ADDRESS`/`SURREAL_PORT` corrigé (`ws://host:port/rpc`) ; `.env.example` utilise les bons noms `OPEN_NOTEBOOK_CHUNK_*` ; italien sélectionnable.
- Supprimé : `POST /api/commands/jobs` (le statut `GET /api/commands/jobs/{id}` reste).
- Sécurité : contrôles de répertoire d'upload et d'URL appliqués aussi dans le worker ; content-core ≥ 2.2.1 (refus des adresses link-local / métadonnées à chaque redirection).

**1.15.0 (2026-10-04)** — `CHANGELOG.md:35-83`
- Ajouts : uploads ODT/ODS/ODP/HTM ; options YouTube (`CCORE_YOUTUBE_PROXY`, `CCORE_YOUTUBE_COOKIES_FILE`, segmentation audio) ; fournisseurs SiliconFlow et Z.ai ; TTS MiniMax ; nouvelle charte graphique « Quiet Green ».
- Changements : podcasts sur podcast-creator 0.13 (JSON validé par schéma, budget 8192 tokens pour plan et transcription) ; **chiffrement des credentials en PBKDF2-HMAC-SHA256 600k** (`pbkdf2v1:`), migration via `POST /api/credentials/migrate-encryption`, avertissement : pas de retour arrière vers une version antérieure.
- Corrections : podcasts sur installation neuve ; worker qui ne bloque plus quand une source est supprimée avant traitement ; **timeout LLM par défaut 180 s** (esperanto 2.28 impose 60 s sinon ; Ollama attendait sans limite avant) ; insertion des embeddings par lots de 50 ; streaming du chat de source réparé ; mot de passe API en UTF-8 ; erreurs d'extraction typées (content-core 2.2) ; langue des profils de podcast respectée ; Ask non tronqué (2000 → 8192 tokens) ; nettoyage des embeddings partiels en cas d'échec ; transformations refusées sur source vide ; résultats vectoriels triés par similarité ; réponse vide du modèle traitée comme une erreur ; erreurs de longueur de contexte non retentées.
- Sécurité : esperanto 2.28.0, content-core 2.2.0, podcast-creator 0.13.1, Next 16.3.8 et autres mises à jour de dépendances.

**1.14.0 (2026-07-20)** — `CHANGELOG.md:85-119`
- Ajouts : options Docling formules / vision ; TTS et STT via OpenRouter ; fournisseur `anthropic_compatible` ; fournisseur oMLX ; Cohere, Deepgram STT, PPQ, Novita ; **`OPEN_NOTEBOOK_WORKER_MAX_TASKS`** ; champ « Max output tokens » des profils d'épisode.
- Corrections notables : moteur d'extraction non installé qui cassait l'ingestion ; proxy HTTP qui cassait le WebSocket SurrealDB (ajout automatique à `NO_PROXY`) ; **auto-assign ne remplit plus que les slots obligatoires** ; épinglage DNS des URL de fournisseurs (TOCTOU) ; modèle par transformation enfin pris en compte ; suppression d'un carnet supprime ses sessions de chat ; exemples Ollama corrigés (`OLLAMA_API_BASE` au lieu de `OLLAMA_BASE_URL`, qui n'est lu nulle part).
