# Plan des manuels — Open Notebook

Version décrite : Open Notebook 1.15.1, Ollama 0.40.15 sur CPU (machine sans GPU NVIDIA).

## En une phrase par manuel

| N° | Manuel | En une phrase |
|---|---|---|
| - | [Open Notebook en bref](presentation.md) | Ce que fait la solution, pour qui, le projet, les fonctions (oui ou non), les résultats mesurés. |
| 00 | [Notions fondamentales](00-notions-fondamentales.md) | Ce qu'est le RAG et comment Open Notebook l'applique, avec le schéma des services et des ports. |
| 01 | [Installation sous Windows et WSL2](01-installation.md) | Installer, brancher au socle Ollama, mesurer la mémoire, mettre à jour et tout désinstaller. |
| 02 | [Prise en main](02-prise-en-main.md) | Du premier carnet à la première réponse citée. |
| 03 | [Carnets, sources et formats](03-carnets-sources-formats.md) | Ce qui est extrait de chaque format, et ce qui ne l'est pas (scan, tableaux, audio). |
| 04 | [Chat et citations](04-chat-et-citations.md) | Choisir le contexte source par source, lire les citations, limites mesurées. |
| 05 | [Notes et transformations](05-notes-et-transformations.md) | Notes manuelles, transformations intégrées et personnalisées. |
| 06 | [Recherche](06-recherche.md) | Recherche plein texte, recherche vectorielle et « Ask », différences mesurées. |
| 07 | [Podcasts](07-podcasts.md) | Profils d'épisode et de locuteur, serveur de voix local, résultat en français. |
| 08 | [API REST et MCP](08-api-et-mcp.md) | Automatiser l'ingestion et les questions ; brancher un client MCP. |
| 09 | [Recettes](09-recettes.md) | Cas d'usage complets, de bout en bout. |
| 10 | [Qualité et performances](10-qualite-performances.md) | Résultats du banc, réglages qui changent le résultat, profils matériels, contexte. |
| 11 | [Exploitation](11-exploitation.md) | Sauvegarde, restauration, mise à jour, journaux, sécurité, accès. |
| 12 | [Dépannage et FAQ](12-depannage.md) | Les échecs réellement rencontrés et leur solution. |

## Contenu détaillé

- **00** : RAG, embeddings, découpage, recherche hybride, reranking, citations ; particularité d'Open Notebook (chat à contexte choisi, sans recherche top-k) ; schéma des services (interface, API, worker, SurrealDB, Ollama) et des ports.
- **01** : prérequis mesurés ; pourquoi Ollama sur CPU ici ; mémoire de l'application seule au repos et pendant une indexation ; script d'installation ; ports limités à 127.0.0.1 ; premier démarrage ; branchement des modèles ; mise à jour ; désinstallation complète.
- **02** : se connecter avec le mot de passe ; créer un carnet ; ajouter une source ; poser une question ; lire la citation.
- **03** : formats essayés sur le corpus Vélanor (PDF texte, PDF scanné, DOCX, PPTX, XLSX, HTML, Markdown, anglais, audio) ; texte extrait, tableaux, OCR avec Docling ; découpage.
- **04** : modes de contexte (« not in », « insights », « full content ») ; jetons envoyés ; format des citations ; modèles de raisonnement ; troncature silencieuse au-delà de `num_ctx`.
- **05** : notes manuelles et notes issues du chat ; transformations fournies ; transformation personnalisée en français.
- **06** : recherche plein texte et vectorielle sur les mêmes requêtes ; « Ask » ; scores et seuil.
- **07** : serveur de voix local compatible OpenAI ; profils de locuteur et d'épisode ; durée, voix, langue.
- **08** : authentification ; scripts d'exemple (créer un carnet, ajouter un fichier, poser une question) ; serveur MCP tiers.
- **09** : analyser un rapport annuel ; comparer un contrat et un audit ; préparer une note de synthèse.
- **10** : banc de 36 questions ; réglages par défaut puis réglages recommandés ; second modèle ; profils A (mesuré) et B ([Estimation]).
- **11** : sauvegarde et restauration des dossiers de données ; mise à jour de version ; journaux ; sécurité ; mono-utilisateur.
- **12** : tableau Symptôme | Cause probable | Action, tiré des journaux d'essai.

Les écarts au plan constatés pendant la rédaction sont notés dans [l'index de la solution](README.md#ce-qui-reste-ouvert).
