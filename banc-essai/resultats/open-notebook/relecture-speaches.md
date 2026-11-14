# Relecture : Speaches comme serveur de voix local pour Open Notebook 1.15.1

Vérifié le 2026-11-08, en lecture seule (aucun conteneur lancé). Sources :

- dépôt cloné au tag `v0.8.3` (commit `c78b77d5`), noté `[0.8.3] chemin:ligne` ;
- dépôt cloné sur `master` (commit `993994f7`, 17/04/2026), noté `[master] chemin:ligne` ;
- API GitHub, API du registre ghcr, API Hugging Face, `docker image inspect` sur l'image locale ;
- docs Open Notebook au tag `v1.15.1` : `docs/5-CONFIGURATION/local-tts.md` et `local-stt.md`.

Machine cible : WSL2, Docker, CPU seulement, 15 Go de RAM.

---

## 1. Version et image

| Élément | Valeur | Source |
|---|---|---|
| Release la plus récente | `v0.9.0-rc.3`, publiée le 27/12/2025. C'est une *release candidate*, même si GitHub ne la marque pas comme pré-version (`prerelease: false`, alors que `v0.9.0-rc.1` porte `true`). | https://api.github.com/repos/speaches-ai/speaches/releases |
| Dernière version stable | `v0.8.3`, publiée le 19/09/2025 | idem |
| Image CPU de la stable | `ghcr.io/speaches-ai/speaches:0.8.3-cpu` | `https://ghcr.io/v2/speaches-ai/speaches/tags/list` |
| Empreinte `0.8.3-cpu` | `sha256:21e3df06d842fb7802ab470dd77c25f0e8c0d22950e8d8c6ae886e851af53ef8` | en-tête `docker-content-digest` de `GET /v2/speaches-ai/speaches/manifests/0.8.3-cpu` (token anonyme) |
| Empreinte `latest-cpu` (au 08/11/2026) | **la même** : `sha256:21e3df06…53ef8` | idem, manifeste `latest-cpu` |
| Image locale `latest-cpu` | `RepoDigests = ghcr.io/speaches-ai/speaches@sha256:21e3df06…53ef8`, créée le 2025-09-19T03:50:55Z | `docker image inspect` |
| Image CPU de la RC | `ghcr.io/speaches-ai/speaches:0.9.0-rc.3-cpu`, empreinte `sha256:2163775b6df5e451a71200e8f675fed68dbd8ab184fc604453d549e486f22fd2`. L'étiquette ne prend pas de `v` : `v0.9.0-rc.3-cpu` renvoie 404. | registre ghcr |

**Ce que ça implique.** L'image `latest-cpu` déjà présente sur la machine est exactement la `0.8.3-cpu`. Pour figer la version, utiliser `ghcr.io/speaches-ai/speaches:0.8.3-cpu@sha256:21e3df06d842fb7802ab470dd77c25f0e8c0d22950e8d8c6ae886e851af53ef8`.

Petite incohérence à connaître : en 0.8.3, l'application annonce `version="v0.8.2"` (`[0.8.3] src/speaches/main.py:71`, commentaire « TODO: update this on release »). Ce n'est pas un problème.

Le reste de ce document décrit la **0.8.3**, sauf mention contraire.

---

## 2. Lancement en Docker

- **Port** : le serveur écoute sur le port 8000 du conteneur. Voir `[0.8.3] Dockerfile:38-39,51` (`UVICORN_HOST=0.0.0.0`, `UVICORN_PORT=8000`, `EXPOSE 8000`) et la commande `uvicorn --factory speaches.main:create_app` (`Dockerfile:52`). Les mêmes valeurs par défaut sont dans `[0.8.3] src/speaches/config.py:76-77`.
- **Écoute par défaut** : `0.0.0.0` dans le conteneur.
- **Volume du cache Hugging Face** : `hf-hub-cache:/home/ubuntu/.cache/huggingface/hub`. Sources : `[0.8.3] compose.cpu.yaml:12-13`, `docs/installation.md:88-98`. Le conteneur tourne avec l'utilisateur `ubuntu` (UID 1000, `Dockerfile:16-17`), et le répertoire est créé d'avance (`Dockerfile:37`).
- **Commande officielle (CPU)**, d'après `[0.8.3] docs/installation.md:91-97` :
  `docker run --rm --detach --publish 8000:8000 --name speaches --volume hf-hub-cache:/home/ubuntu/.cache/huggingface/hub ghcr.io/speaches-ai/speaches:latest-cpu`
