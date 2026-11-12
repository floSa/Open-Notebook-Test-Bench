# A2. Choisir son matériel et ses modèles

> **Objet** : dimensionner une machine pour Open Notebook branché au service LLM central : configurations minimales sans et avec carte graphique, mémoire, taille de contexte, temps d'attente.
> **Prérequis** : [Découvrir Open Notebook](../manuel/01-decouvrir-open-notebook.md) ; [évaluation](A1-qualite-et-performances.md).
> **Version décrite** : Open Notebook 1.15.1 ; service LLM central de LLM-Service (branche `service-llamacpp`) : `chat` = Qwen3.5-4B (GGUF, vision, réflexion activée), `embed` = bge-m3 (Q8_0, 1 024 dimensions), `rerank` = bge-reranker-v2-m3 (non utilisé par Open Notebook), `transcribe` = faster-whisper-small ; 16 384 jetons par requête.
> **Statut des informations** : [Vérifié] mesuré sur la machine d'essai (profil B : Ryzen 5 9600X, 32 Go, RTX 4060 Ti 16 Go), avec renvoi au résultat brut ; [Source] mesures publiées par LLM-Service dans son dépôt (README, section « Mesures », dossiers `mesures/gpu` et `mesures/cpu`, relus le 12 novembre 2026) ; [Estimation] calcul à partir de ces mesures, avec sa base ; [À tester] non essayé.
> **Précautions** : le profil A (sans carte graphique) n'a pas été mesuré avec le service central sur la machine d'essai : ses chiffres viennent des mesures de LLM-Service en profil `cpu` (même machine B, carte non utilisée) et sont marqués comme tels ; les chiffres du profil A mesurés le 8 novembre portent sur l'ancienne pile (Ollama, qwen3:4b-instruct) et ne se comparent pas tels quels.

## Sommaire

