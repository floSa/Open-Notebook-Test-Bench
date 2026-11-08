# Open Notebook en bref

> **Objet** : savoir en cinq minutes ce que fait Open Notebook, ce qu'il vaut d'après les essais, et en quoi il diffère des autres alternatives locales à NotebookLM.
> **Version décrite** : Open Notebook 1.15.1 (4 novembre 2026), essayé le 2026-11-08 sur Windows 11 et WSL2, sans GPU NVIDIA (modèles locaux sur CPU avec Ollama).
> **Statut des informations** : [Vérifié] observé ou mesuré pendant les essais ; [Source] lu dans la documentation officielle ou le code source au tag v1.15.1, non essayé ; [Estimation] calcul non mesuré ; [À tester] ni documenté ni essayé.

## Sommaire

1. [En une minute](#1-en-une-minute)
2. [Identité du projet](#2-identité-du-projet)
3. [Ce que fait la solution](#3-ce-que-fait-la-solution)
4. [Grille de comparaison](#4-grille-de-comparaison)
5. [Résultats des essais](#5-résultats-des-essais)
6. [Pour aller plus loin](#6-pour-aller-plus-loin)

## 1. En une minute

Open Notebook reproduit NotebookLM sur sa propre machine : des **carnets** regroupent des documents (PDF, Office, pages web, audio), une conversation répond en citant les documents, des notes et des résumés se rangent à côté, et un **podcast** à plusieurs voix peut être généré à partir du carnet. Tout peut tourner sans service en ligne, avec des modèles locaux.

| | |
|---|---|
| **À choisir si** | une seule personne veut l'expérience NotebookLM complète, podcasts compris, avec ses documents gardés en local |
| **À éviter si** | plusieurs utilisateurs doivent avoir des comptes séparés ; les documents sont surtout des scans ; il faut chercher dans des centaines de documents à la fois (le chat lit les documents choisis en entier, il ne recherche pas les passages) |
| **Point fort constaté** | réponses exactes et citées sur les documents lisibles, refus net quand l'information n'existe pas ; podcast en français généré en 5 minutes sur CPU [Vérifié] |
| **Point faible constaté** | les PDF scannés restent illisibles (OCR inopérant dans l'image officielle 1.15.1) ; pas de recherche hybride ni de reranking ; citation au niveau du document, sans page [Vérifié] |

## 2. Identité du projet

Relevé par l'API publique de GitHub le 2026-11-08 [Vérifié] ([résultat](../../outils/resultats/open-notebook/identite-github-2026-11-08.json), script `outils/communs/identite_github.py`).

| Élément | Valeur |
|---|---|
| Dépôt | https://github.com/lfnovo/open-notebook |
| Site et documentation | https://www.open-notebook.ai ; documentation dans le dépôt, dossier `docs/` |
| Licence | MIT : permissive, usage commercial libre |
| Étoiles, forks | 41 764 étoiles, 4 798 forks |
| Créé le | 21 octobre 2024 |
| Activité | 1 043 commits sur la branche principale, dont 114 sur les 90 derniers jours ; 98 contributeurs ; dernier envoi le 8 novembre 2026 ; 184 tickets et demandes de fusion ouverts |
| Rythme des versions | 1.8.4 (avril 2026) à 1.15.1 (4 novembre 2026) : dix versions en sept mois |
| Maturité | très actif ; versions 1.x stables ; depuis la 1.15.0, pas de retour arrière sans sauvegarde (migration de la base) [Source] |
| Technologies | interface Next.js et React, API Python FastAPI, base SurrealDB, traitements en tâche de fond (worker) [Source] |

## 3. Ce que fait la solution

| Fonction | En pratique | Statut | Manuel |
|---|---|---|---|
| Carnets | trois colonnes : **Sources**, **Notes**, conversation | [Vérifié] | [02](02-prise-en-main.md) |
| Ajout de documents | fichiers, liens web, texte collé ; extraction, découpage, embeddings en tâche de fond | [Vérifié] pour les fichiers | [03](03-carnets-sources-formats.md) |
| Conversation citée | le modèle reçoit les documents choisis en entier et cite chaque information par l'identifiant du document | [Vérifié] | [04](04-chat-et-citations.md) |
| Notes et transformations | notes manuelles, réponse gardée en note, consignes réutilisables (résumé, extraction de chiffres) | [Vérifié] | [05](05-notes-et-transformations.md) |
| Recherche | plein texte et vectorielle sur tous les carnets ; mode **Demander** qui enchaîne plusieurs recherches | [Vérifié] | [06](06-recherche.md) |
| Podcast | épisode de 1 à 4 voix, profils réutilisables | [Vérifié] à deux voix | [07](07-podcasts.md) |
| API et MCP | API REST complète (tout ce que fait l'interface) ; serveur MCP tiers | [Vérifié] | [08](08-api-et-mcp.md) |

## 4. Grille de comparaison

Critères du comparatif des six solutions relevé le 7 novembre 2026 (fourni par l'utilisateur, non vérifié), repris et contrôlés pour Open Notebook. La dernière colonne signale ce que les essais corrigent ou précisent.

### Identité et inférence

| Critère | Open Notebook 1.15.1 | Statut | Par rapport au comparatif du 7 novembre |
|---|---|---|---|
| Ollama | natif : modèles de langage et d'embedding | [Vérifié] | confirmé |
| vLLM | par le fournisseur « OpenAI Compatible » (toutes modalités) | [Source] ; non essayé faute de GPU NVIDIA | confirmé, non essayé |
| Autres moteurs | tout serveur compatible OpenAI ou Anthropic ; oMLX (Apple) ; 20 fournisseurs en ligne (OpenAI, Anthropic, Mistral, Groq…) | [Source] | LM Studio passe par « OpenAI Compatible » |
| Embeddings en local | oui, bge-m3 sur Ollama | [Vérifié] | confirmé |
| Reranking | non : ni reranker ni recherche hybride dans la 1.15.1 | [Source] | « non documenté » devient **non** |
| Voix (synthèse et transcription) en local | oui, par un serveur compatible OpenAI (ici Speaches) ; Ollama n'en fournit pas | [Vérifié] | précisé |

### Sources ingérées

| Critère | Open Notebook 1.15.1 | Statut | Par rapport au comparatif du 7 novembre |
|---|---|---|---|
| Formats de fichiers | PDF, Office (DOC à XLSX), OpenDocument, EPUB, TXT, Markdown, HTML, images, audio, vidéo | [Source] ; 8 formats essayés [Vérifié] | confirmé |
| Tableaux | bien extraits avec Docling (option) ; sans Docling, les tableaux DOCX disparaissent | [Vérifié] | précisé |
| OCR, scans | Docling prévu pour l'OCR, mais inopérant dans l'image officielle (« No OCR engine found ») : un PDF scanné reste illisible | [Vérifié] | « non documenté » devient **non, en l'état** |
| URL et pages web | oui ; moteur simple intégré, Crawl4AI ou services tiers en option | [Source] ; non essayé | confirmé, non essayé |
| Audio | oui, transcrit par le modèle de transcription local | [Vérifié] | confirmé |
| Vidéo, YouTube | oui (transcription ; lien YouTube) | [Source] ; non essayé | confirmé, non essayé |
| Connecteurs externes (Drive, Notion…) | non : fichiers, liens et texte seulement | [Source] | confirmé |

### RAG et citations

| Critère | Open Notebook 1.15.1 | Statut | Par rapport au comparatif du 7 novembre |
|---|---|---|---|
| Type de recherche | conversation : pas de recherche, documents choisis envoyés en entier ; recherche séparée plein texte (BM25) ou vectorielle ; **Demander** : jusqu'à 5 recherches vectorielles de 10 résultats | [Source] et [Vérifié] | précisé : la conversation n'est pas un RAG par passages |
| Affichage des citations | identifiant du document dans la réponse, liste « Références », ouverture du document au clic ; ni page ni passage surligné | [Vérifié] | précisé |
| Stockage vectoriel | SurrealDB (documents, vecteurs, plein texte dans un seul conteneur) | [Vérifié] | confirmé |
| RAG avancé | transformations personnalisées, mode **Demander** multi-recherches, modèles de raisonnement ; pas de graphe de connaissances | [Vérifié] | confirmé |
| Taille de contexte | le total des documents choisis doit tenir dans le contexte du modèle ; au-delà, erreur explicite | [Vérifié] | ajouté |

### Fonctions façon NotebookLM

| Critère | Open Notebook 1.15.1 | Statut | Par rapport au comparatif du 7 novembre |
|---|---|---|---|
| Carnets | oui (Notebooks) | [Vérifié] | confirmé |
| Podcast | 1 à 4 voix, profils d'intervenants et d'épisode ; en français, une seule voix française disponible avec Kokoro | [Vérifié] | précisé |
| Notes et livrables | notes, transformations ; pas de diapositives ni de rapports mis en forme | [Vérifié] | confirmé |

### Déploiement et exploitation

| Critère | Open Notebook 1.15.1 | Statut | Par rapport au comparatif du 7 novembre |
|---|---|---|---|
| Installation | Docker Compose, 2 conteneurs (application, SurrealDB) ; interface sur le port 8502, API sur 5055 | [Vérifié] | confirmé |
| Ressources hors modèles | 1,3 Go de RAM au repos ; 1 Go en pointe sans Docling, 3,8 Go avec ; 6,2 Go de disque pour Docling | [Vérifié] | « léger » sans Docling, moyen avec |
| Interface | Next.js et React ; en français (suit la langue du navigateur) | [Vérifié] | confirmé |
| Multi-utilisateur | non : un seul mot de passe, ni comptes ni rôles | [Source] | confirmé |
| API et MCP | API REST complète [Vérifié] ; serveur MCP tiers `open-notebook-mcp` 0.3.0, en partie défaillant | [Vérifié] | précisé |
| Confidentialité | tout local possible ; clés de fournisseurs chiffrées ; un seul appel sortant, la vérification de version vers GitHub (non désactivable) ; aucune télémétrie trouvée | [Source] | précisé : pas « 100 % » hors ligne |

## 5. Résultats des essais

Banc de 38 questions sur un corpus fictif de 9 documents, modèle qwen3:4b-instruct sur CPU [Vérifié] ([détail](10-qualite-performances.md)) :

| Mesure | Résultat |
|---|---|
| Réponses exactes | 28 sur 34 ; les 6 erreurs portent toutes sur le PDF scanné |
| Questions pièges (réponse absente des documents) | 4 refus corrects sur 4, aucune invention |
| Temps de réponse | 9 s en médiane, 24 s pour les plus lentes ; 80 à 100 s pour la première question d'une conversation |
| Indexation des 9 documents | 2 minutes avec Docling |
| Mode **Demander** | inutilisable sur CPU : 74 à 1 089 s par question |

## 6. Pour aller plus loin

- Installer : [01. Installation](01-installation.md) ; prendre en main : [02. Prise en main](02-prise-en-main.md) ; cas complets : [09. Recettes](09-recettes.md).
- Ce qui reste ouvert (OCR, GPU, mode **Demander**) : [index](README.md#ce-qui-reste-ouvert).
- Sources : [synthèse du code](../../outils/resultats/open-notebook/cadrage-source.md), [relecture de sécurité](../../outils/resultats/open-notebook/relecture.md), [identité GitHub](../../outils/resultats/open-notebook/identite-github-2026-11-08.json).