- **Variables d'environnement utiles.** Elles sont lues par pydantic-settings, avec `__` comme séparateur pour les réglages imbriqués (`[0.8.3] src/speaches/config.py:58-66`).

  | Variable | Défaut | Ligne dans `config.py` |
  |---|---|---|
  | `API_KEY` | aucune | 68-71 |
  | `LOG_LEVEL` | `debug` | 72 |
  | `ENABLE_UI` | `True`, interface Gradio | 86-89 |
  | `ALLOW_ORIGINS` | non défini | 78 |
  | `WHISPER__INFERENCE_DEVICE` | `auto` | 24 |
  | `WHISPER__COMPUTE_TYPE` | `default` | 26 |
  | `WHISPER__CPU_THREADS` | `0` | 27 |
  | `WHISPER__TTL` | `300` s avant de décharger le modèle ; `-1` = jamais | 29-34 |
  | `CHAT_COMPLETION_BASE_URL` | `http://localhost:11434/v1` (Ollama, sert seulement au temps réel et au chat) | 112 |

- **Aucun téléchargement de modèle au démarrage (0.8.3).** La configuration ne contient pas d'option de préchargement (`[0.8.3] src/speaches/config.py`, en entier). Les modèles se téléchargent seulement sur demande explicite (`POST /v1/models/{id}`, voir §3). Les requêtes TTS et STT ne déclenchent pas de téléchargement automatique : elles renvoient une erreur 404 « not installed locally » (`[0.8.3] src/speaches/routers/speech.py:64-69`, `routers/stt.py:183-188`).
  L'option `PRELOAD_MODELS` (liste d'identifiants à télécharger au démarrage, vide par défaut) n'existe qu'à partir de la `0.9.0-rc.3` (`src/speaches/config.py:139-145` au tag `v0.9.0-rc.3`, `[master] src/speaches/main.py:85-89`). Il suffit de ne pas la définir.

---

## 3. Endpoints compatibles OpenAI et modèles

### Endpoints

Toutes les références sont dans `[0.8.3] src/speaches/routers/`.

| Endpoint | Rôle | Référence |
|---|---|---|
| `POST /v1/audio/speech` | Corps JSON : `model`, `input`, `voice`, `response_format` (`mp3` par défaut ; `flac`, `wav`, `pcm` ; **`opus` et `aac` ne sont pas acceptés**), `speed` (1.0), `sample_rate` (optionnel) | `speech.py:22-53,58` |
| `POST /v1/audio/transcriptions` | Formulaire multipart : `file`, `model`, `language`, `response_format` (`text`, `json`, `verbose_json`, `vtt`, `srt`) | `stt.py:151-214` |
| `POST /v1/audio/translations` | Traduction | `stt.py:102` |
| `GET /v1/models` | Liste **uniquement les modèles déjà téléchargés** (TTS et STT) ; filtre `?task=text-to-speech` ou `?task=automatic-speech-recognition` | `models.py:28-36` |
| `GET /v1/models/{id}` | Détail d'un modèle local | `models.py:69-78` |
| `POST /v1/models/{id}` | **Télécharge** le modèle depuis Hugging Face. Renvoie 200 « downloaded », 201 « already exists », 404 si l'identifiant n'est pas au registre. Le chargement en mémoire se fait ensuite à la première requête. | `models.py:82-96` |
| `DELETE /v1/models/{id}` | Supprime le modèle du cache | `models.py:100-106` |
| `GET /v1/registry?task=…` | Catalogue distant ; interroge l'API Hugging Face | `models.py:110-118` |
| `GET /v1/audio/voices` | Voix des modèles TTS installés | `models.py:58-64` |
| `GET /health` | État du service | `compose.yaml` (healthcheck) |

