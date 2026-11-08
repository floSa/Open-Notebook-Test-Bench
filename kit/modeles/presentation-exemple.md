# Open Notebook en bref

Version 1.15.1, essayée le 8 novembre 2026 sur Windows 11 (WSL2), avec des modèles d'IA installés sur la machine.

## Sommaire

1. [Ce que c'est](#1-ce-que-cest)
2. [Pour qui](#2-pour-qui)
3. [Le projet](#3-le-projet)
4. [Fonctions](#4-fonctions)
5. [Matériel nécessaire](#5-matériel-nécessaire)
6. [Résultats mesurés](#6-résultats-mesurés)
7. [Pour aller plus loin](#7-pour-aller-plus-loin)

## 1. Ce que c'est

Open Notebook est une application web qui permet de poser des questions à ses propres documents et d'obtenir des réponses qui indiquent de quel document vient chaque information.

Le travail s'organise en **carnets**. Un carnet réunit :

- des **sources** : fichiers PDF, Word, Excel, PowerPoint, pages web, enregistrements audio ;
- une **conversation** : une question en langage courant, une réponse rédigée à partir des sources, avec un renvoi cliquable vers le document utilisé ;
- des **notes** : réponses conservées, résumés, notes libres.

À partir d'un carnet, l'application peut aussi produire des résumés ou des extractions selon une consigne réutilisable, et un **podcast** : un dialogue audio entre deux voix qui présente le contenu des documents.

L'application s'installe sur un poste ou un serveur. Elle peut fonctionner sans aucun service en ligne : les modèles d'IA tournent alors sur la même machine, et les documents ne quittent pas le poste.

## 2. Pour qui

| Adapté | Peu adapté |
|---|---|
| Une personne qui travaille sur un dossier de quelques dizaines de documents et veut des réponses vérifiables | Une équipe : il n'existe qu'un mot de passe commun, sans comptes ni droits séparés |
| Des documents confidentiels qui ne doivent pas partir vers un service en ligne | Des documents scannés : l'application ne les lit pas en l'état |
| Des documents texte, des tableaux, des réunions enregistrées | Une recherche dans des centaines de documents à la fois : la conversation transmet au modèle les documents choisis en entier, ce qui limite leur nombre |

## 3. Le projet

| | |
|---|---|
| Dépôt | https://github.com/lfnovo/open-notebook |
| Site | https://www.open-notebook.ai |
| Licence | MIT : libre, usage commercial autorisé |
| Popularité | 41 764 étoiles, 4 798 forks sur GitHub |
| Activité | très active : 114 modifications sur les 90 derniers jours, 98 contributeurs, une nouvelle version par mois environ |
| Ancienneté | projet créé en octobre 2024 ; versions 1.x stables |
| Coût | gratuit ; aucun abonnement |

Chiffres relevés sur GitHub le 8 novembre 2026.

## 4. Fonctions

Réponses : **Oui**, **Non**, ou **Partiel** avec la limite en une phrase.

### Modèles d'IA

| Fonction | Réponse |
|---|---|
| Modèles installés sur la machine avec Ollama | Oui |
| Modèles installés sur la machine avec vLLM, LM Studio ou tout serveur compatible OpenAI | Oui |
| Services en ligne (OpenAI, Anthropic, Mistral, Google…) | Oui, une vingtaine |
| Calcul des embeddings sur la machine (représentation numérique du sens d'un passage, qui sert à la recherche par le sens) | Oui |
| Reranking (second tri des passages trouvés, par un modèle spécialisé, pour garder les plus pertinents) | Non |
| Voix (lecture et transcription) sur la machine | Oui, avec un serveur de voix séparé |

### Documents acceptés

| Fonction | Réponse |
|---|---|
| PDF, Word, Excel, PowerPoint, OpenDocument, EPUB, texte, Markdown, HTML | Oui |
| Tableaux | Oui, avec le module Docling activé ; sans lui, les tableaux Word sont perdus |
| Documents scannés (OCR) | Non : le module prévu ne fonctionne pas dans la version 1.15.1 |
| Pages web à partir d'une adresse | Oui |
| Audio (MP3, WAV, M4A) | Oui, transcrit automatiquement |
| Vidéo et liens YouTube | Oui, transcrits |
| Connexion à Google Drive, SharePoint, Notion, Slack | Non : les documents s'ajoutent un par un |

### Recherche et réponses

| Fonction | Réponse |
|---|---|
| Conversation sur les documents d'un carnet | Oui : les documents cochés sont transmis en entier au modèle |
| Recherche par mots | Oui |
| Recherche par le sens | Oui |
| Recherche combinant mots et sens | Non |
| Question posée à tous les carnets à la fois | Oui (« Demander »), mais trop lent sans carte graphique |
| Indication de la source dans la réponse | Oui, document par document, avec ouverture au clic |
| Indication de la page ou surlignage du passage | Non |
| Refus de répondre quand l'information n'est pas dans les documents | Oui |

### Production

| Fonction | Réponse |
|---|---|
| Notes | Oui |
| Résumés et extractions à partir d'une consigne réutilisable | Oui |
| Podcast | Oui, de 1 à 4 voix ; une seule voix française disponible avec le serveur de voix utilisé |
| Rapports, diapositives | Non |

### Installation et exploitation

| Fonction | Réponse |
|---|---|
| Installation | Docker, deux conteneurs : l'application et sa base de données |
| Mémoire nécessaire, hors modèles d'IA | 1 Go ; 4 Go avec le module Docling |
| Interface en français | Oui |
| Plusieurs utilisateurs avec leurs propres comptes | Non |
| API pour automatiser | Oui, complète |
| Connexion à un assistant IA par MCP | Partiel : serveur MCP externe au projet, une fonction en échec |
| Fonctionnement hors ligne | Oui, sauf une vérification de version auprès de GitHub, impossible à couper |
| Envoi de statistiques d'usage | Non |
| Sauvegarde et restauration | Oui, par copie des dossiers de données |

## 5. Matériel nécessaire

### Sans carte graphique : configuration minimale, mesurée

| Élément | Minimum |
|---|---|
| Processeur | 8 cœurs récents (instructions AVX2) |
| Mémoire vive | 16 Go |
| Disque libre | 20 Go : application 2,5 Go, module Docling 6 Go, modèles 4 Go, voix 1,3 Go, images Docker |
| Modèle de réponse | qwen3:4b-instruct : 4 milliards de paramètres, 2,5 Go |
| Modèle d'embedding | bge-m3 : 1,2 Go, multilingue |
| Taille de contexte | 16 384 jetons |

Mémoire utilisée : 5,5 Go pour les modèles, 1 Go pour l'application (4 Go avec Docling), 0,5 à 2,4 Go pour la voix. Le total reste sous 12 Go, ce qui laisse de la marge sur 16 Go.

**Combien de documents par conversation.** La conversation transmet au modèle tous les documents cochés, en entier. Sans carte graphique, c'est leur volume qui fixe le temps d'attente de la première question :

| Volume coché | Équivalent | Première question | Questions suivantes |
|---|---|---|---|
| 12 000 caractères | 5 pages de texte | 1 min 30 | 10 à 25 s |
| 28 000 caractères | 10 pages | 5 min | 10 à 25 s |
| 45 000 caractères | 15 pages, la limite d'un contexte de 16 384 jetons | 6 à 10 min (estimé) | 10 à 25 s |

Au-delà, la question échoue avec un message d'erreur. Un carnet peut contenir beaucoup plus de documents : seuls ceux cochés en « Contenu complet » comptent.

**Modèles plus légers.** ministral-3:3b donne autant de bonnes réponses que qwen3:4b-instruct, mais met deux fois plus de temps sur les réponses longues. Les modèles de moins de 3 milliards de paramètres n'ont pas été essayés.

### Avec une carte graphique NVIDIA : configuration minimale, estimée

| Élément | Minimum |
|---|---|
| Carte graphique | 8 Go de mémoire |
| Modèle de réponse | le même modèle de 4 milliards de paramètres, en version 4 bits pour vLLM |
| Taille de contexte | 32 768 jetons |
| Effet attendu | première question en quelques secondes au lieu de plusieurs minutes ; deux fois plus de pages par conversation ; mode « Demander » utilisable |

Cette configuration n'a pas encore été mesurée.

## 6. Résultats mesurés

Test sur 38 questions dont la réponse est connue, posées à 9 documents d'une entreprise fictive. Modèle qwen3:4b-instruct, sur un ordinateur portable sans carte graphique dédiée.

| Mesure | Résultat |
|---|---|
| Réponses justes | 28 sur 34 ; les 6 erreurs portent sur le document scanné, illisible |
| Questions sans réponse dans les documents | 4 refus sur 4, aucune réponse inventée |
| Temps de réponse | 9 secondes en général ; environ 1 minute 30 pour la première question d'une conversation, le temps que le modèle lise les documents |
| Ajout des 9 documents | 2 minutes |
| Podcast de 77 secondes | généré en 5 minutes |

Détail : [Qualité et performances](10-qualite-performances.md).

## 7. Pour aller plus loin

| Pour | Lire |
|---|---|
| Installer | [01. Installation](01-installation.md) |
| Premier carnet, première réponse | [02. Prise en main](02-prise-en-main.md) |
| Trois cas d'usage complets | [09. Recettes](09-recettes.md) |
| Limites connues et questions en suspens | [index, « Ce qui reste ouvert »](README.md#ce-qui-reste-ouvert) |

Les réponses de cette page viennent des essais du 8 novembre 2026 et du code source de la version 1.15.1 : [relevé GitHub](../../outils/resultats/open-notebook/identite-github-2026-11-08.json), [analyse du code](../../outils/resultats/open-notebook/cadrage-source.md), [résultats des essais](../../outils/resultats/open-notebook/).
