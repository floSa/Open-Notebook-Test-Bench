# Fiche 06. SurfSense

| Champ | Valeur |
|---|---|
| Identifiant `<solution>` | `surfsense` |
| Dépôt | https://github.com/MODSetter/SurfSense |
| Documentation | https://www.surfsense.com/docs/ |
| Licence | Apache-2.0, sauf `surfsense_backend/app/proprietary/` sous Business Source License 1.1 |
| Version à décrire | Dernière release taguée (voir `VERSION` et les releases) ; images figées par empreinte. |
| Public | Utilisateur technique à l'aise avec un terminal, pas forcément développeur |
| Interface | Port 3000 par défaut (interface web), backend 8000 : republier sur `127.0.0.1`, en choisissant des ports libres si d'autres solutions de la série les occupent |
| API | API REST et serveur MCP (`surfsense_mcp`) |
| Services | Interface Next.js, backend FastAPI, PostgreSQL avec pgvector, autres selon le compose |
| Besoins indicatifs | Moyen, hors modèles |

## Particularités connues

Relevé du 7 novembre 2026, à revérifier au cadrage.

- Le projet s'est réorienté en 2026 vers la collecte de données web pour agents (connecteurs Reddit, YouTube, Google…). Le volet NotebookLM (base de connaissances, chat cité, rapports, podcasts) reste annoncé comme maintenu. **Périmètre : le volet NotebookLM.** Les connecteurs de collecte web sont hors périmètre (ils interrogent des sites tiers), sauf le crawl d'une page locale de test.
- Le script d'installation officiel s'appuie sur `curl … | bash` et installe Watchtower (mises à jour automatiques) : **ne pas l'utiliser**. Installer par Docker Compose depuis le dépôt au tag figé, sans Watchtower ; relire le script pour documenter ce qu'il fait.
- Le projet se déclare « pas encore prêt pour la production » : chaque échec est consigné tel quel.
- Licence mixte : expliquer dans le manuel d'exploitation ce qui relève de la BSL 1.1.
- ETL des documents : Docling (local) ; Unstructured et LlamaCloud demandent des clés d'API, hors périmètre.
- LLM via LiteLLM ou la spécification OpenAI ; podcasts et vidéos demandent un fournisseur TTS : tester un serveur TTS local compatible OpenAI (par exemple Kokoro-FastAPI, relu avant installation), sinon marquer [À tester].
- Fonctions à couvrir : espaces de recherche, base de connaissances (formats, synchronisation d'un dossier local), recherche hybride et index hiérarchiques, chat cité, rapports et présentations, podcasts, rôles et collaboration en temps réel, API, serveur MCP local.

## Branchement au socle

- Joindre les services au réseau `rag-local`.
- Chat : `http://rag-vllm-chat:8000/v1`. Embedding : `http://rag-vllm-embed:8001/v1`. Reranker, s'il existe : `http://rag-vllm-rerank:8002`.
- Via LiteLLM, préfixe de modèle compatible OpenAI ou vLLM (à vérifier dans la doc de la version).
- Régler découpage, top-k et historique pour rester dans le budget de contexte du socle.
- Repli seulement si vLLM échoue : Ollama, `http://rag-ollama:11434`.

## Thèmes des manuels 03 et suivants

1. Espaces et base de connaissances : formats, ETL Docling, dossier local synchronisé.
2. Recherche et chat cité : hybride, rerankers, qualité mesurée.
3. Livrables : rapports, présentations.
4. Podcasts avec un TTS local.
5. Équipe : rôles, chat partagé, commentaires.
6. API REST et serveur MCP local.

## Hors périmètre

Connecteurs de collecte web vers des sites tiers, connecteurs OAuth (Notion, Slack, Jira, Drive), offre cloud et facturation, application desktop Windows et extension navigateur (citées en [Source]).

## Adaptateur du banc

Via l'API REST : créer un espace « Banc », téléverser le corpus, attendre l'indexation, poser chaque question, relever la réponse et les citations.

## Lancement

Coller dans Claude Code, à la racine du dépôt :

```text
/goal Exécuter kit/PROMPT.md pour la fiche kit/fiches/06-surfsense.md, en autonomie complète, sans jamais attendre de réponse. J'autorise explicitement, pour cette mission : git clone du dépôt officiel de SurfSense ; docker pull, docker compose et docker run des images officielles citées dans la fiche et dans kit/PROMPT.md ; lecture seule des modèles déjà présents sur la machine, dans les dossiers usuels et dans MODELES_EXISTANTS=<chemin facultatif> ; téléchargement de modèles Hugging Face seulement s'ils manquent, dans la limite de 30 Go ; un téléchargement total (images et modèles) de 120 Go au plus ; la création d'environnements Python dans .venv du dépôt et l'installation de paquets PyPI ou npm dans le dépôt ; la création de comptes locaux fictifs dans l'outil testé ; git add et git commit locaux. Interdit : sudo, git push, port publié hors de 127.0.0.1, compte en ligne, dépense, curl | bash, Watchtower, docker prune, suppression hors du dépôt et des ressources Docker préfixées rag-. Objectif atteint quand, preuves affichées dans la conversation : RAPPORT-surfsense.md existe et couvre les rubriques de la phase H ; python3 outils/communs/verifier_docs.py affiche 0 point ; exemples/surfsense/sorties_verifiees.txt couvre chaque exemple ; un fichier outils/resultats/surfsense/banc-*.json existe ; curl sur l'URL locale de SurfSense répond ; git status est propre après le commit final. Sinon, arrêt après 300 tours avec JOURNAL.md et RAPPORT-surfsense.md à jour.
```