**Alias.** `tts-1` et `tts-1-hd` pointent vers `speaches-ai/Kokoro-82M-v1.0-ONNX`, et `whisper-1` vers `Systran/faster-whisper-large-v3` (`[0.8.3] model_aliases.json:2-4`, résolution dans `src/speaches/model_aliases.py:16-23`).

**`speaches-cli model download <id>`** n'est qu'un `POST /v1/models/<id>` (`[0.8.3] packages/speaches-cli/src/speaches_cli/main.py:53-56`). Un simple `curl -X POST` fait la même chose, sans télécharger la CLI depuis PyPI.

### Moteurs TTS pris en charge

Il y en a deux : **Kokoro** (ONNX, `kokoro-onnx` 0.4.5) et **Piper** (`piper-tts` 1.2.0). Voir `[0.8.3] uv.lock` ; détection par les tags Hugging Face `speaches` + `kokoro` ou `piper` (`executors/kokoro/utils.py:26-28`, `executors/piper/utils.py:37-39`).

### Voix françaises

**Kokoro.** Une seule voix française : `ff_siwis`, féminine, langue `fr-fr` (`[0.8.3] src/speaches/executors/kokoro/utils.py:97-98`).

- La langue est déduite de la voix (`kokoro/utils.py:191`, `lang=voice_language`).
- Une voix inconnue renvoie une erreur 422.
- Les noms OpenAI (`alloy`, `echo`, etc.) sont remplacés en silence par `af_heart`, une voix **anglaise** (`speech.py:87-97`).

**Piper.** Dépôts Hugging Face trouvés avec les filtres `onnx` + `speaches` + `piper` et `fr_FR` :

- `speaches-ai/piper-fr_FR-siwis-medium`
- `speaches-ai/piper-fr_FR-siwis-low`
- `speaches-ai/piper-fr_FR-tom-medium`
- `speaches-ai/piper-fr_FR-upmc-medium`
- `speaches-ai/piper-fr_FR-mls-medium`
- `speaches-ai/piper-fr_FR-mls_1840-low`
- `speaches-ai/piper-fr_FR-gilles-low`

Avec Piper, **le champ `voice` est ignoré** : un modèle Piper correspond à une seule voix (`speech.py:127`, « TODO: maybe check voice »). La voix est donc choisie par l'identifiant du modèle. Côté Open Notebook, le Voice ID peut contenir n'importe quelle valeur non vide, par exemple `siwis`.

### Tailles (API Hugging Face, `/api/models/<id>/tree/main`)

Fichiers réellement téléchargés : `model.onnx` + `voices.bin` pour Kokoro, `model.onnx` + `config.json` pour Piper (`kokoro/utils.py:172-174`, `piper/utils.py:162-164`).

| Modèle | Taille |
|---|---|
| `speaches-ai/Kokoro-82M-v1.0-ONNX` | 326 Mo + 28 Mo |
| `speaches-ai/Kokoro-82M-v1.0-ONNX-fp16` | 177 Mo + 28 Mo |
| `speaches-ai/Kokoro-82M-v1.0-ONNX-int8` | 92 Mo + 28 Mo |
| Piper `fr_FR` siwis-medium | 63 Mo |
| Piper `fr_FR` tom-medium | 64 Mo |
| Piper `fr_FR` upmc-medium | 77 Mo |
| Piper `fr_FR` mls-medium | 77 Mo |
| Piper `fr_FR` gilles-low | 63 Mo |
| Piper `fr_FR` siwis-low | 28 Mo |

---

## 4. Modèle STT conseillé sur CPU

