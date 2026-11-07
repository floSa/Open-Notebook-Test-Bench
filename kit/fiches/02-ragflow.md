# Fiche 02. RAGFlow

| Champ | Valeur |
|---|---|
| Identifiant `<solution>` | `ragflow` |
| Dépôt | https://github.com/infiniflow/ragflow |
| Documentation | https://ragflow.io/docs/dev/ · modèles : https://ragflow.io/docs/supported_models |
| Licence | Apache-2.0 |
| Version à décrire | La 1.0.0 finale si elle est publiée ; sinon la release candidate la plus récente (v1.0.0-rc2 au 7 novembre 2026). Ne pas décrire la branche 0.x. Noter l'écart de version dans « Ce qui reste ouvert ». |
| Public | Utilisateur technique à l'aise avec un terminal, pas forcément développeur |
| Interface | Port HTTP par défaut 80 : le republier sur `127.0.0.1:8080` (variable `SVR_WEB_HTTP_PORT` ou override) |
| API | API HTTP (port 9380 par défaut) et SDK Python `ragflow-sdk` |
| Services | RAGFlow (Admin, Ingestor, Syncer, API), MySQL, MinIO, moteur documentaire (Infinity ou Elasticsearch), et autres selon `docker/docker-compose.yml` |
| Besoins indicatifs | Application seule, modèles exclus : 16 Go de RAM conseillés par le projet, 50 Go de disque, plus de 9 Go d'images. À mesurer service par service. |

## Particularités connues

Relevé du 7 novembre 2026, à revérifier au cadrage.

- Installation : `git clone`, `git checkout <tag>`, puis `docker compose -f docker/docker-compose.yml up -d` depuis `docker/`. Réglages dans `docker/.env`. Appliquer les changements par un fichier d'override plutôt qu'en modifiant les fichiers suivis.
- Moteur documentaire : choisir **Infinity**. Elasticsearch exige `vm.max_map_count ≥ 262144` sur l'hôte Docker, réglage interdit par l'enveloppe (sysctl). Si Infinity échoue, consigner l'échec et inscrire Elasticsearch dans les décisions en attente, avec la commande que l'utilisateur devra lancer lui-même.
- RAM : les 16 Go conseillés couvrent la pile de l'application, sans les modèles (moteur de recherche, MySQL, MinIO, file de messages, services RAGFlow, modèles de vision DeepDoc chargés sur CPU). Mesurer chaque service au repos et en indexation. Si la pile ne démarre pas faute de RAM, c'est un bloquant ; le rapport donne le réglage `.wslconfig` (`memory=`) à faire par l'utilisateur.
- Santé : `curl -f http://127.0.0.1:<port>/api/v1/system/healthz` doit renvoyer HTTP 200 avant d'ouvrir l'interface.
- DeepDoc (OCR, structure des tableaux, mise en page) tourne sur CPU dans la 1.0 : mesurer le temps d'analyse par page.
- Après la connexion, il faut déclarer un LLM, un modèle d'embedding et un reranker dans « Model providers », tous servis par le socle vLLM.
- macOS n'est pas pris en charge ; sans objet ici (WSL2).
- Fonctions à couvrir : datasets et gabarits de découpage (General, Q&A, Table, Paper, Book, Laws, Presentation, Picture… selon la version), visualisation et correction des chunks, assistants de chat avec citations, Agentic RAG et ses niveaux de réflexion, Knowledge Compilation (wikis, graphes, mind maps, timelines), agents et gabarits, ingestion de sites par sitemap, synchronisation de sources, API et SDK, comptes et administration.

## Branchement au socle

- Joindre les services au réseau `rag-local`.
- Chat : `http://rag-vllm-chat:8000/v1`. Embedding : `http://rag-vllm-embed:8001/v1`. Reranker, s'il existe : `http://rag-vllm-rerank:8002`.
- Dans Model providers : fournisseur « VLLM » natif (chat, embedding, rerank) ; sinon « OpenAI-API-Compatible ».
- Régler découpage, top-k et historique pour rester dans le budget de contexte du socle.
- Repli seulement si vLLM échoue : Ollama, `http://rag-ollama:11434`.

## Thèmes des manuels 03 et suivants

1. Datasets et découpage : gabarits comparés sur le corpus (au moins General, Table, Paper et Presentation), effet sur le banc.
2. DeepDoc : scans, tableaux, mise en page ; correction manuelle des chunks.
3. Assistants de chat et citations : réglages de recherche (top-k, seuil de similarité, poids mots-clés et vecteurs, reranker).
4. Agentic RAG : niveaux de réflexion comparés (qualité, latence).
5. Knowledge Compilation : ce que chaque type d'artefact produit sur le corpus.
6. Agents et gabarits : un flux complet.
7. Sources externes : sitemap d'un site local de test, synchronisation.
8. API HTTP et SDK Python : automatiser datasets, ingestion et questions.

## Hors périmètre

Offre cloud RAGFlow, fournisseurs payants (en [Source] seulement), lancement depuis les sources (Go), connecteurs qui exigent un compte en ligne.

## Adaptateur du banc

Via le SDK Python ou l'API HTTP : créer un dataset « Banc » (gabarit General), téléverser le corpus, lancer l'analyse et attendre la fin, créer un assistant de chat lié au dataset, poser chaque question et relever la réponse et les références (document, chunk, page si exposée). Rejouer avec le meilleur gabarit trouvé et avec un niveau d'Agentic RAG.

## Lancement

Coller dans Claude Code, à la racine du dépôt :

```text
/goal Exécuter kit/PROMPT.md pour la fiche kit/fiches/02-ragflow.md, en autonomie complète, sans jamais attendre de réponse. J'autorise explicitement, pour cette mission : git clone du dépôt officiel de RAGFlow ; docker pull, docker compose et docker run des images officielles citées dans la fiche et dans kit/PROMPT.md ; lecture seule des modèles déjà présents sur la machine, dans les dossiers usuels et dans MODELES_EXISTANTS=<chemin facultatif> ; téléchargement de modèles Hugging Face seulement s'ils manquent, dans la limite de 30 Go ; un téléchargement total (images et modèles) de 150 Go au plus ; la création d'environnements Python dans .venv du dépôt et l'installation de paquets PyPI dedans ; la création de comptes locaux fictifs dans l'outil testé ; git add et git commit locaux. Interdit : sudo, sysctl, git push, port publié hors de 127.0.0.1, compte en ligne, dépense, curl | bash, docker prune, suppression hors du dépôt et des ressources Docker préfixées rag-. Objectif atteint quand, preuves affichées dans la conversation : RAPPORT-ragflow.md existe et couvre les rubriques de la phase H ; python3 outils/communs/verifier_docs.py affiche 0 point ; exemples/ragflow/sorties_verifiees.txt couvre chaque exemple ; un fichier outils/resultats/ragflow/banc-*.json existe ; curl sur l'URL locale de RAGFlow répond ; git status est propre après le commit final. Sinon, arrêt après 300 tours avec JOURNAL.md et RAPPORT-ragflow.md à jour.
```
