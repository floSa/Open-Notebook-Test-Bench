# Fiche 01. Open Notebook

| Champ | Valeur |
|---|---|
| Identifiant `<solution>` | `open-notebook` |
| Dépôt | https://github.com/lfnovo/open-notebook |
| Documentation | https://github.com/lfnovo/open-notebook/tree/main/docs · https://www.open-notebook.ai |
| Licence | MIT |
| Version à décrire | Dernière version publiée (tag ou image `lfnovo/open_notebook`). Remplacer l'étiquette flottante `v1-latest` par la version exacte et l'empreinte de l'image. |
| Public | Utilisateur technique à l'aise avec un terminal, pas forcément développeur |
| Interface | `http://127.0.0.1:8502` |
| API | `http://127.0.0.1:5055` (documentation OpenAPI sur `/docs`) |
| Services | `open_notebook` (interface, API, worker) et `surrealdb` |
| Besoins indicatifs | Léger : quelques Go de RAM et de disque, hors modèles |

## Particularités connues

Relevé du 7 novembre 2026, à revérifier au cadrage.

- Installation officielle par `docker-compose.yml` téléchargé depuis le dépôt (deux services). Variable obligatoire `OPEN_NOTEBOOK_ENCRYPTION_KEY` : la générer localement (`openssl rand -hex 32`) et la ranger dans `donnees/IDENTIFIANTS-LOCAUX.txt`.
- Par défaut, l'interface et l'API écoutent sur toutes les interfaces, sans mot de passe. Le README recommande `127.0.0.1:8502:8502` et `127.0.0.1:5055:5055`, ou `OPEN_NOTEBOOK_PASSWORD`. Appliquer les deux.
- Les fournisseurs de modèles se configurent dans l'interface (Models, puis Add Configuration). Le fournisseur « OpenAI Compatible » demande une Base URL ; il faut au moins un modèle de langage et un modèle d'embedding, puis « Auto-assign Defaults ».
- Le socle ne fournit pas de synthèse vocale (TTS). Pour les podcasts et les sources audio ou vidéo en 100 % local, il faut un serveur local compatible OpenAI pour la voix (par exemple Speaches pour STT et TTS, ou Kokoro-FastAPI pour TTS). Relire le projet retenu avant installation, utiliser son image Docker officielle. Si aucun ne fonctionne, marquer podcasts et sources audio en [À tester] et le noter dans les décisions en attente.
- Fonctions à couvrir : carnets (notebooks), sources, notes, chat avec citations, recherche plein texte et vectorielle, transformations, podcasts multi-voix (profils d'épisode et de locuteur), API REST, intégration MCP, mot de passe.

## Branchement à LLM-Service

- Réseau externe `llm-net` (modèles) ; `rag-local` pour la voix. Aucun serveur de modèles dans la pile de la solution.
- Sans GPU (`service-ollama`) : `http://ollama-central:11434` (fournisseur Ollama) ou `http://ollama-central:11434/v1` (compatible OpenAI), modèles qwen3:4b-instruct et bge-m3, contexte 16 384 jetons. Avec GPU (`service-vllm`) : `http://vllm-central:8000/v1` (chat), `http://vllm-embed:8000/v1` (embedding). Voir `kit/PROMPT.md`, phase B.
- Dans Models : fournisseur « OpenAI Compatible » pour le langage et l'embedding.
- Régler découpage, top-k et historique pour rester dans 16 384 jetons de contexte.
- Reranker : Ollama n'en sert pas ; reranker intégré à la solution s'il existe, sinon [À tester].

## Thèmes des manuels 03 et suivants

1. Carnets, sources et formats : PDF, Office, web, audio et vidéo ; ce qui est extrait et ce qui ne l'est pas (scan, tableaux).
2. Chat et citations : contexte choisi par source, qualité des citations, modèles de raisonnement.
3. Notes et transformations : intégrées et personnalisées.
4. Recherche : plein texte et vectorielle, différences mesurées.
5. Podcasts : profils, nombre de voix, durée, langue française, serveur de voix local.
6. API REST et MCP : automatiser l'ingestion et les questions ; brancher un client MCP.

## Hors périmètre

Fournisseurs cloud payants (mentionnés en [Source] seulement), déploiement sur serveur distant.

## Adaptateur du banc

Via l'API REST : créer un carnet « Banc », ajouter les sources du corpus, attendre la fin du traitement, poser chaque question dans le chat du carnet, relever la réponse et les citations. Lire le schéma exact sur `/docs`.

## Lancement

Coller dans Claude Code, à la racine du dépôt (les limites peuvent être ajustées) :

```text
/goal Exécuter kit/PROMPT.md pour la fiche kit/fiches/01-open-notebook.md, en autonomie complète, sans jamais attendre de réponse. J'autorise explicitement, pour cette mission : docker pull, docker compose et docker run des images officielles citées dans la fiche et dans kit/PROMPT.md ; lecture seule des modèles déjà présents sur la machine ; le démarrage du service de modèles commun LLM-Service (~/Projets/Projet-IA/LLM-Service, outils/communs/llm_service.sh) et l'ajout de modèles dedans par ollama pull, sans modifier ses fichiers suivis par git ; téléchargement de modèles seulement s'ils manquent, dans la limite de 30 Go ; un téléchargement total (images et modèles) de 100 Go au plus ; la création d'environnements Python dans .venv du dépôt et l'installation de paquets PyPI dedans ; la création de comptes locaux fictifs dans l'outil testé ; git add et git commit locaux. Interdit : sudo, sysctl, pkill -f, git push, port publié hors de 127.0.0.1, compte en ligne, dépense, curl | bash, docker prune, suppression hors du dépôt et des ressources Docker préfixées rag-. Objectif atteint quand, preuves affichées dans la conversation : RAPPORT-open-notebook.md existe et couvre les rubriques de la phase H ; python3 outils/communs/verifier_docs.py affiche 0 point ; exemples/open-notebook/sorties_verifiees.txt couvre chaque exemple ; un fichier outils/resultats/open-notebook/banc-*.json existe ; curl sur http://127.0.0.1:8502 répond ; docker ps montre chaque port lié à 127.0.0.1 ; README.md, LICENSE, docs/open-notebook/presentation.md (avec les configurations minimales sans et avec GPU) et les fichiers outils/resultats/open-notebook/versions-*.json existent ; git status est propre après le commit final. Sinon, arrêt après 300 tours avec JOURNAL.md et RAPPORT-open-notebook.md à jour.
```