STT repose sur faster-whisper 1.1.1 (`[0.8.3] uv.lock`). Le registre accepte tout dépôt Hugging Face de type `library_name=ctranslate2` + `automatic-speech-recognition` (`executors/whisper/utils.py:18-26`).

| Identifiant exact | Taille de `model.bin` | Remarque |
|---|---|---|
| `Systran/faster-whisper-base` | 145 Mo | rapide, moins précis |
| **`Systran/faster-whisper-small`** | 484 Mo | **conseillé sur CPU** par Open Notebook (`local-stt.md:20`) ; multilingue, donc gère le français |
| `Systran/faster-whisper-medium` | 1 528 Mo | plus précis, nettement plus lent sur CPU |
| `deepdml/faster-whisper-large-v3-turbo-ct2` | 1 618 Mo | variante « turbo », taguée ctranslate2 + ASR, donc acceptée ; lourde sur CPU |
| `Systran/faster-whisper-large-v3` | 3 087 Mo | à réserver au GPU (`local-stt.md:22`) |

À éviter pour le français : les modèles `*.en`, par exemple `Systran/faster-distil-whisper-small.en`, l'exemple de la doc Speaches (`docs/usage/speech-to-text.md:21`). Ils ne gèrent que l'anglais.

Sur CPU, on peut forcer `WHISPER__COMPUTE_TYPE=int8` (`config.py:26,63`). Valeur non mesurée ici.

---

## 5. Sécurité

- **Télémétrie désactivée dans l'image** : `DO_NOT_TRACK=1`, `GRADIO_ANALYTICS_ENABLED=False`, `DISABLE_TELEMETRY=1`, `HF_HUB_DISABLE_TELEMETRY=1` (`[0.8.3] Dockerfile:45-50`). L'image locale les contient bien (`docker image inspect`, `Config.Env`).
- **Appels sortants** :
  - vers `huggingface.co` uniquement lors d'un `GET /v1/registry` ou d'un `POST /v1/models/{id}` (`huggingface_hub.list_models` et `snapshot_download`, `models.py:84-89,110-118`) ;
  - `CHAT_COMPLETION_BASE_URL` (Ollama local par défaut, `config.py:112`) n'est contacté que par le temps réel et le chat ;
  - `uv tool run speaches-cli`, la méthode de la doc Open Notebook, télécharge en plus la CLI depuis PyPI dans le conteneur. `curl -X POST` l'évite.
  - Une fois les modèles en cache, TTS et STT fonctionnent sans réseau.
- **Pas d'authentification par défaut** : `api_key` vaut `None` (`config.py:68`). Si `API_KEY` est défini, la clé est exigée sur toutes les routes (`main.py:65-66`). Dans ce cas, renseigner la même clé dans la configuration « OpenAI Compatible » d'Open Notebook.
- **Écoute sur `0.0.0.0`** dans le conteneur (`Dockerfile:38`). La doc Open Notebook publie `"8969:8000"`, ce qui expose le port **sur toutes les interfaces de l'hôte**, et le signale elle-même (`local-tts.md:43`). Deux parades :
  - publier `127.0.0.1:8969:8000` ;
  - mieux, mettre Speaches dans le même compose qu'Open Notebook sans publier de port, avec la Base URL `http://speaches:8000/v1` (`local-tts.md:45`).
- **Interface Gradio** : activée par défaut et montée à la **racine `/`** (`main.py:116-121`), sans authentification. Elle permet de télécharger et d'utiliser les modèles. Pour la couper : `ENABLE_UI=false` (`config.py:86`).
- **Autres expositions** : la console temps réel est servie sur `/v1/realtime` (`main.py:105`). CORS n'est ajouté que si `ALLOW_ORIGINS` est défini (`main.py:107-109`).
- **Journaux** : `LOG_LEVEL=debug` par défaut, et la configuration est journalisée au démarrage (`main.py:62`). La clé est un `SecretStr`, donc masquée. Mettre `LOG_LEVEL=info`.
- **Licence** : MIT (`Dockerfile:5`).

