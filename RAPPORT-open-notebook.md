# Rapport de mission : Open Notebook

Date : 2026-11-08. Machine : Windows 11, WSL2 Ubuntu 24.04, Intel Core Ultra 7 255H (16 fils), 15,3 Go de RAM dans WSL, sans GPU NVIDIA (Intel Arc intégré, invisible pour Docker). Journal détaillé : [JOURNAL.md](JOURNAL.md).

## 1. Ce qui a été installé

| Élément | Version | Conteneur | Port |
|---|---|---|---|
| Open Notebook (interface, API, worker) | 1.15.1, image `lfnovo/open_notebook:1.15.1@sha256:e4e18f12…95812` | `rag-open-notebook` | `127.0.0.1:8502` (interface), `127.0.0.1:5055` (API) |
| SurrealDB | v2.7.0, `sha256:e5d7387e…45723` | `rag-open-notebook-surrealdb` | non publié |
| Service de modèles : LLM-Service (dépôt séparé `~/Projets/Projet-IA/LLM-Service`, branche `service-ollama`, sur CPU) | Ollama 0.30.7 | `ollama-central`, réseau `llm-net`, partagé avec d'autres applications | `127.0.0.1:11434` |
| Serveur de voix : Speaches | 0.8.3-cpu, `sha256:21e3df06…53ef8` | `rag-speaches` | `127.0.0.1:8969` |
| Captures d'écran : Playwright | v1.64.1-noble, conteneur jetable | `rag-captures` (supprimé après usage) | aucun |

Modèles : qwen3:4b-instruct (chat par défaut), ministral-3:3b, qwen3:4b (raisonnement), copiés depuis `~/.ollama` ; bge-m3 (embedding, 1,2 Go téléchargés) ; Kokoro-82M-v1.0-ONNX (synthèse vocale) ; faster-whisper-small (transcription, copié du cache Hugging Face). Docling 2.130.0 activé dans l'application (installé au démarrage, 72 s). Réglage retenu : `num_ctx` 16384.

Installation complète, rejouable : `outils/open-notebook/installer.sh` ([manuel 01](docs/open-notebook/01-installation.md)).

## 2. Où ouvrir la solution

- Dans le navigateur Windows : http://127.0.0.1:8502 (WSL2 relaie `127.0.0.1` vers Windows).
- Mot de passe : dans `donnees/IDENTIFIANTS-LOCAUX.txt` (fichier local, ignoré par git).
- Carnet de démonstration : « Démo Vélanor » (corpus fictif indexé, trois conversations citées, deux notes) ; page **Podcasts** : un épisode à deux voix.
- Contrôle depuis WSL : `curl -I http://127.0.0.1:8502` renvoie `307` vers `/notebooks` ; `outils/open-notebook/etat.sh` résume tout.

## 3. Manuels écrits

Index : [docs/open-notebook/README.md](docs/open-notebook/README.md) ; plan détaillé : [plan-des-manuels.md](docs/open-notebook/plan-des-manuels.md).

| N° | Manuel |
|---|---|
| 00 | [Notions fondamentales](docs/open-notebook/00-notions-fondamentales.md) |
| 01 | [Installation sous Windows et WSL2](docs/open-notebook/01-installation.md) |
| 02 | [Prise en main](docs/open-notebook/02-prise-en-main.md) |
| 03 | [Carnets, sources et formats](docs/open-notebook/03-carnets-sources-formats.md) |
| 04 | [Chat et citations](docs/open-notebook/04-chat-et-citations.md) |
| 05 | [Notes et transformations](docs/open-notebook/05-notes-et-transformations.md) |
| 06 | [Recherche et « Demander »](docs/open-notebook/06-recherche.md) |
| 07 | [Podcasts](docs/open-notebook/07-podcasts.md) |
| 08 | [API REST et MCP](docs/open-notebook/08-api-et-mcp.md) |
| 09 | [Recettes de bout en bout](docs/open-notebook/09-recettes.md) |
| 10 | [Qualité et performances](docs/open-notebook/10-qualite-performances.md) |
| 11 | [Exploitation](docs/open-notebook/11-exploitation.md) |
| 12 | [Dépannage et FAQ](docs/open-notebook/12-depannage.md) |