1. [Ce qui consomme la mémoire](#1-ce-qui-consomme-la-mémoire)
2. [Profil A : sans carte graphique](#2-profil-a--sans-carte-graphique)
3. [Profil B : avec carte graphique NVIDIA](#3-profil-b--avec-carte-graphique-nvidia)
4. [Taille de contexte et volume de documents](#4-taille-de-contexte-et-volume-de-documents)
5. [Modèles](#5-modèles)
6. [Dépannage](#dépannage)
7. [Sources](#sources)

## 1. Ce qui consomme la mémoire

| Élément | Mémoire | Statut |
|---|---|---|
| Open Notebook au repos, sans Docling | environ 0,4 à 0,5 Go (interface Next.js, API FastAPI, tâches de fond, SurrealDB) | [Vérifié] le 8 novembre ([vérification minimale](../../../outils/resultats/open-notebook/verif-minimale-2026-11-08.json)) |
| Open Notebook avec Docling chargé | 2,8 Go au repos, 4,7 Go en pointe pendant le banc (application 4,5 Go + SurrealDB 0,2 Go) | [Vérifié] ([vérification minimale](../../../outils/resultats/open-notebook/verif-minimale-2026-11-12.json), [banc](../../../outils/resultats/open-notebook/banc-2026-11-12-central-chat.json), champ `pic_ram_mo`) |
| Service central, profil `gpu` | 5,4 Go de mémoire vive (LiteLLM 0,8, llama-swap 4,4, Speaches 0,2 à 1,5) ; 7,0 Go de mémoire de carte pour `chat`, `embed`, `rerank` | [Source] README de LLM-Service ; [Vérifié] en pointe de banc : `llm-central` 0,7 Go, `llm-swap` 5,8 Go, `llm-speaches` 1,5 Go, carte 8,4 Go utilisés sur 16 (Windows compris) |
| Service central, profil `cpu` | 4,3 Go (LiteLLM 0,6, llama-swap 3,6, Speaches 0,1), trois modèles chargés | [Source] `LLM-Service/mesures/cpu/memoire-vive-conteneurs.txt` |
| Serveur de synthèse vocale `rag-speaches` (podcasts) | 0,5 à 2,4 Go selon les voix chargées | [Vérifié] le 8 novembre ([ressources](../../../outils/resultats/open-notebook/ressources-2026-11-08.txt)) |

## 2. Profil A : sans carte graphique

Configuration minimale [Estimation] (base : mesures `cpu` de LLM-Service et mémoire de l'application ci-dessus) :

| Élément | Valeur |
|---|---|
| Processeur | 8 cœurs récents (AVX2) |
| Mémoire vive | 16 Go : service central 4,3 Go + Open Notebook 3 Go avec Docling (0,5 Go sans) + voix 0,5 à 2,4 Go ; reste environ 6 à 8 Go pour Windows, WSL et le navigateur |
| Disque | 25 Go : modèles GGUF environ 6 Go, images du service central et d'Open Notebook (2,6 Go), Docling 6 Go, voix 3 Go |
| Contexte | 16 384 jetons par requête (fixé par le service) |
| Débit de `chat` | 14 jetons/s pour une requête, 31 jetons/s cumulés pour quatre [Source] |
| Réflexion | environ 2 minutes sur une question de calcul [Source] |

Temps d'attente [Estimation] : une réponse de 150 jetons s'écrit en une dizaine de secondes à 14 jetons/s ; s'y ajoutent la lecture des documents envoyés (plusieurs dizaines de secondes pour quelques milliers de jetons sur processeur, d'après l'ancienne pile : 36 à 67 jetons/s de lecture) et la réflexion de `chat`, qu'Open Notebook ne permet pas de couper. Une question sur les neuf documents du corpus (environ 3 000 jetons) demanderait donc de l'ordre d'une à trois minutes, contre 9 s en médiane sur carte graphique. Indexation : l'embedding `embed` répond en 0,08 s par lot de 10 passages [Source] ; la transcription et le résumé automatique de chaque document ajouté dominent.

## 3. Profil B : avec carte graphique NVIDIA

Configuration mesurée [Vérifié] (machine d'essai) :

| Élément | Valeur |
|---|---|
| Machine | Ryzen 5 9600X, 32 Go, RTX 4060 Ti 16 Go ([diagnostic](../../../outils/resultats/machine/diagnostic-2026-11-12.json)) |
| Carte graphique | 8,4 Go utilisés sur 16 en fin de banc, Windows compris ; les trois modèles permanents en prennent 7,0 Go [Source] |
| Mémoire vive en pointe | application 4,7 Go + service central 8,0 Go (dont Whisper chargé) ([banc](../../../outils/resultats/open-notebook/banc-2026-11-12-central-chat.json)) |
| Débit de `chat` | 68 jetons/s pour une requête, 174 jetons/s cumulés pour quatre [Source] |
| Banc | 28/34 justes, 4/4 refus, médiane 8,7 s, p95 27,9 s ; indexation des 9 documents 65 s |

Configuration minimale [Estimation] : carte de 12 Go (7,0 Go de modèles + environ 1,8 Go pris par Windows et l'affichage, mesurés par LLM-Service service arrêté), 16 Go de mémoire vive ; une carte de 8 Go ne suffit pas pour garder les trois modèles chargés.

## 4. Taille de contexte et volume de documents

La conversation d'un carnet n'a pas de recherche : elle envoie à chaque question les consignes du système, les sources choisies (aperçu ou texte entier), les notes, l'historique de la session et la question ; la réflexion de `chat` et la réponse doivent tenir dans le reste des 16 384 jetons [Source] (code `open_notebook/graphs/chat.py`, synthèse dans [A5](A5-fonctionnement-interne.md)).

| Situation | Jetons envoyés (compteur « Context ») | Résultat | Statut |
|---|---|---|---|
| Corpus de 9 documents + 1 texte, contenu complet, 2 notes | 7,0 K (24 200 caractères) | réponses justes en 13 à 20 s | [Vérifié] (captures du chapitre 11) |
| Même carnet, sources en aperçus | 4,5 K (14 800 caractères) | réponses incomplètes | [Vérifié] |
| Texte de 80 000 caractères en contenu complet | 19,8 K annoncés, 21 842 comptés par le service | refus : « ContextWindowExceededError » | [Vérifié] ([dépassement](../../../outils/resultats/open-notebook/contexte-2026-11-12.txt)) |

Ordre de grandeur [Estimation] (base : 24 200 caractères pour 7,0 K jetons, soit environ 3,5 caractères par jeton) : en gardant environ 4 000 jetons pour la réflexion et la réponse, il reste environ 12 000 jetons, soit de l'ordre de 40 000 caractères ou une quinzaine de pages en contenu complet. Au-delà, mettre des sources en aperçus, ouvrir une nouvelle session, ou utiliser « Demander », qui n'envoie que les passages trouvés (10 résultats par recherche [Source]).

## 5. Modèles

| Nom fixe | Modèle réel | Usage dans Open Notebook |
|---|---|---|
| `chat` | Qwen3.5-4B (GGUF), réflexion activée par défaut | conversation, transformations, « Demander », plan et texte des podcasts |
| `embed` | bge-m3 Q8_0, 1 024 dimensions, multilingue | recherche vectorielle, « Demander » |
| `transcribe` | faster-whisper-small | sources audio et vidéo |
| `rerank` | bge-reranker-v2-m3 | non utilisé : Open Notebook n'accepte aucun reranker ([relevé](../../../outils/resultats/open-notebook/reranker-2026-11-12.txt)) |

Modèles relevés par `/v1/models` [Vérifié] ([diagnostic](../../../outils/resultats/machine/diagnostic-2026-11-12.json)). Le service expose aussi `gemma-4-e4b` (chargé à la demande) ; il n'a pas été passé au banc. Un modèle de réponse plus léger, pour situer un plancher de qualité sur processeur, demande un changement dans LLM-Service, hors de cette mission (décision en attente).

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| Réponses très lentes sans carte graphique | réflexion de `chat` sur processeur | limiter les documents en « contenu complet » ; préférer une carte graphique |
| Mémoire de WSL saturée | Docling, service central et voix chargés ensemble sur 16 Go | désactiver Docling si les documents n'ont pas de tableaux ; arrêter `rag-speaches` hors podcasts (`arreter.sh --voix`) |
| Carte graphique pleine | autre modèle chargé à la demande (`gemma-4-e4b`) | relève de LLM-Service |

## Sources

- LLM-Service, README (sections « Mesures », « Réflexion et vision ») et `mesures/cpu/memoire-vive-conteneurs.txt`, relus le 12 novembre 2026 (dépôt séparé `~/mes_projets/Projet-IA/LLM-Service`, branche `service-llamacpp`, commit `8568e75`).
- Résultats : [banc](../../../outils/resultats/open-notebook/banc-2026-11-12-central-chat.json), [vérification minimale](../../../outils/resultats/open-notebook/verif-minimale-2026-11-12.json), [diagnostic](../../../outils/resultats/machine/diagnostic-2026-11-12.json).