---

## 6. Compatibilité avec Open Notebook 1.15.1

Procédure officielle : `docs/5-CONFIGURATION/local-tts.md` et `local-stt.md` au tag `v1.15.1`.

1. **Lancer Speaches** avec `ghcr.io/speaches-ai/speaches:latest-cpu`, les ports `"8969:8000"` et le volume `hf-hub-cache:/home/ubuntu/.cache/huggingface/hub` (`local-tts.md:17-29`). Le fichier d'exemple `examples/docker-compose-speaches.yml:40-47` reprend exactement ces valeurs.
2. **Télécharger les modèles** (`local-tts.md:52-56`, `local-stt.md:14`) :
   - `docker compose exec speaches uv tool run speaches-cli model download speaches-ai/Kokoro-82M-v1.0-ONNX`
   - puis la même commande avec `Systran/faster-whisper-small`.
3. **Tester** :
   - TTS (`local-tts.md:62-64`) : `curl http://localhost:8969/v1/audio/speech … {"model":"speaches-ai/Kokoro-82M-v1.0-ONNX","voice":"af_bella"}` ;
   - STT (`local-stt.md:29-30`) : `-F "file=@test.mp3" -F "model=Systran/faster-whisper-small"`.
4. **Fournisseur dans Open Notebook** (`local-tts.md:69-80`) : **OpenAI Compatible**, nom « Speaches », **aucune clé API**. Base URL selon le cas :

   | Situation | Base URL |
   |---|---|
   | Open Notebook en Docker sous Linux | `http://host.docker.internal:8969/v1` avec `extra_hosts: ["host.docker.internal:host-gateway"]` sur `open_notebook`, ou `http://172.17.0.1:8969/v1` |
   | Speaches dans le même compose | `http://speaches:8000/v1` |
   | Open Notebook lancé depuis les sources | `http://localhost:8969/v1` |

5. **Discover Models** (`local-tts.md:82-83`) :
   - choisir le type **TTS** et ajouter `speaches-ai/Kokoro-82M-v1.0-ONNX` ;
   - choisir le type **STT** et ajouter le modèle Whisper avec le même identifiant exact (`local-stt.md:24`) ;
   - si un modèle n'apparaît pas, taper son identifiant puis « Add "…" ».

   Ensuite, renseigner *Default Model Assignments* (TTS et STT). Rappel : Speaches ne liste dans `/v1/models` que les modèles **déjà téléchargés**.
6. **Podcasts** (`local-tts.md:89-91`) :
   - dans chaque *speaker profile*, choisir le modèle Speaches et un **Voice ID** Kokoro (exemples de la doc : `af_bella`, `am_adam`, deux voix anglaises). Pour le français, utiliser **`ff_siwis`** (déduit du code Speaches, la doc Open Notebook ne le cite pas) ;
   - les profils fournis utilisent des noms de voix OpenAI et n'ont pas de modèle : il faut les modifier. Sinon Speaches remplace la voix par `af_heart`, en anglais ;
   - sur CPU : `TTS_BATCH_SIZE=1` ou `2` (défaut 5), et augmenter `ESPERANTO_TTS_TIMEOUT` (défaut 300 s).
7. **STT, enregistrements longs** (`local-stt.md:39-43`) :
   - `CCORE_AUDIO_SEGMENT_MINUTES` (défaut 10 ; `0` envoie le fichier entier) ;
   - `CCORE_AUDIO_CONCURRENCY=1` pour un seul serveur CPU ;
   - `CCORE_STT_TIMEOUT` (défaut 3600 s).

**Point de vigilance.** Open Notebook ne demande pas de `response_format` particulier dans ces docs. Or Speaches refuse `opus` et `aac` (`speech.py:32`). Si un client réclame l'un de ces formats, la requête échouera. Non vérifié côté Esperanto.
