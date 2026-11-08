# Fiche 04. AnythingLLM

| Champ | Valeur |
|---|---|
| Identifiant `<solution>` | `anythingllm` |
| Dépôt | https://github.com/Mintplex-Labs/anything-llm |
| Documentation | https://docs.anythingllm.com · Docker : `docker/HOW_TO_USE_DOCKER.md` du dépôt |
| Licence | MIT |
| Version à décrire | Dernière release ; image `mintplexlabs/anythingllm` au tag de version (pas `latest`), empreinte notée. |
| Public | Utilisateur technique à l'aise avec un terminal, pas forcément développeur |
| Interface | `http://127.0.0.1:3001` |
| API | API développeur (clé créée dans l'interface), documentation Swagger servie par l'instance |
| Services | Un conteneur (serveur, collecteur, base vectorielle LanceDB intégrée) |
| Besoins indicatifs | Très léger, hors modèles |

## Particularités connues

Relevé du 7 novembre 2026, à revérifier au cadrage.

- Deux éditions : application desktop (Windows, Mac, Linux, mono-utilisateur) et Docker (multi-utilisateur). La session tourne dans WSL et ne pilote pas d'application Windows : **décrire l'édition Docker** et citer l'application desktop en [Source], avec ses différences documentées.
- Télémétrie anonyme activée par défaut : la couper (`DISABLE_TELEMETRY=true`) et le vérifier (journaux, paramètre Privacy). Même télémétrie coupée, des connexions sortantes restent possibles (CDN de modèles, GitHub) : les observer et les documenter.
- Embedder natif sur CPU par défaut (all-MiniLM-L6-v2, surtout anglais) : comparer avec l'embedding multilingue du socle sur le corpus français.
- Un moteur llama.cpp est intégré ; ici, utiliser LLM-Service et citer le moteur intégré en [Source], ou le tester s'il marche sans GPU supplémentaire.
- Fonctions à couvrir : workspaces cloisonnés, modes chat et query, citations, connecteurs de données (GitHub public, YouTube, sites web), agents et agent flows no-code, compatibilité MCP, mémoires, tâches planifiées, routage de modèles, multi-utilisateur et permissions, widget de chat intégrable, API développeur, voix (TTS et STT du navigateur ou Piper).

## Branchement à LLM-Service

- Réseau externe `llm-net` (modèles) ; `rag-local` pour la voix. Aucun serveur de modèles dans la pile de la solution.
- Sans GPU (`service-ollama`) : `http://ollama-central:11434` (fournisseur Ollama) ou `http://ollama-central:11434/v1` (compatible OpenAI), modèles qwen3:4b-instruct et bge-m3, contexte 16 384 jetons. Avec GPU (`service-vllm`) : `http://vllm-central:8000/v1` (chat), `http://vllm-embed:8000/v1` (embedding). Voir `kit/PROMPT.md`, phase B.
- LLM : « Generic OpenAI ». Embedder : « Generic OpenAI » compatible.
- Régler découpage, top-k et historique pour rester dans 16 384 jetons de contexte.
- Reranker : Ollama n'en sert pas ; reranker intégré à la solution s'il existe, sinon [À tester].

## Thèmes des manuels 03 et suivants

1. Workspaces et documents : import, épinglage, modes chat et query, réglages de similarité.
2. Citations et qualité : embedder natif contre `bge-m3`, effet mesuré.
3. Connecteurs de données : site web local de test, dépôt GitHub public, YouTube si accessible sans compte.
4. Agents : compétences intégrées, agent flows, outils MCP (un serveur MCP local relu avant installation).
5. Mémoires, tâches planifiées et routage de modèles.
6. Multi-utilisateur, rôles et widget intégrable.
7. API développeur.

## Hors périmètre

Fournisseurs cloud payants (en [Source]), déploiements AWS, GCP et autres, application mobile Android.

## Adaptateur du banc

Via l'API développeur : créer un workspace « Banc », téléverser et intégrer le corpus, interroger en mode query, relever la réponse et les sources renvoyées.

## Lancement

Coller dans Claude Code, à la racine du dépôt :

```text
/goal Exécuter kit/PROMPT.md pour la fiche kit/fiches/04-anythingllm.md, en autonomie complète, sans jamais attendre de réponse. J'autorise explicitement, pour cette mission : docker pull, docker compose et docker run des images officielles citées dans la fiche et dans kit/PROMPT.md ; lecture seule des modèles déjà présents sur la machine ; le démarrage du service de modèles commun LLM-Service (~/Projets/Projet-IA/LLM-Service, outils/communs/llm_service.sh) et l'ajout de modèles dedans par ollama pull, sans modifier ses fichiers suivis par git ; téléchargement de modèles seulement s'ils manquent, dans la limite de 30 Go ; un téléchargement total (images et modèles) de 100 Go au plus ; la création d'environnements Python dans .venv du dépôt et l'installation de paquets PyPI ou npm dans le dépôt ; la création de comptes locaux fictifs dans l'outil testé ; git add et git commit locaux. Interdit : sudo, sysctl, pkill -f, git push, port publié hors de 127.0.0.1, compte en ligne, dépense, curl | bash, docker prune, suppression hors du dépôt et des ressources Docker préfixées rag-. Objectif atteint quand, preuves affichées dans la conversation : RAPPORT-anythingllm.md existe et couvre les rubriques de la phase H ; python3 outils/communs/verifier_docs.py affiche 0 point ; exemples/anythingllm/sorties_verifiees.txt couvre chaque exemple ; un fichier outils/resultats/anythingllm/banc-*.json existe ; curl sur http://127.0.0.1:3001 répond ; docker ps montre chaque port lié à 127.0.0.1 ; README.md, LICENSE, docs/anythingllm/presentation.md (avec les configurations minimales sans et avec GPU) et les fichiers outils/resultats/anythingllm/versions-*.json existent ; git status est propre après le commit final. Sinon, arrêt après 300 tours avec JOURNAL.md et RAPPORT-anythingllm.md à jour.
```
