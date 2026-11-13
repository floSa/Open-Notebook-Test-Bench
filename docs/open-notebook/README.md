# Open Notebook — manuel utilisateur

Ce manuel apprend à installer et à utiliser Open Notebook 1.15.1, une application qui répond aux questions posées sur ses propres documents en citant ses sources, sur un poste Windows 11 avec WSL2 et des modèles d'IA qui tournent sur la machine. Il s'adresse à un utilisateur à l'aise avec un terminal, sans être forcément développeur. Il se lit dans l'ordre : la partie 1 suffit pour maîtriser l'outil ; la partie 2 évalue le produit et sert à choisir le matériel, automatiser et exploiter.

| Version décrite | Date des essais | Machine d'essai | Langue de l'interface |
|---|---|---|---|
| Open Notebook 1.15.1, SurrealDB 2.7.0 ; modèles du service LLM central : `chat` (Qwen3.5-4B), `embed` (bge-m3), `transcribe` (faster-whisper-small) | 12 novembre 2026 | Ryzen 5 9600X, 32 Go de RAM, RTX 4060 Ti 16 Go, Windows 11 + WSL2 | français |

## Par où commencer

1. [01. Découvrir Open Notebook](manuel/01-decouvrir-open-notebook.md) : savoir si l'outil convient et quelle machine il demande.
2. [02. Installer Open Notebook](manuel/02-installer-open-notebook.md) : l'installer en une commande.
3. [03. Premiers pas](manuel/03-premiers-pas.md) : se connecter et se repérer dans l'écran.
4. [04. Première question en dix minutes](manuel/04-premiere-question.md) : obtenir une première réponse citée.

## Partie 1 — Manuel utilisateur

| N° | Chapitre | Ce qu'on saura faire |
|---|---|---|
| 01 | [Découvrir Open Notebook](manuel/01-decouvrir-open-notebook.md) | dire à quoi sert l'outil, pour qui, ce qu'il demande comme machine (sans et avec carte graphique), et les mots de base |
| 02 | [Installer Open Notebook](manuel/02-installer-open-notebook.md) | installer, démarrer, arrêter et désinstaller l'application sous Windows 11 + WSL2 |
| 03 | [Premiers pas](manuel/03-premiers-pas.md) | se connecter, choisir la langue et le thème, se repérer dans chaque zone de l'écran, déclarer les modèles d'IA |
| 04 | [Première question en dix minutes](manuel/04-premiere-question.md) | créer un carnet, ajouter un document, poser une question et ouvrir la citation |
| 05 | [Ajouter et organiser ses sources](manuel/05-ajouter-et-organiser-les-sources.md) | ajouter des fichiers, des liens et des textes, suivre leur lecture, consulter une source, ranger et supprimer carnets et sources |
| 06 | [Discuter avec ses sources](manuel/06-discuter-avec-les-sources.md) | choisir ce qui est envoyé au modèle, lire les citations, gérer plusieurs conversations, changer de modèle |
| 07 | [Prendre des notes et transformer les sources](manuel/07-notes-et-transformations.md) | écrire et garder des notes, appliquer une transformation, créer sa propre transformation |
| 08 | [Rechercher et demander](manuel/08-rechercher-et-demander.md) | chercher par mots ou par le sens dans tous les carnets, poser une question à tous les carnets |
| 09 | [Créer un podcast](manuel/09-creer-un-podcast.md) | régler les voix et le déroulé, générer un épisode et l'écouter |
| 10 | [Régler l'application](manuel/10-regler-l-application.md) | régler la lecture des documents, les embeddings et les options avancées |
| 11 | [Cas pratiques](manuel/11-cas-pratiques.md) | mener trois cas réels de bout en bout sur un dossier d'entreprise |
| 12 | [En cas de problème](manuel/12-en-cas-de-probleme.md) | reconnaître les erreurs réellement rencontrées, leur cause et leur remède |
| 13 | [Glossaire](manuel/13-glossaire.md) | retrouver le sens des mots de l'interface |

## Partie 2 — Évaluation et compléments

| N° | Annexe | Contenu |
|---|---|---|
| A1 | [Évaluation : qualité et performances](annexes/A1-evaluation-qualite-et-performances.md) | banc de 38 questions, réglages qui changent le résultat, préconisations |
| A2 | [Choisir son matériel et ses modèles](annexes/A2-choisir-son-materiel-et-ses-modeles.md) | configurations minimales sans et avec carte graphique, taille de contexte, temps d'attente |
| A3 | [Automatiser par l'API et MCP](annexes/A3-automatiser-par-l-api.md) | API REST, exemples exécutés, serveur MCP |
| A4 | [Exploitation](annexes/A4-exploitation.md) | sauvegarde et restauration, mise à jour, journaux, sécurité, administration |
| A5 | [Fonctionnement interne](annexes/A5-fonctionnement-interne.md) | architecture, services, ports, notions techniques |
| A6 | [Rapport d'essais](annexes/A6-rapport-d-essais.md) | méthode, preuves, étiquettes, renvois aux résultats bruts |
| — | [Carte de l'interface](annexes/carte-interface.md) | chaque page, menu et réglage de l'interface, et le chapitre qui le couvre |

Une présentation d'une page reste disponible : [Open Notebook en bref](presentation.md). Termes communs à la série : [glossaire général](../glossaire.md).

## Parcours conseillés

| Objectif | Lire |
|---|---|
| Savoir si l'outil convient | 01, puis A1 et A2 |
| Installer et essayer | 01, 02, 03, 04 |
| Travailler sur ses documents au quotidien | 05, 06, 07, 08, puis 11 |
| Produire un podcast | 04, 09 |
| Automatiser | 04, puis A3 |
| Exploiter et dépanner | 12, A4, A5 |

## Ce qui reste ouvert

| Sujet | État | Ce qui permettrait de conclure |
|---|---|---|
| Documents scannés | OCR de Docling inopérant dans l'image 1.15.1 ; le contrat scanné reste illisible (6 erreurs du banc) | installer le moteur d'OCR dans l'image, ou signaler le défaut au projet (décision en attente) |
| Mode « Demander » | une question essayée dans l'interface ; banc complet non rejoué sur le service central | rejouer `banc.py --mode ask` |
| Sources en aperçus | effet mesuré sur cinq questions seulement | banc complet en mode aperçus |
| Réflexion de `chat` | non réglable depuis Open Notebook | modèle de réponse sans réflexion ou plus léger dans LLM-Service (décision en attente) |
| Profil sans carte graphique | non mesuré avec le service central ; chiffres tirés des mesures de LLM-Service | rejouer le banc avec le service en profil `cpu` |
| Exemples de l'API, sauvegarde et restauration | sorties et essai du 8 novembre (ancienne pile) | les rejouer sur le service central |