Exemples exécutables : [exemples/open-notebook/](exemples/open-notebook/), sorties dans [sorties_verifiees.txt](exemples/open-notebook/sorties_verifiees.txt). Glossaire et comparatif : [docs/README.md](docs/README.md).

## 4. Banc en cinq lignes

1. Configuration de référence (chat de carnet, sources en « full content », qwen3:4b-instruct, Docling, `num_ctx` 16384) : 28/34 réponses exactes, 4/4 pièges refusés, médiane 9,1 s, p95 23,8 s, indexation du corpus 126 s ([banc](outils/resultats/open-notebook/banc-2026-11-08-docling-qwen-fullcontent.json)).
2. Les 6 erreurs viennent toutes du PDF scanné : l'OCR de Docling ne fonctionne pas dans l'image 1.15.1 (`onnxruntime` absent).
3. Sans Docling : 25/34 (tableau DOCX perdu) ; ministral-3:3b : 28/34 selon la notation, 27/34 en relecture, p95 44,7 s.
4. `num_ctx` 4096 : 38 erreurs « exceeds the available context size » ; 6144 : 28/34, le corpus entier tient (latences de ce banc faussées par des rechargements du modèle).
5. Le mode « Demander » (Ask) est inutilisable sur CPU avec ce modèle : 74 à 1 089 s par question, 4 réponses vides sur 6.

