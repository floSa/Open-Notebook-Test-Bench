# Fiche 05. Open WebUI

| Champ | Valeur |
|---|---|
| Identifiant `<solution>` | `open-webui` |
| Dépôt | https://github.com/open-webui/open-webui |
| Documentation | https://docs.openwebui.com/ |
| Licence | Open WebUI License : BSD-3 avec clause de marque (voir `LICENSE` et `LICENSE_HISTORY` du dépôt) |
| Version à décrire | Dernière release ; image `ghcr.io/open-webui/open-webui` au tag de version (pas `main`), empreinte notée. |
| Public | Utilisateur technique à l'aise avec un terminal, pas forcément développeur |
| Interface | `http://127.0.0.1:3000` (port interne 8080) |
| API | API de l'instance (clés créées dans Settings, Account) |
| Services | Un conteneur ; services annexes optionnels : extraction (Docling Serve ou Tika), recherche web (SearXNG) |
| Besoins indicatifs | Léger, hors modèles et services annexes |

## Particularités connues

Relevé du 7 novembre 2026, à revérifier au cadrage.

- Prendre l'image standard, pas les variantes `:ollama` ni `:cuda` : les modèles viennent du socle vLLM. Le volume de données est obligatoire (`/app/backend/data`), sinon tout est perdu au redémarrage.
- Le premier compte créé devient administrateur.
- La licence impose de garder la marque « Open WebUI » ; la marque blanche au-delà de 50 utilisateurs est réservée à l'offre Enterprise. À expliquer dans le manuel d'exploitation.
- RAG : 9 bases vectorielles possibles (Chroma par défaut), moteurs d'extraction (Tika, Docling, Mistral OCR, PaddleOCR-vl, Document Intelligence), recherche hybride BM25 et vecteurs avec reranking, mode « contexte complet ». Bases Knowledge appelées avec `#` dans le chat ; URL avec `#` suivi de l'URL.
- Extraction locale : tester Docling via son serveur officiel (image `docling-serve`, relue avant installation), sinon Tika. Mistral OCR et Document Intelligence sont hors périmètre (API payantes).
- Recherche web : SearXNG en conteneur local relu avant installation, ou hors périmètre si trop lourd. Ne rien exposer hors de `127.0.0.1`.
- Mode hors ligne : `HF_HUB_OFFLINE=1` une fois les modèles d'embedding téléchargés ; vérifier l'effet.
- Fonctions à couvrir : connexions OpenAI-compatibles (et Ollama en [Source]), Knowledge, modèles personnalisés liés à une base, notes, mémoire, outils et MCP, fonctions (filtres, pipes), RBAC et groupes, voix (Whisper local), canaux, automatisations, API.

## Branchement au socle

- Joindre les services au réseau `rag-local`.
- Chat : `http://rag-vllm-chat:8000/v1`. Embedding : `http://rag-vllm-embed:8001/v1`. Reranker, s'il existe : `http://rag-vllm-rerank:8002`.
- Chat : connexion OpenAI. Embeddings : moteur « OpenAI » avec l'URL d'embedding. API Ollama désactivée sauf repli.
- Régler découpage, top-k et historique pour rester dans le budget de contexte du socle.
- Repli seulement si vLLM échoue : Ollama, `http://rag-ollama:11434`.

## Thèmes des manuels 03 et suivants

1. Connexions aux modèles : OpenAI-compatible vers vLLM, plusieurs modèles dans une même conversation.
2. Knowledge et RAG : création, import, `#` dans le chat, modèle personnalisé lié à une base.
3. Réglages documentaires : moteur d'extraction, découpage, hybride, reranking, contexte complet ; effet mesuré au banc.
4. Notes et mémoire.
5. Outils, fonctions et MCP : un outil local relu, un serveur MCP local.
6. Voix : transcription Whisper locale, synthèse vocale locale.
7. Utilisateurs, groupes, permissions.
8. API de l'instance.

## Hors périmètre

Offre Enterprise, SSO, LDAP et SCIM (en [Source]), stockage cloud (S3, GCS, Azure), génération d'images.

## Adaptateur du banc

Via l'API : créer une base Knowledge « Banc », téléverser le corpus, poser chaque question avec la base attachée, relever la réponse et les sources renvoyées.

## Lancement

Coller dans Claude Code, à la racine du dépôt :

```text
/goal Exécuter kit/PROMPT.md pour la fiche kit/fiches/05-open-webui.md, en autonomie complète, sans jamais attendre de réponse. J'autorise explicitement, pour cette mission : docker pull, docker compose et docker run des images officielles citées dans la fiche et dans kit/PROMPT.md, y compris docling-serve, Tika et SearXNG après relecture ; lecture seule des modèles déjà présents sur la machine, dans les dossiers usuels et dans MODELES_EXISTANTS=<chemin facultatif> ; téléchargement de modèles Hugging Face seulement s'ils manquent, dans la limite de 30 Go ; un téléchargement total (images et modèles) de 120 Go au plus ; la création d'environnements Python dans .venv du dépôt et l'installation de paquets PyPI dedans ; la création de comptes locaux fictifs dans l'outil testé ; git add et git commit locaux. Interdit : sudo, git push, port publié hors de 127.0.0.1, compte en ligne, dépense, curl | bash, docker prune, suppression hors du dépôt et des ressources Docker préfixées rag-. Objectif atteint quand, preuves affichées dans la conversation : RAPPORT-open-webui.md existe et couvre les rubriques de la phase H ; python3 outils/communs/verifier_docs.py affiche 0 point ; exemples/open-webui/sorties_verifiees.txt couvre chaque exemple ; un fichier outils/resultats/open-webui/banc-*.json existe ; curl sur http://127.0.0.1:3000 répond ; git status est propre après le commit final. Sinon, arrêt après 300 tours avec JOURNAL.md et RAPPORT-open-webui.md à jour.
```
