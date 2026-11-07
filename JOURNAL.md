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