Tableau complet : [manuel 10, section 2](docs/open-notebook/10-qualite-performances.md#2-résultats).

## 5. Vérifié, non vérifié

Vérifié (résultat brut dans `outils/resultats/`) : installation et ports limités à `127.0.0.1` ; mot de passe actif ; extraction de huit formats avec et sans Docling ; transcription audio ; chat et ses trois modes de contexte ; citations ; recherche plein texte et vectorielle ; transformations ; notes ; podcast ; API REST (exemples 01 à 05) et serveur MCP tiers (exemple 06) ; bancs ; sauvegarde et restauration ; mémoire et débits du socle.

Non vérifié, et pourquoi :

| Point | Raison |
|---|---|
| vLLM et profil GPU (RTX 4060 Ti) | aucun GPU NVIDIA sur la machine ; profil B en [Estimation] dans le manuel 10 |
| Banc complet en mode « Demander » | plusieurs heures sur CPU, et saturation mémoire constatée ; échantillon de 6 questions |
| OCR des PDF scannés | défaut de l'image (D3) ; correction hors enveloppe |
| Sources web (URL, YouTube) | pas d'accès réseau sortant voulu pour des données fictives ; [Source] seulement |
| Mise à jour vers une version suivante | aucune version plus récente à essayer ; procédure en [À tester] |
| Sauvegarde à chaud, usage à plusieurs | non essayés ; l'application est mono-utilisateur [Source] |
| Création d'épisode de podcast par l'interface | essai fait par l'API |

## 6. Incidents

| Incident | Effet | Traitement |
|---|---|---|
| Pas de GPU NVIDIA | vLLM impossible | socle Ollama sur CPU (D1) |
| `python3-venv` absent | pas de `venv` | `uv venv` |
| Image `ubuntu:24.04` tirée pendant le diagnostic, hors des images citées | 119 Mo inutiles | plus utilisée, consignée ; suppression manuelle possible |
| Transcription audio en échec (Base URL STT ignorée par le worker) | message vocal illisible | variables `OPENAI_COMPATIBLE_*_STT/TTS` dans l'override |
| OCR de Docling inopérant | scan illisible | documenté (D3) |
| Faux positif de notation du banc (« 8 » dans « 87 ») | 1 réponse comptée juste à tort | notation corrigée, bancs renotés |
| Saturation de la mémoire de WSL pendant l'échantillon « Demander » (16:10) | WSL « en reconnexion » pendant 36 min | processus arrêtés, modèles déchargés, garde-fou mémoire, essais un par un |
| Worker bloqué après cette saturation | tâche de podcast en attente 1 h | `docker restart rag-open-notebook` |
| Juge du banc à un autre `num_ctx` que le chat | latences du banc 6144 faussées | signalé dans le manuel 10 ; exactitude valide |
| Passage sur LLM-Service : génération à 0,4 jeton/s (16 fils de calcul sur un processeur hybride) | questions en 3 à 5 min | `LLAMA_ARG_THREADS=8` dans l'override local de LLM-Service : 13,3 jetons/s, échantillon de 6 questions identique au banc |
| `pkill -f` qui tuait le shell appelant | essais interrompus | motifs de recherche réécrits |

## 7. Décisions en attente

| N° | Sujet | Option appliquée | À trancher |
|---|---|---|---|
| D1 | Pas de GPU NVIDIA | Ollama sur CPU | rejouer sur une machine NVIDIA pour vLLM, ou accepter le CPU |
| D2 | Anciens conteneurs `rag-ollama`, `rag-agent-api`, `rag-frontend` d'un autre projet | laissés intacts | les renommer ou les supprimer |
| D3 | OCR de Docling (`onnxruntime` absent) | conteneur non modifié | autoriser `pip install onnxruntime` dans le conteneur, ou signaler au projet |
| D4 | Banc « Demander » complet | échantillon | rejouer avec un GPU |

## 8. Disque, RAM et VRAM

Mesures du [relevé de fin de mission](outils/resultats/open-notebook/ressources-2026-11-08.txt) :

| Ressource | Occupation |
|---|---|
| Disque, `donnees/` | 16 Go : modèles Ollama 8,5 Go, modèles de voix 1,3 Go, Open Notebook 6,2 Go (dont 6,2 Go de cache Docling), sauvegarde 5,5 Mo, Playwright 144 Mo |
| Disque, images Docker | Open Notebook 2,46 Go, Ollama 8,25 Go, Speaches 3,04 Go, Playwright 3,53 Go, SurrealDB 118 Mo |
| RAM au repos | application 1,3 Go, SurrealDB 95 Mo, Speaches 0,4 Go, Ollama 8,9 Go tant que qwen3:4b-instruct reste chargé (déchargé après 30 min sans requête) |
| RAM en pointe | application 3,8 Go (indexation avec Docling) ; Ollama 10 Go ; au total, la limite des 15,3 Go de WSL a été atteinte une fois (incident du §6) |
| VRAM | sans objet (aucun GPU NVIDIA) |

## 9. Arrêter ou supprimer

```bash
outils/open-notebook/arreter.sh
```

```bash
outils/open-notebook/arreter.sh --voix
```

La première commande arrête l'application en gardant les données ; la seconde arrête aussi le serveur de voix. LLM-Service n'est pas arrêté : il sert d'autres applications (`make down` dans son dépôt). Redémarrage : `outils/open-notebook/demarrer.sh`.

Suppression complète (jamais lancée automatiquement, confirmation demandée) :

```bash
outils/communs/nettoyer.sh open-notebook
```

Avec `--socle`, elle supprime aussi le serveur de voix, le réseau `rag-local` et `donnees/socle/` ; LLM-Service n'est jamais touché ([manuel 01, désinstallation](docs/open-notebook/01-installation.md)). Les images Docker ne sont pas supprimées ; `docker image rm` à la main si besoin.

## 10. Proposition pour la solution suivante

RAGFlow (fiche 02), dans l'ordre des fiches. Points tirés de cette mission :

- Se brancher sur LLM-Service (`http://ollama-central:11434`, réseau `llm-net`) et sur le serveur de voix `rag-speaches` ; réutiliser le corpus, le banc et le vérificateur, déjà rejouables.
- RAGFlow embarque Elasticsearch ou Infinity, MySQL, Redis et MinIO : prévoir 4 à 6 Go de RAM de plus que l'application [Estimation]. Sur 15,3 Go, n'avoir qu'un modèle de chat chargé et `OLLAMA_NUM_PARALLEL=1` pendant les essais, et garder le garde-fou mémoire.
- RAGFlow fait de l'OCR et une recherche hybride avec reranker : c'est là que le corpus devrait départager les deux solutions (scan, multi-documents).
- Fixer le `num_ctx` du juge du banc sur celui du chat pour éviter les rechargements du modèle.
- Décider D1 avant de commencer si une machine NVIDIA est disponible : la branche `service-vllm` de LLM-Service est la cible pour plusieurs utilisateurs.
