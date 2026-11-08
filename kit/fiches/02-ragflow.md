# Fiche 02. RAGFlow

| Champ | Valeur |
|---|---|
| Identifiant `<solution>` | `ragflow` |
| Dépôt | https://github.com/infiniflow/ragflow |
| Documentation | https://ragflow.io/docs/dev/ · modèles : https://ragflow.io/docs/supported_models |
| Licence | Apache-2.0 |
| Version à décrire | La dernière version stable, relevée par `outils/communs/versions.py ragflow infiniflow/ragflow=<tag>` au cadrage : v1.0.0 (publiée le 6 novembre 2026) ou une 1.0.x plus récente. Préversions, `nightly` et branche 0.x exclues. `ragflow-sdk` à la même version que le serveur. |
| Public | Utilisateur technique à l'aise avec un terminal, pas forcément développeur |
| Interface | Port HTTP par défaut 80 : le republier sur `127.0.0.1:8080`. Tous les autres ports du compose (443, 9380, administration, MySQL, MinIO, moteur documentaire, Redis) : sur `127.0.0.1` ou retirés (`ports: !override` dans un override par service). Conteneurs renommés `rag-ragflow-*` (`container_name`), projet compose `rag-ragflow`, réglages dans un fichier `--env-file` du dépôt plutôt que dans le `docker/.env` suivi. |
| API | API HTTP (port 9380 par défaut) et SDK Python `ragflow-sdk` |
| Services | RAGFlow (Admin, Ingestor, Syncer, API), MySQL, MinIO, moteur documentaire (Infinity ou Elasticsearch), et autres selon `docker/docker-compose.yml` |
| Besoins indicatifs | Application seule, modèles exclus : 16 Go de RAM conseillés par le projet, 50 Go de disque, plus de 9 Go d'images. Sur la machine A (15,3 Go dans WSL, dont 5 à 6 Go pour Ollama), la pile doit être réduite (voir « RAM »). À mesurer service par service. |

## Particularités connues

Relevé du 7 novembre 2026, à revérifier au cadrage.

- Installation : `git clone`, `git checkout <tag>`, puis `docker compose -f docker/docker-compose.yml up -d` depuis `docker/`. Réglages dans `docker/.env`. Appliquer les changements par un fichier d'override plutôt qu'en modifiant les fichiers suivis.
- Moteur documentaire : Elasticsearch exige `vm.max_map_count ≥ 262144` ; la VM de Docker Desktop de la machine A l'a déjà (262144, lu sans rien modifier) : le relire en phase A. Prendre le moteur par défaut du compose au tag choisi ; mesurer la RAM d'Infinity et d'Elasticsearch si les deux sont proposés, et garder le plus léger qui fonctionne. Ne jamais lancer `sysctl` : si la valeur manque, inscrire la commande dans les décisions en attente.
- RAM : les 16 Go conseillés couvrent la pile de l'application, sans les modèles (moteur de recherche, MySQL, MinIO, file de messages, services RAGFlow, modèles de vision DeepDoc chargés sur CPU). Avant de démarrer : arrêter Open Notebook (`~/Projets/Tutoriels/Open-Notebook-Test-Bench/outils/open-notebook/arreter.sh`), relever `free -m`. Réductions à appliquer d'abord, puis mesurer : `MEM_LIMIT` et mémoire Java d'Elasticsearch (ou limites d'Infinity), une seule tâche d'analyse à la fois (`MAX_CONCURRENT_TASKS=1` ou équivalent), un seul modèle chargé dans Ollama. Mesurer chaque service au repos et en indexation. Bloquant seulement si la pile ne démarre toujours pas : le rapport donne alors le réglage `.wslconfig` (`memory=`) à faire par l'utilisateur.
- Santé : `curl -f http://127.0.0.1:<port>/api/v1/system/healthz` doit renvoyer HTTP 200 avant d'ouvrir l'interface.
- DeepDoc (OCR, structure des tableaux, mise en page) tourne sur CPU dans la 1.0 : mesurer le temps d'analyse par page. Ses modèles se téléchargent depuis Hugging Face au premier usage : les compter dans le budget.
- Fonctions coûteuses sur CPU (16 jetons/s en génération) : Knowledge Compilation (graphes, RAPTOR, wikis), Agentic RAG à haut niveau de réflexion, agents. Les essayer sur un document court, avec la limite de 30 minutes du prompt ; consigner la durée. Le gabarit Picture exige un modèle de vision : petit modèle de vision tiré dans LLM-Service dans le budget, sinon [À tester].
- Après la connexion, il faut déclarer un LLM et un modèle d'embedding dans « Model providers », servis par LLM-Service. Reranker : Ollama n'en sert pas ; vérifier au cadrage si RAGFlow en embarque un ; sinon banc sans reranker, reranking en [À tester].
- macOS n'est pas pris en charge ; sans objet ici (WSL2).
- Fonctions à couvrir : datasets et gabarits de découpage (General, Q&A, Table, Paper, Book, Laws, Presentation, Picture… selon la version), visualisation et correction des chunks, assistants de chat avec citations, Agentic RAG et ses niveaux de réflexion, Knowledge Compilation (wikis, graphes, mind maps, timelines), agents et gabarits, ingestion de sites par sitemap, synchronisation de sources, API et SDK, comptes et administration.

