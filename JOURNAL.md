# Journal de la mission

Solution en cours : Open Notebook (`kit/fiches/01-open-notebook.md`).

## Décisions en attente

| N° | Décision | Option retenue (la plus prudente) | À trancher par l'utilisateur |
|---|---|---|---|
| D1 | La machine d'exécution n'a pas de GPU NVIDIA (Intel Arc 140T intégré, invisible pour Docker). Le §2 du prompt prévoit l'arrêt ; le `/goal` exige d'aller au critère de fin. | Socle sur CPU avec Ollama (repli prévu par la fiche), image locale `ollama/ollama` 0.30.7 figée par empreinte, modèles déjà présents copiés depuis `~/.ollama`. vLLM non installé. Profil A mesuré sur CPU ; profil B (RTX 4060 Ti 16 Go) en [Estimation]. | Relancer la mission sur une machine NVIDIA pour mesurer vLLM, ou accepter le socle CPU. |
| D2 | Des conteneurs `rag-ollama`, `rag-agent-api`, `rag-frontend` existent déjà (autre projet `rag-agent-chat`, arrêtés). | Ne pas y toucher. Conteneur du socle nommé `rag-socle-ollama`, avec l'alias réseau `rag-ollama` sur le réseau `rag-local`. `nettoyer.sh` ne vise que des noms explicites. | Renommer ou supprimer l'ancien projet si souhaité. |

## Entrées

### 2026-11-08 13:15 — Phase A, diagnostic

- Fait : extraction du kit, `git init`, commit du kit ; `outils/communs/diagnostic.sh` écrit et lancé.
- Résultat : Intel Core Ultra 7 255H (16 fils), 15,3 Go de RAM et 4 Go de swap dans WSL, 619 Go libres, Docker 29.9.2, Compose 5.6.1, WSL 2.7.14. Aucun GPU NVIDIA : `nvidia-smi` absent, `docker run --gpus all` échoue (« no known GPU vendor found »). Registres joignables, port publié sur 127.0.0.1 joignable depuis WSL.
- Version d'Open Notebook retenue : 1.15.1 (publiée le 2026-11-04), image `lfnovo/open_notebook:1.15.1@sha256:e4e18f12653df5bf48674b7b187c4252be52238b4d706330fd30d9b177b95812`.
- Fichiers : `outils/communs/diagnostic.sh`, `outils/resultats/machine/diagnostic-2026-11-08.json`, `JOURNAL.md`, `.gitignore`.
- Suite : phase B, socle CPU (inventaire des modèles, Ollama, corpus, banc).

### 2026-11-08 13:20 — Phase B (en cours) et phase C, cadrage

- Fait : socle Ollama CPU (`outils/communs/socle.sh`), inventaire de 22 modèles présents, choix qwen3:4b-instruct (chat), ministral-3:3b (second modèle), bge-m3 (embedding, seul téléchargement, 1,2 Go) ; corpus Vélanor reproductible à l'octet (8 documents, `corpus/MANIFEST.json`) ; 36 questions de référence ; banc commun et son auto-contrôle ; `verifier_docs.py` ; `nettoyer.sh`. Cadrage d'Open Notebook 1.15.1 par sous-agent (`outils/resultats/open-notebook/cadrage-source.md`), relecture consignée (`relecture.md`), compose officiel copié et override écrit, scripts installer/démarrer/arrêter/état, plan des manuels.
- Résultat : Ollama CPU, 16 à 17 jetons/s en génération, 53 à 67 jetons/s en lecture de prompt (mesures en cours). Constats de cadrage : chat de carnet sans top-k (sources injectées en entier), citations seulement `[source:id]` dans le texte, OCR des scans seulement avec Docling.
- Incident : `python3-venv` absent (sudo exclu) ; `.venv` créé avec `uv`. L'image `ubuntu:24.04` a été tirée par le premier test GPU, hors liste des images autorisées ; elle n'est plus utilisée (diagnostic et nettoyage passent par l'image Ollama) et n'a pas été supprimée (suppression hors `rag-` interdite).
- Fichiers : `outils/communs/*`, `outils/open-notebook/*`, `outils/resultats/open-notebook/*`, `docs/glossaire.md`, `docs/open-notebook/plan-des-manuels.md`, `outils/README.md`.
- Suite : fin des mesures du socle, puis phase D (installation testée).
