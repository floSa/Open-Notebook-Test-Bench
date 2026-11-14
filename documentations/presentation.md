# Open Notebook en bref

Version 1.15.1, essayée le 12 novembre 2026 sous Windows 11 (WSL2), avec les modèles du service LLM central. Cette page reprend le chapitre [01. Découvrir Open Notebook](manuel/01-decouvrir-open-notebook.md) du manuel ; la suite du manuel est sommairement décrite dans [la page d'accueil](README.md).

## Ce que c'est

Open Notebook est une application web qui permet de poser des questions à ses propres documents et d'obtenir des réponses qui indiquent de quel document vient chaque information. Elle s'utilise dans le navigateur, mais tout tourne sur la machine : les documents ne partent vers aucun service en ligne.

Le travail s'organise en **carnets**, un par sujet ou par dossier. Un carnet réunit :

- des **sources** : fichiers PDF, Word, Excel, PowerPoint, pages web, textes collés, enregistrements audio ;
- une **conversation** : une question en langage courant, une réponse rédigée à partir des sources, avec un renvoi cliquable vers le document utilisé (la **citation**) ;
- des **notes** : réponses gardées, résumés, notes libres.

À partir d'un carnet, l'application sait aussi appliquer une consigne réutilisable à un document (une **transformation** : résumé, liste des chiffres clés…), chercher dans tous les carnets à la fois, et produire un **podcast** : un dialogue audio à deux voix qui présente le contenu des documents.

## Les mots à connaître

| Mot | Sens dans ce manuel |
|---|---|
| Carnet | dossier de travail : des sources, des notes, des conversations sur un même sujet |
| Source | un document ajouté à un carnet (fichier, lien web, texte collé, audio) |
| Conversation (chat) | échange de questions et de réponses avec le modèle d'IA, à partir des sources du carnet |
| Citation | renvoi, à la fin d'une phrase de la réponse, vers la source qui la justifie ; un clic ouvre la source |
| Note | texte gardé dans le carnet : écrit à la main, ou réponse enregistrée |
| Transformation | consigne réutilisable appliquée à une source, par exemple « résumer » |
| Modèle d'IA | programme qui rédige les réponses (modèle de langage) ou qui calcule la ressemblance de sens entre deux textes (modèle d'embedding) |
| Service LLM central | le service, installé à part, qui fait tourner les modèles d'IA pour toutes les applications de la machine |
| Jeton | unité de texte comptée par le modèle : environ trois quarts de mot en français |

Les autres termes sont dans le [glossaire](manuel/13-glossaire.md).

## Pour qui

| Adapté | Peu adapté |
|---|---|
| Une personne qui travaille sur un dossier de quelques dizaines de documents et veut des réponses vérifiables | Une équipe : il n'existe qu'un mot de passe commun, sans comptes ni droits séparés |
| Des documents confidentiels qui ne doivent pas partir vers un service en ligne | Des documents scannés : l'application ne les lit pas en l'état |
| Des documents texte, des tableaux, des réunions enregistrées | Une question posée à des centaines de documents à la fois dans la conversation : elle transmet au modèle les documents choisis en entier, ce qui en limite le volume |

## Le projet

| | |
|---|---|
| Dépôt | https://github.com/lfnovo/open-notebook |
| Site | https://www.open-notebook.ai |
| Licence | MIT : libre, usage commercial autorisé |
| Popularité | 41 884 étoiles et 4 815 copies (forks) sur GitHub |
| Activité | très active : 114 modifications sur les 90 derniers jours, 98 contributeurs, une nouvelle version par mois environ |
| Ancienneté | projet créé en octobre 2024 ; versions 1.x stables |
| Coût | gratuit, sans abonnement |

Chiffres relevés sur GitHub le 12 novembre 2026.

## Ce que fait l'application

Réponses : **Oui**, **Non**, ou **Partiel** avec la limite en une phrase.

| Fonction | Réponse |
|---|---|
| Modèles d'IA installés sur la machine (service compatible OpenAI, Ollama, LM Studio…) | Oui |
| Services en ligne payants (OpenAI, Anthropic, Mistral, Google…) | Oui, une vingtaine ; non utilisés dans ce manuel |
| Second tri des passages par un modèle spécialisé (reranker) | Non |
| PDF, Word, Excel, PowerPoint, OpenDocument, EPUB, texte, Markdown, pages web | Oui |
| Tableaux dans les documents | Oui, avec le module de lecture avancée (Docling), activé dans cette installation |
| Documents scannés (reconnaissance de caractères) | Non : le module prévu ne fonctionne pas dans la version 1.15.1 |
| Audio et vidéo | Oui, transcrits automatiquement |
| Conversation sur les documents d'un carnet, avec citations | Oui, document par document ; pas de numéro de page |
| Recherche par mots et recherche par le sens | Oui, séparément ; pas de recherche qui combine les deux |
| Question posée à tous les carnets à la fois (« Demander ») | Oui |
| Refus de répondre quand l'information n'est pas dans les documents | Oui |
| Notes, résumés et extractions par consigne réutilisable | Oui |
| Podcast | Oui, de 1 à 4 voix ; une seule voix française disponible avec le serveur de voix utilisé |
| Interface en français | Oui |
| Plusieurs utilisateurs avec leurs propres comptes | Non |
| API pour automatiser | Oui, complète |
| Fonctionnement hors ligne | Oui, sauf une vérification de version auprès de GitHub, impossible à couper |