## Branchement à LLM-Service

- Rejoindre le réseau externe `llm-net` (modèles) ; `rag-local` pour la voix si RAGFlow transcrit l'audio.
- Sans GPU (branche `service-ollama`) : chat qwen3:4b-instruct et embedding bge-m3 sur `http://ollama-central:11434`, fournisseur « Ollama » ; si RAGFlow fait varier `num_ctx` d'une requête à l'autre (à vérifier dans son code au cadrage), passer par « OpenAI-API-Compatible » sur `http://ollama-central:11434/v1` pour garder le contexte fixe de 16 384 jetons.
- Avec GPU (branche `service-vllm`) : fournisseur « VLLM » natif ou « OpenAI-API-Compatible », `http://vllm-central:8000/v1` (chat) et `http://vllm-embed:8000/v1` (embedding).
- Régler découpage, top-k et historique pour rester dans 16 384 jetons de contexte.
- Aucun serveur de modèles dans la pile RAGFlow : si le compose officiel en propose un, l'override le retire.

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
/goal Exécuter kit/PROMPT.md pour la fiche kit/fiches/02-ragflow.md, en autonomie complète, sans jamais attendre de réponse. J'autorise explicitement, pour cette mission : git clone du dépôt officiel de RAGFlow ; docker pull, docker compose et docker run des images officielles citées dans la fiche et dans kit/PROMPT.md ; lecture seule des modèles déjà présents sur la machine ; téléchargement de modèles seulement s'ils manquent (modèles Ollama par ollama pull dans LLM-Service, modèles DeepDoc et autres modèles propres à RAGFlow depuis Hugging Face), dans la limite de 30 Go ; un téléchargement total (images et modèles) de 150 Go au plus ; la création d'environnements Python dans .venv du dépôt et l'installation de paquets PyPI dedans ; la création de comptes locaux fictifs dans l'outil testé ; le démarrage du service de modèles commun LLM-Service (~/Projets/Projet-IA/LLM-Service, outils/communs/llm_service.sh) et l'ajout de modèles dedans, sans modifier ses fichiers suivis par git ; git add et git commit locaux. Interdit : sudo, sysctl, pkill -f, git push, port publié hors de 127.0.0.1, compte en ligne, dépense, curl | bash, docker prune, suppression hors du dépôt et des ressources Docker préfixées rag-. Objectif atteint quand, preuves affichées dans la conversation : RAPPORT-ragflow.md existe et couvre les rubriques de la phase H ; python3 outils/communs/verifier_docs.py affiche 0 point ; exemples/ragflow/sorties_verifiees.txt couvre chaque exemple ; un fichier outils/resultats/ragflow/banc-*.json existe ; curl sur l'URL locale de RAGFlow répond ; docker ps montre chaque port lié à 127.0.0.1 ; README.md, LICENSE, docs/ragflow/presentation.md (avec les configurations minimales sans et avec GPU) et outils/resultats/ragflow/versions-*.json existent ; git status est propre après le commit final. Sinon, arrêt après 300 tours avec JOURNAL.md et RAPPORT-ragflow.md à jour.
```
