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
- Un moteur llama.cpp est intégré ; ici, utiliser le socle vLLM et citer le moteur intégré en [Source], ou le tester s'il marche sans GPU supplémentaire.
- Fonctions à couvrir : workspaces cloisonnés, modes chat et query, citations, connecteurs de données (GitHub public, YouTube, sites web), agents et agent flows no-code, compatibilité MCP, mémoires, tâches planifiées, routage de modèles, multi-utilisateur et permissions, widget de chat intégrable, API développeur, voix (TTS et STT du navigateur ou Piper).

## Branchement au socle

- Joindre les services au réseau `rag-local`.
- Chat : `http://rag-vllm-chat:8000/v1`. Embedding : `http://rag-vllm-embed:8001/v1`. Reranker, s'il existe : `http://rag-vllm-rerank:8002`.
- LLM : « Generic OpenAI ». Embedder : « Generic OpenAI » compatible.
- Régler découpage, top-k et historique pour rester dans le budget de contexte du socle.
- Repli seulement si vLLM échoue : Ollama, `http://rag-ollama:11434`.

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
/goal Exécuter kit/PROMPT.md pour la fiche kit/fiches/04-anythingllm.md, en autonomie complète, sans jamais attendre de réponse. J'autorise explicitement, pour cette mission : docker pull, docker compose et docker run des images officielles citées dans la fiche et dans kit/PROMPT.md ; lecture seule des modèles déjà présents sur la machine, dans les dossiers usuels et dans MODELES_EXISTANTS=<chemin facultatif> ; téléchargement de modèles Hugging Face seulement s'ils manquent, dans la limite de 30 Go ; un téléchargement total (images et modèles) de 100 Go au plus ; la création d'environnements Python dans .venv du dépôt et l'installation de paquets PyPI ou npm dans le dépôt ; la création de comptes locaux fictifs dans l'outil testé ; git add et git commit locaux. Interdit : sudo, git push, port publié hors de 127.0.0.1, compte en ligne, dépense, curl | bash, docker prune, suppression hors du dépôt et des ressources Docker préfixées rag-. Objectif atteint quand, preuves affichées dans la conversation : RAPPORT-anythingllm.md existe et couvre les rubriques de la phase H ; python3 outils/communs/verifier_docs.py affiche 0 point ; exemples/anythingllm/sorties_verifiees.txt couvre chaque exemple ; un fichier outils/resultats/anythingllm/banc-*.json existe ; curl sur http://127.0.0.1:3001 répond ; git status est propre après le commit final. Sinon, arrêt après 300 tours avec JOURNAL.md et RAPPORT-anythingllm.md à jour.
```
