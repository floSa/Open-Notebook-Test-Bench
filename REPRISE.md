# Reprise

État au 8 novembre 2026, 23 h. Ce qui tourne, ce qui reste à faire, et comment lancer la solution suivante.

## 1. État

| Élément | État |
|---|---|
| Open Notebook 1.15.1 | en marche : http://127.0.0.1:8502, mot de passe dans `donnees/IDENTIFIANTS-LOCAUX.txt` |
| Carnet de démonstration | « Démo Vélanor » : 9 documents, 3 conversations citées, 2 notes ; un épisode de podcast |
| Modèles | LLM-Service (`~/Projets/Projet-IA/LLM-Service`, branche `service-ollama`), conteneur `ollama-central`, réseau `llm-net` : qwen3:4b-instruct (réponses), bge-m3 (embedding), ministral-3:3b et qwen3:4b (essais) |
| Voix | `rag-speaches` (Kokoro pour la synthèse, faster-whisper-small pour la transcription), réseau `rag-local` |
| Manuels | `docs/open-notebook/` ; commencer par `presentation.md` |
| Banc | 28 réponses justes sur 34, 4 pièges refusés sur 4 ; détails dans `docs/open-notebook/10-qualite-performances.md` |
| Git | branche `master`, aucun commit ne mentionne Claude ; dépôt distant `origin` = https://github.com/floSa/Open-Notebook-Test-Bench, pas encore poussé |

Réglages locaux de LLM-Service, propres à ce portable et non commités dans son dépôt :

| Fichier | Contenu |
|---|---|
| `.env` | `PRELOAD_MODELS=qwen3:4b-instruct bge-m3`, `OLLAMA_CONTEXT_LENGTH=16384`, `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_KEEP_ALIVE=30m`, `OLLAMA_FLASH_ATTENTION=0`, `OLLAMA_KV_CACHE_TYPE=f16` |
| `docker-compose.override.yml` | pas de réservation de GPU ; `LLAMA_ARG_THREADS=8` : sans ce réglage, 16 fils de calcul et 0,4 jeton/s au lieu de 13,3 |

## 2. À faire tout de suite

1. Pousser le dépôt. `git push` est interdit à l'agent par `.claude/settings.json` :

   ```bash
   git push -u origin master
   ```

2. Redémarrer Docker Desktop : dans WSL, le greffon `docker compose` de Docker Desktop renvoie une erreur d'entrée-sortie. Les scripts ont été lancés avec `/usr/libexec/docker/cli-plugins/docker-compose` en contournement.
3. Avant de renommer ce dossier, arrêter l'application (`outils/open-notebook/arreter.sh`), puis la relancer depuis le nouveau chemin (`outils/open-notebook/demarrer.sh`) : les volumes Docker pointent vers `donnees/` par chemin absolu.

## 3. Sur la machine avec GPU (RTX 4060 Ti)

| Tâche | Pourquoi | Où écrire le résultat |
|---|---|---|
| LLM-Service, branche `service-vllm`, avec Qwen3-4B-Instruct en 4 bits et bge-m3 ; ports à republier sur `127.0.0.1` (ils sont aujourd'hui sur toutes les interfaces) | mêmes modèles que le banc CPU, pour comparer | `outils/resultats/socle/` |
| Ajouter un conteneur reranker et un routeur (LiteLLM) devant les serveurs vLLM | un serveur vLLM ne sert qu'un modèle ; une seule adresse pour les applications | dépôt LLM-Service |
| Rejouer le banc d'Open Notebook sur vLLM (fournisseur « OpenAI Compatible », `http://vllm-central:8000/v1`) | mesurer la configuration minimale avec GPU, aujourd'hui estimée | `outils/resultats/open-notebook/banc-*-vllm.json`, manuel 10, `presentation.md` section 5 |
| Rejouer le mode « Demander » sur les 38 questions | inutilisable sur CPU (décision D4) | idem |

## 4. Sans GPU, encore à mesurer

| Tâche | Pourquoi |
|---|---|
| Banc avec un modèle de moins de 3 milliards de paramètres (par exemple qwen3:1.7b) | situer le modèle le plus léger qui garde des réponses justes |
| OCR des scans : `onnxruntime` dans le conteneur d'Open Notebook (décision D3) | les 6 erreurs du banc viennent toutes du scan |

## 5. Lancer RAGFlow dans un nouveau dossier

Le corpus, le banc et les outils communs doivent être identiques d'une solution à l'autre : on les copie depuis ce dépôt.

```bash
mkdir -p ~/Projets/Tutoriels/RAGFlow && cd ~/Projets/Tutoriels/RAGFlow
```

```bash
cp -r ~/Projets/Tutoriels/NotebookLM_Like/{kit,corpus,CLAUDE.md,.claude,.gitignore} . && mkdir -p outils && cp -r ~/Projets/Tutoriels/NotebookLM_Like/outils/communs outils/
```

```bash
git init -q && git add -A && git commit -qm "Kit : prompt, fiches, outils communs et corpus repris d'Open Notebook"
```

```bash
claude --permission-mode auto
```

Puis coller le bloc `/goal` de la section « Lancement » de `kit/fiches/02-ragflow.md`.

Déjà dans le kit :

- les modèles viennent de LLM-Service : aucune solution n'embarque son propre serveur de modèles ;
- même taille de contexte (16 384 jetons) pour toutes les applications et pour le juge du banc ;
- une page `docs/<solution>/presentation.md` au format de celle d'Open Notebook ;
- deux configurations minimales, sans et avec GPU, en langage courant.

Points à surveiller pour RAGFlow : 16 Go de RAM conseillés pour lui seul (il ne restera qu'environ 3 Go pour le modèle sur ce portable) ; Elasticsearch peut demander un réglage système (`vm.max_map_count`) que l'agent n'a pas le droit de faire (`sysctl` interdit) : prévoir le moteur Infinity, ou faire ce réglage soi-même.

## 6. Décisions en attente

| N° | Sujet | À décider |
|---|---|---|
| D1 | Pas de GPU NVIDIA sur ce portable | mesurer le profil GPU sur la machine équipée (section 3) |
| D2 | Conteneurs `rag-ollama`, `rag-agent-api`, `rag-frontend` du projet `~/Projets/rag-agent-chat`, arrêtés | les garder ou les supprimer |
| D3 | OCR de Docling inopérant dans l'image 1.15.1 | autoriser l'installation d'`onnxruntime` dans le conteneur |
| D4 | Mode « Demander » sur CPU | le rejouer avec GPU |