## Le matériel nécessaire

Open Notebook lui-même est léger : environ 0,5 Go de mémoire vive, près de 3 Go quand le module de lecture avancée des documents (Docling) est chargé, et 2,6 Go de disque pour ses images. L'essentiel de la machine sert aux **modèles d'IA**, qui tournent dans le service LLM central. Ce service fonctionne de deux façons : avec une carte graphique NVIDIA, ou sur le processeur seul, plus lentement. Pour l'application, rien ne change : même adresse, mêmes modèles.

Les modèles utilisés sont les mêmes dans les deux cas : un modèle de réponse de 4 milliards de paramètres (Qwen3.5-4B, nommé `chat`), un modèle d'embedding multilingue (bge-m3, nommé `embed`) et un modèle de transcription de la voix (faster-whisper-small, nommé `transcribe`). Chaque question peut envoyer au modèle 16 384 jetons au plus, soit environ 45 000 caractères ou une quinzaine de pages, réflexion du modèle et réponse comprises.

### Configuration minimale sans carte graphique

| Élément | Minimum |
|---|---|
| Processeur | 8 cœurs récents |
| Mémoire vive | 16 Go |
| Disque libre | 25 Go : modèles d'IA environ 6 Go, images du service central et d'Open Notebook, module Docling 6 Go |
| Mémoire prise par le service central | environ 4,3 Go, les trois modèles permanents chargés |
| Mémoire prise par Open Notebook | 0,5 Go, 3 Go avec Docling |
| Ce qui reste sur 16 Go | environ 8 Go pour Windows, le navigateur et les autres programmes |

Temps d'attente : le modèle de réponse écrit environ 14 jetons par seconde, soit une réponse de quelques phrases en 10 à 20 secondes, plus le temps de lire les documents envoyés. Le modèle **réfléchit** avant de répondre ; sur processeur seul, une question qui demande un calcul peut prendre environ 2 minutes. L'ajout d'un document de quelques pages prend de quelques secondes à une minute.

### Configuration minimale avec carte graphique NVIDIA

| Élément | Minimum |
|---|---|
| Carte graphique | 12 Go de mémoire : les trois modèles permanents en prennent 7,0 Go, Windows et l'affichage environ 1,8 Go ; une carte de 8 Go ne suffit pas ; la machine d'essai en a 16 |
| Mémoire vive | 16 Go ; la machine d'essai en a 32 |
| Mémoire vive prise par le service central | environ 5,4 Go |
| Mémoire prise par Open Notebook | 0,5 Go, 3 Go avec Docling |

Temps d'attente : le modèle écrit environ 68 jetons par seconde. Une question sur neuf documents reçoit sa réponse en quelques secondes ; une question de calcul avec réflexion prend 15 à 40 secondes.

Le détail des mesures et leurs sources est dans l'annexe [A2](annexes/A2-choisir-son-materiel-et-ses-modeles.md).

## Les résultats mesurés

Test sur 38 questions dont la réponse est connue, posées à 9 documents d'une entreprise fictive, avec le modèle `chat` du service central sur carte graphique ; détail dans l'annexe [A1](annexes/A1-evaluation-qualite-et-performances.md).

| Mesure | Résultat |
|---|---|
| Réponses justes | 28 sur 34 ; les 6 erreurs portent sur le contrat scanné, illisible |
| Questions sans réponse dans les documents | 4 refus sur 4, aucune réponse inventée |
| Temps de réponse | 9 secondes en général, jusqu'à une minute quand le modèle réfléchit longtemps |
| Ajout des 9 documents | environ une minute (quelques minutes avec le résumé automatique de chaque document) |
| Document trop long pour une question | refusé avec un message d'erreur clair, jamais tronqué en silence |

## Bon à savoir

- Une réponse citée n'est pas forcément juste : la citation désigne le document, pas la phrase exacte. Les chiffres importants se relisent dans la source.
- La conversation envoie au modèle les documents choisis **en entier**, à chaque question : plus le carnet est gros, plus l'attente est longue. Le chapitre [06](manuel/06-discuter-avec-les-sources.md) explique comment choisir ce qui est envoyé.
