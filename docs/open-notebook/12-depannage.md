# 12. Dépannage et FAQ

> **Objet** : retrouver vite la cause d'un problème rencontré avec Open Notebook et son socle local, à partir des échecs réellement observés pendant les essais.
> **Prérequis** : [01. Installation](01-installation.md).
> **Version décrite** : Open Notebook 1.15.1, SurrealDB 2.7.0, Ollama 0.40.15 (essais du 8 novembre faits sur 0.30.7 ; banc de référence rejoué sur 0.40.15) sur CPU, Speaches 0.8.3, Docling 2.130.0 ; Docker 29.9.2, Compose 5.6.1, WSL 2.7.14.
> **Statut des informations** : [Vérifié] observé ou mesuré le 2026-11-08 sur la machine d'essai (Intel Core Ultra 7 255H, sans GPU NVIDIA) ; [Source] documentation officielle ou code source au tag v1.15.1 ; [Estimation] calcul non mesuré ; [À tester] non documenté et non essayé.
> **Précautions** : chaque ligne marquée [Vérifié] renvoie au journal où l'échec apparaît.

## Sommaire

1. [Installation et démarrage](#1-installation-et-démarrage)
2. [Sources et extraction](#2-sources-et-extraction)
3. [Chat, contexte et modèles](#3-chat-contexte-et-modèles)
4. [API, MCP et automatisation](#4-api-mcp-et-automatisation)
5. [FAQ](#5-faq)
6. [Dépannage](#dépannage)
7. [Sources](#sources)

## 1. Installation et démarrage

### Essentiel

| Symptôme | Cause probable | Action | Statut |
|---|---|---|---|
| `docker run --gpus all` : « failed to discover GPU vendor from CDI: no known GPU vendor found » | aucun GPU NVIDIA (ici Intel Arc intégré) | socle Ollama sur CPU ; vLLM exige un GPU NVIDIA | [Vérifié] ([diagnostic](../../outils/resultats/machine/diagnostic-2026-11-08.json)) |
| `python3 -m venv .venv` : « ensurepip is not available » | paquet `python3-venv` absent | `uv venv .venv` (sans sudo) | [Vérifié] ([sortie](../../outils/resultats/machine/venv-ensurepip-2026-11-08.txt)) |
| L'installateur attend deux minutes alors que l'API est « healthy » | l'interface répond 307 vers `/notebooks` | accepter 200 ou 307 (corrigé dans `installer.sh`) | [Vérifié] ([journal](../../outils/resultats/open-notebook/installation-2026-11-08.log)) |
| `cp: warning: behavior of -n is non-portable` | coreutils récent | `cp --update=none` | [Vérifié] |
| Tâches de fond jamais traitées | namespace ou base SurrealDB différents entre API et worker | fixer `SURREAL_NAMESPACE` et `SURREAL_DATABASE` | [Source] |
| Premier démarrage long après activation de Docling | installation de 65 paquets | attendre ; 72 s mesurées | [Vérifié] |

### Pour aller plus loin

`outils/open-notebook/etat.sh` résume conteneurs, ports, santé de l'API et de l'interface, mémoire et modèles chargés.

## 2. Sources et extraction

### Essentiel

| Symptôme | Cause probable | Action | Statut |
|---|---|---|---|
| PDF scanné : « Could not extract any text content from this source » | pas d'OCR sans Docling | OCR préalable du PDF | [Vérifié] |
| Avec Docling : « No OCR engine found » | `onnxruntime` absent de l'installation de Docling | voir [03, section 3](03-carnets-sources-formats.md#3-docling--tableaux-et-ocr) | [Vérifié] ([preuve](../../outils/resultats/open-notebook/essai-docling-ocr-2026-11-08.log)) |
| Audio : « Content extraction is not configured correctly » ; journal : « OpenAI-compatible base URL is required » | Base URL STT non transmise au worker | `OPENAI_COMPATIBLE_BASE_URL_STT` et `OPENAI_COMPATIBLE_API_KEY_STT` | [Vérifié] pour le message de l'interface ([formats sans Docling](../../outils/resultats/open-notebook/formats-2026-11-08-sans-docling.json)) ; message du journal relevé pendant l'essai, extrait non conservé |
| Réponses fausses sur un tableau Word | tableau DOCX non extrait par le moteur simple | activer Docling et réimporter | [Vérifié] |
| Source « completed » mais absente de la recherche vectorielle | embedding pas encore calculé, ou ajouté sans embedding | attendre `embedded_chunks > 0` | [Source] |

### Pour aller plus loin

Le message affiché dans l'interface est court ; le détail est dans `docker logs rag-open-notebook`.

## 3. Chat, contexte et modèles

### Essentiel

| Symptôme | Cause probable | Action | Statut |
|---|---|---|---|
| Chat : « AI service error … request (4238 tokens) exceeds the available context size (4096 tokens) » (HTTP 502) | prompt plus long que `num_ctx` | réduire les sources en « full content » ou augmenter `num_ctx` | [Vérifié] ([banc](../../outils/resultats/open-notebook/banc-2026-11-08-docling-qwen-fullcontent-ctx4096.json)) |
| Appel direct à Ollama (`/api/generate`) : réponse sans erreur mais qui ignore le début du texte | troncature silencieuse (`truncated = 1` dans le journal d'Ollama) | même action | [Vérifié] ([mesures](../../outils/resultats/socle/mesures-2026-11-08-passe2.json)) |
| Première question très lente (une à deux minutes), suivantes rapides | lecture complète du prompt sur CPU, puis réutilisation du cache de préfixe d'Ollama | normal ; garder le même contexte d'une question à l'autre | [Vérifié] |
| Délai dépassé sur un long traitement | `ESPERANTO_LLM_TIMEOUT` à 180 s par défaut | 900 s dans l'override | [Source] |
| Réponses en plusieurs minutes, Ollama à plus de 1 500 % de CPU, 0,4 jeton/s | Ollama lance un fil par cœur vu par WSL (16 sur ce processeur hybride) | `LLAMA_ARG_THREADS=8` dans l'environnement du conteneur Ollama : 13,3 jetons/s | [Vérifié] ([mesures](../../outils/resultats/socle/migration-llm-service-2026-11-08.txt)) |
| Mémoire saturée avec un grand contexte | mémoire de contexte proportionnelle à `num_ctx` et aux requêtes simultanées | `num_ctx` 16384 au plus sur 16 Go ; `OLLAMA_NUM_PARALLEL=1` | [Estimation] |

### Pour aller plus loin

Voir [Chat et citations](04-chat-et-citations.md) et [Qualité et performances](10-qualite-performances.md).

## 4. API, MCP et automatisation

### Essentiel

| Symptôme | Cause probable | Action | Statut |
|---|---|---|---|
| `401 Missing authorization header` | mot de passe actif | en-tête `Authorization: Bearer <mot de passe>` | [Vérifié] |
| `422` sur `POST /api/sources` en JSON | la route n'accepte qu'un formulaire multipart | `curl -F` ou `POST /api/sources/json` | [Source] |
| MCP `create_source` : « Field required … type » | défaut du serveur tiers 0.3.0 | ajouter la source par l'API REST | [Vérifié] ([sortie](../../exemples/open-notebook/sorties_verifiees.txt)) |
| Import du serveur MCP en échec | SDK `mcp` 2.x installé | `"mcp<2"` | [Source] |
| Capture Playwright : « Timeout 30000ms exceeded » sur `networkidle` | l'interface interroge l'API en continu | attendre l'événement `load` puis un délai fixe | [Vérifié] (consigné dans `JOURNAL.md`, sans journal brut) |

### Pour aller plus loin

Le banc lui-même a connu un faux positif de notation (« 8 » reconnu dans « 87 ») ; la notation exige désormais que les nombres ne soient pas collés à d'autres chiffres, et les résultats ont été renotés ([outil](../../outils/communs/banc/renoter.py)).

## 5. FAQ

### Essentiel

- **Faut-il un GPU ?** Non : tout a tourné sur CPU, avec 6 à 25 s par question une fois le contexte en cache (médiane 9 s) [Vérifié]. Un GPU NVIDIA réduit fortement le temps de lecture du prompt [Estimation].
- **Les citations donnent-elles la page ?** Non : la source seulement [Source].
- **Plusieurs utilisateurs ?** Un seul mot de passe, pas de comptes [Source] ([Exploitation](11-exploitation.md)).
- **L'interface est en anglais ?** Elle suit la langue du navigateur ; bouton **Langue** en bas à gauche [Vérifié].

### Pour aller plus loin

Les questions non résolues sont listées dans « Ce qui reste ouvert » de l'[index](README.md#ce-qui-reste-ouvert).

## Dépannage

Ce manuel est lui-même le tableau de dépannage de la série pour Open Notebook ; chaque manuel a aussi sa propre section.

| Symptôme | Cause probable | Action |
|---|---|---|
| Problème absent de ce manuel | cas non rencontré pendant les essais | lire `docker logs rag-open-notebook` et `docker logs ollama-central` |

## Sources

- Journaux d'essai : `outils/resultats/open-notebook/` ; mesures du socle : `outils/resultats/socle/`
- Documentation officielle : https://github.com/lfnovo/open-notebook/tree/v1.15.1/docs/6-TROUBLESHOOTING
