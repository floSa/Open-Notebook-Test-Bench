# Fiche 03. Kotaemon

| Champ | Valeur |
|---|---|
| Identifiant `<solution>` | `kotaemon` |
| Dépôt | https://github.com/Cinnamon/kotaemon |
| Documentation | https://cinnamon.github.io/kotaemon/ · modèles locaux : `docs/local_model.md` du dépôt |
| Licence | Apache-2.0 |
| Version à décrire | Dernière release (v0.12.0 au 7 novembre 2026). Image `ghcr.io/cinnamon/kotaemon` au tag correspondant si disponible, sinon empreinte exacte de `main-full`. |
| Public | Utilisateur technique à l'aise avec un terminal, pas forcément développeur |
| Interface | `http://127.0.0.1:7860` (Gradio) |
| API | Pas d'API REST documentée ; bibliothèque Python `kotaemon` pour construire des pipelines |
| Services | Un conteneur ; magasins de documents et de vecteurs configurables (LanceDB, Chroma par défaut selon la version) |
| Besoins indicatifs | Léger, hors modèles ; l'image `full` est plus grosse |

## Particularités connues

Relevé du 7 novembre 2026, à revérifier au cadrage.

- Images : `lite`, `full` (formats DOCX et autres via Unstructured) et `ollama` (Ollama inclus). Prendre **`full`** et utiliser LLM-Service, pas l'Ollama de l'image.
- Identifiants par défaut `admin` / `admin` : les changer dès le premier démarrage et le documenter comme risque en tête du manuel d'installation.
- Le fichier `.env` ne sert qu'au premier lancement (il remplit la base) ; les changements suivants se font dans l'interface (Resources, LLMs and Embeddings).
- Lecteurs de documents : Docling et PaddleOCR (locaux), Azure Document Intelligence et Adobe (API payantes, hors périmètre). Réglage dans Settings, Retrieval Settings, File loader.
- GraphRAG : NanoGraphRAG (recommandé par le projet), LightRAG, Microsoft GraphRAG. Les installations peuvent créer des conflits de versions (issue 440 du dépôt) ; consigner ce qui se passe.
- Activité ralentie (327 commits, plus de 200 issues ouvertes) : le noter dans les limites.
- Fonctions à couvrir : collections privées et publiques, citations dans la visionneuse PDF avec surlignage et score de pertinence, alerte de faible pertinence, recherche hybride et reranking, QA multimodale (figures, tableaux), décomposition de questions, agents ReAct et ReWOO, GraphRAG, réglages de l'interface et des prompts, multi-utilisateur.

## Branchement à LLM-Service

- Réseau externe `llm-net` (modèles) ; `rag-local` pour la voix. Aucun serveur de modèles dans la pile de la solution.
- Sans GPU (`service-ollama`) : `http://ollama-central:11434` (fournisseur Ollama) ou `http://ollama-central:11434/v1` (compatible OpenAI), modèles qwen3:4b-instruct et bge-m3, contexte 16 384 jetons. Avec GPU (`service-vllm`) : `http://vllm-central:8000/v1` (chat), `http://vllm-embed:8000/v1` (embedding). Voir `kit/PROMPT.md`, phase B.
- Dans Resources : type OpenAI pour le LLM et pour les embeddings, clé fictive.
- Régler découpage, top-k et historique pour rester dans 16 384 jetons de contexte.
- Reranker : Ollama n'en sert pas ; reranker intégré à la solution s'il existe, sinon [À tester].

## Thèmes des manuels 03 et suivants

1. Collections et indexation : lecteurs de fichiers comparés (par défaut, Docling, PaddleOCR) sur PDF texte, scan et tableaux.
2. Citations vérifiables : lire la visionneuse, le score, l'alerte ; cas où la citation est fausse.
3. Réglages de recherche : hybride, reranking, nombre de passages.
4. Raisonnement : simple, décomposition, ReAct, ReWOO ; qualité et latence comparées.
5. GraphRAG : NanoGraphRAG puis LightRAG ; coût d'indexation et apport mesuré.
6. Utilisateurs et partage.
7. Personnaliser un pipeline avec la bibliothèque Python (un exemple court).

## Hors périmètre

Lecteurs Azure et Adobe, fournisseurs cloud (en [Source] seulement), démo Hugging Face.

## Adaptateur du banc

Pas d'API REST : piloter l'interface Gradio avec Playwright (dans le conteneur du socle), ou appeler les pipelines via la bibliothèque Python dans le conteneur. Indiquer la méthode retenue et ses limites dans le manuel « Qualité et performances ».

## Lancement

Coller dans Claude Code, à la racine du dépôt :

```text
/goal Exécuter kit/PROMPT.md pour la fiche kit/fiches/03-kotaemon.md, en autonomie complète, sans jamais attendre de réponse. J'autorise explicitement, pour cette mission : docker pull, docker compose et docker run des images officielles citées dans la fiche et dans kit/PROMPT.md ; l'installation de nano-graphrag et LightRAG dans le conteneur de Kotaemon ; lecture seule des modèles déjà présents sur la machine ; le démarrage du service de modèles commun LLM-Service (~/Projets/Projet-IA/LLM-Service, outils/communs/llm_service.sh) et l'ajout de modèles dedans par ollama pull, sans modifier ses fichiers suivis par git ; téléchargement de modèles seulement s'ils manquent, dans la limite de 30 Go ; un téléchargement total (images et modèles) de 100 Go au plus ; la création d'environnements Python dans .venv du dépôt et l'installation de paquets PyPI dedans ; la création de comptes locaux fictifs dans l'outil testé ; git add et git commit locaux. Interdit : sudo, sysctl, pkill -f, git push, port publié hors de 127.0.0.1, compte en ligne, dépense, curl | bash, docker prune, suppression hors du dépôt et des ressources Docker préfixées rag-. Objectif atteint quand, preuves affichées dans la conversation : RAPPORT-kotaemon.md existe et couvre les rubriques de la phase H ; python3 outils/communs/verifier_docs.py affiche 0 point ; exemples/kotaemon/sorties_verifiees.txt couvre chaque exemple ; un fichier outils/resultats/kotaemon/banc-*.json existe ; curl sur http://127.0.0.1:7860 répond ; docker ps montre chaque port lié à 127.0.0.1 ; README.md, LICENSE, docs/kotaemon/presentation.md (avec les configurations minimales sans et avec GPU) et les fichiers outils/resultats/kotaemon/versions-*.json existent ; git status est propre après le commit final. Sinon, arrêt après 300 tours avec JOURNAL.md et RAPPORT-kotaemon.md à jour.
```
