# Journal de la mission

Solution en cours : Open Notebook (`kit/fiches/01-open-notebook.md`).

## Décisions en attente

| N° | Décision | Option retenue (la plus prudente) | À trancher par l'utilisateur |
|---|---|---|---|
| D1 | La machine d'exécution n'a pas de GPU NVIDIA (Intel Arc 140T intégré, invisible pour Docker). Le §2 du prompt prévoit l'arrêt ; le `/goal` exige d'aller au critère de fin. | Socle sur CPU avec Ollama (repli prévu par la fiche), image locale `ollama/ollama` 0.30.7 figée par empreinte, modèles déjà présents copiés depuis `~/.ollama`. vLLM non installé. Profil A mesuré sur CPU ; profil B (RTX 4060 Ti 16 Go) en [Estimation]. | Relancer la mission sur une machine NVIDIA pour mesurer vLLM, ou accepter le socle CPU. |
| D3 | L'OCR de Docling ne fonctionne pas dans l'image 1.15.1 (`onnxruntime` absent). L'installer dans le conteneur sort de l'enveloppe (paquets PyPI seulement dans `.venv` du dépôt). | Ne pas modifier le conteneur ; scan documenté en échec, contournement en [À tester]. | Autoriser `pip install onnxruntime` dans le conteneur, ou signaler le défaut au projet. |
| D4 | Le banc en mode « Demander » (Ask) sur 38 questions dépasserait plusieurs heures sur CPU. | Échantillon d'une question par type, consigné comme tel. | Relancer le banc Ask complet sur une machine avec GPU. |
| D2 | Des conteneurs `rag-ollama`, `rag-agent-api`, `rag-frontend` existent déjà (autre projet `rag-agent-chat`, arrêtés). | Ne pas y toucher. Conteneur du socle nommé `rag-socle-ollama`, avec l'alias réseau `rag-ollama` sur le réseau `rag-local`. `nettoyer.sh` ne vise que des noms explicites. | Renommer ou supprimer l'ancien projet si souhaité. |

## Entrées

### 2026-11-08 13:15 — Phase A, diagnostic

- Fait : extraction du kit, `git init`, commit du kit ; `outils/communs/diagnostic.sh` écrit et lancé.
- Résultat : Intel Core Ultra 7 255H (16 fils), 15,3 Go de RAM et 4 Go de swap dans WSL, 619 Go libres, Docker 29.9.2, Compose 5.6.1, WSL 2.7.14. Aucun GPU NVIDIA : `nvidia-smi` absent, `docker run --gpus all` échoue (« no known GPU vendor found »). Registres joignables, port publié sur 127.0.0.1 joignable depuis WSL.
- Version d'Open Notebook retenue : 1.15.1 (publiée le 2026-11-04), image `lfnovo/open_notebook:1.15.1@sha256:e4e18f12653df5bf48674b7b187c4252be52238b4d706330fd30d9b177b95812`.
- Fichiers : `outils/communs/diagnostic.sh`, `outils/resultats/machine/diagnostic-2026-11-08.json`, `JOURNAL.md`, `.gitignore`.
- Suite : phase B, socle CPU (inventaire des modèles, Ollama, corpus, banc).

### 2026-11-08 13:20 — Phase B (en cours) et phase C, cadrage

- Fait : socle Ollama CPU (`outils/communs/socle.sh`), inventaire de 22 modèles présents, choix qwen3:4b-instruct (chat), ministral-3:3b (second modèle), bge-m3 (embedding, seul téléchargement, 1,2 Go) ; corpus Vélanor reproductible à l'octet (8 documents, `corpus/MANIFEST.json`) ; 36 questions de référence ; banc commun et son auto-contrôle ; `verifier_docs.py` ; `nettoyer.sh`. Cadrage d'Open Notebook 1.15.1 par sous-agent (`outils/resultats/open-notebook/cadrage-source.md`), relecture consignée (`relecture.md`), compose officiel copié et override écrit, scripts installer/démarrer/arrêter/état, plan des manuels.
- Résultat : Ollama CPU, 16 à 17 jetons/s en génération, 53 à 67 jetons/s en lecture de prompt (mesures en cours). Constats de cadrage : chat de carnet sans top-k (sources injectées en entier), citations seulement `[source:id]` dans le texte, OCR des scans seulement avec Docling.
- Incident : `python3-venv` absent (sudo exclu) ; `.venv` créé avec `uv`. L'image `ubuntu:24.04` a été tirée par le premier test GPU, hors liste des images autorisées ; elle n'est plus utilisée (diagnostic et nettoyage passent par l'image Ollama) et n'a pas été supprimée (suppression hors `rag-` interdite).
- Fichiers : `outils/communs/*`, `outils/open-notebook/*`, `outils/resultats/open-notebook/*`, `docs/glossaire.md`, `docs/open-notebook/plan-des-manuels.md`, `outils/README.md`.
- Suite : fin des mesures du socle, puis phase D (installation testée).

### 2026-11-08 13:55 — Phase B (fin) et phase D, installation testée

- Fait : mesures du socle en deux passes (la passe 1 a été arrêtée volontairement pendant le palier 32768, trop long, puis le script a été rendu incrémental et robuste) ; installation d'Open Notebook 1.15.1 par `outils/open-notebook/installer.sh` ; branchement au socle par l'API (`configurer.py`) ; vérification des ports (`verifier_ports.sh`) ; vérification fonctionnelle minimale (`verif_minimale.py`) ; seconde exécution de l'installateur (idempotence).
- Résultat : qwen3:4b-instruct 14,7 à 17,9 jetons/s en génération ; lecture du prompt 67 (4096) → 53 (8192) → 36 (16384) → 24 jetons/s (32768) ; RAM d'Ollama 7,3 → 13,9 Go ; 32768 tient mais demande 873 s pour un prompt de 16 000 jetons. Dépassement : 8 800 jetons envoyés avec `num_ctx` 2048, tronqués à 2 047 sans erreur (`truncated = 1` dans les journaux). Installation : 146 s la première fois (dont 120 s d'attente inutile, l'interface répondant 307 ; corrigé), 2 s ensuite. Ports sur 127.0.0.1 seulement, refusés sur l'adresse de WSL ; API en 401 sans mot de passe. Application seule : 458 Mo au repos, environ 550 Mo en pointe d'indexation. Question test : réponse juste avec `[source:…]` en 28,7 s. Le moteur d'URL vaut déjà `simple` par défaut.
- Fichiers : `outils/communs/mesure_modeles.py`, `outils/resultats/socle/mesures-*`, `outils/open-notebook/*`, `outils/resultats/open-notebook/{installation,configuration,ports,verif-minimale,disque}-2026-11-08.*`, relectures Speaches et MCP.
- Suite : serveur de voix Speaches, captures, puis manuels.

### 2026-11-08 14:20 — Phase E et F en cours

- Fait : serveur de voix Speaches (Kokoro, faster-whisper-small copié), message audio du corpus (38 questions, dont 2 audio) ; voix branchée dans Open Notebook ; banc de référence (chat, « full content », qwen3:4b-instruct, sans Docling) ; correction de la notation du banc (« 8 » reconnu dans « 87 ») et renotation (`renoter.py`) ; essai MCP (`open-notebook-mcp` 0.3.0 avec `mcp<2`) ; Docling activé et mesuré ; essai des formats avec et sans Docling ; manuels 00, 01, 02, 03, 08, 11, 12 rédigés ; file d'essais séquentielle (`file_essais.sh`).
- Résultat : banc de référence 25/34 exactes, 4/4 refus, p50 10,8 s, p95 23,8 s, indexation 70 s. Défauts constatés : tableau DOCX perdu sans Docling ; transcription audio en échec sans `OPENAI_COMPATIBLE_BASE_URL_STT` (contourné) ; OCR de Docling inopérant (`onnxruntime` absent, D3) ; `create_source` du serveur MCP tiers en échec. Docling : 72 s d'installation, 5,7 Go, paquets CUDA inutiles.
- Incident : l'étape `formats` de la file a tourné avant la réindexation Docling ; relancée à la main après (fichier écrasé). `pkill -f` a tué deux fois le shell appelant (motif présent dans sa propre ligne de commande) ; garde-fou réécrit en script.
- Suite : fin de la file (banc Docling, recherche, transformations, ministral, contexte 4096, exemples), puis chat, podcast, démo, sauvegarde, manuels 04 à 07, 09, 10, phase H.

### 2026-11-08 16:10 — Incident : mémoire de WSL saturée

- Constat : l'application signalait « reconnexion à Ubuntu 24.04 » depuis 36 minutes. RAM de WSL 15,3/15,7 Go, swap 4/4 Go, charge 47 ; `rag-socle-ollama` à 12,8 Go.
- Cause : échantillon « Demander » (sorties de stratégie très longues, jusqu'au délai de 900 s) après l'essai du chat qui avait chargé un troisième modèle (qwen3:4b), avec deux requêtes simultanées et le cache de prompts d'Ollama.
- Action : arrêt de `suite_essais.sh`, de l'échantillon « Demander » (6 questions sur 8 passées, résultats dans `essai-2026-11-08-banc-ask.log` seulement : 1 exacte, 4 réponses vides, durées de 74 à 1 089 s) et de l'attente de `suite_essais2.sh` ; déchargement des modèles. RAM disponible revenue à 13,3 Go.
- Suite : podcast, démonstration et banc 6144 lancés un par un, en surveillant la mémoire ; « Demander » déclaré inutilisable sur CPU avec ce modèle (D4).

### 2026-11-08 17:35 — Phase F (fin) : podcast, démonstration, banc 6144

- Fait : podcast généré (profils `duo-fr` et `court-fr`, 77 s d'audio, 307 s de génération) ; manuel 07 ; jeu de démonstration « Démo Vélanor » (8 sources sur 9, trois conversations citées, deux notes) ; manuel 09 ; sauvegarde rendue plus légère (cache Docling de 6,2 Go exclu, repris à la restauration) ; vérificateur : les libellés cités entre « » ne comptent plus pour le ton ; banc à `num_ctx` 6144 lancé.
- Incident : la tâche de podcast est restée « new » pendant 3 600 s : worker bloqué depuis la saturation mémoire (connexion SurrealDB perdue). `docker restart rag-open-notebook` : tâche reprise et terminée. Speaches (2,4 Go) redémarré pour libérer la mémoire ; modèle de chat déchargé avant la démonstration.
- Résultat : la seconde voix (`am_michael`, anglaise) disparaît de la transcription de contrôle de l'épisode ; recette 3 de la démonstration : un pourcentage de 2025 attribué à l'objectif 2026 sous une citation valide.
- Suite : fin du banc 6144, manuel 10, sauvegarde et restauration, relecture adversariale (en cours), phase H.

### 2026-11-08 18:50 — Phase G (fin) et phase H, clôture

- Fait : banc à `num_ctx` 6144 (28/34, 4/4 ; latences faussées par les rechargements du modèle, car le juge LLM tourne à 16384 ; preuve : extrait du journal d'Ollama dans `outils/resultats/socle/`) ; manuel 10 complété ; essai de sauvegarde et de restauration (28 s, 5,5 Mo ; 18 s ; carnet témoin disparu, question de contrôle juste) ; relecture adversariale par un sous-agent neuf (22 points, tous traités ou requalifiés) ; nettoyage (carnets « Banc » et « Essai installation » supprimés, données mises de côté par la restauration supprimées) ; relevé des ressources ; `RAPPORT-open-notebook.md` ; index et comparatif ; garde-fou mémoire arrêté.
- Résultat : `verifier_docs.py` à 0 point ; solution en marche (`num_ctx` 16384), interface sur http://127.0.0.1:8502 (307 vers `/notebooks`) ; carnet « Démo Vélanor » et un épisode de podcast gardés.
- Incident : `nettoyer_essais.py` s'est arrêté sur une limite de l'API (`limit` ≤ 100) après avoir supprimé les carnets ; corrigé et relancé, consigné dans `nettoyage-2026-11-08.txt`.
- Suite : décisions D1 à D4 à trancher par l'utilisateur ; solution suivante proposée : RAGFlow (fiche 02).

### 2026-11-08 19:05 — Fiche de présentation

- Demande de l'utilisateur : une page d'entrée qui dit ce que fait la solution et la situe face aux concurrentes (dépôt, étoiles, licence, activité, moteurs, embeddings, reranking, formats, OCR, web, audio, connecteurs, recherche, citations, stockage, RAG avancé, carnets…), sur le modèle de son comparatif HTML du 7 novembre.
- Fait : `docs/open-notebook/presentation.md` (en une minute, identité GitHub relevée par `outils/communs/identite_github.py`, fonctions, grille de 30 critères avec statut et écart au comparatif, résultats) ; liens en tête du README racine, de l'index général, de l'index de la solution et du plan.
- Résultat : deux cases « non documenté » du comparatif tranchées (reranking : non ; OCR : non en l'état) ; « 100 % local » nuancé (vérification de version vers GitHub). 41 764 étoiles, MIT, 114 commits sur 90 jours.

### 2026-11-08 22:55 — Service de modèles commun : LLM-Service

- Demande de l'utilisateur : un seul service de modèles pour toutes les applications, son dépôt LLM-Service (`~/Projets/Projet-IA/LLM-Service`), au lieu d'un Ollama propre à la série.
- Fait : historique git découpé en commits par fonctionnalité (ancien historique gardé dans la branche `sauvegarde-historique-avant-decoupage`) ; LLM-Service passé sur `service-ollama`, `.env` local (contexte 16384, un modèle à la fois, préchargement qwen3:4b-instruct et bge-m3), override local sans GPU ; modèles déplacés depuis `donnees/socle/ollama` (8,5 Go, aucun téléchargement) ; `rag-socle-ollama` supprimé ; Open Notebook sur les réseaux `llm-net` et `rag-local`, configuration `llm-service` ; scripts, manuels, rapport et kit mis à jour.
- Incidents : (1) le préchargement a mis à jour le manifeste de qwen3:4b-instruct (poids identiques, paramètres d'échantillonnage du registre) ; (2) génération à 0,4 jeton/s : 16 fils de calcul sur le processeur hybride ; corrigé par `LLAMA_ARG_THREADS=8` (13,3 jetons/s) ; (3) greffon `docker compose` de Docker Desktop en erreur d'entrée-sortie dans WSL : contourné par le binaire `/usr/libexec/docker/cli-plugins/docker-compose` ; un redémarrage de Docker Desktop devrait le réparer.
- Résultat : échantillon de 6 questions identique au banc d'origine ; vérification minimale passée ; seul le carnet « Démo Vélanor » reste.
- Suite : prompt de la mission RAGFlow.

### 2026-11-09 11:19 — Nouvelle machine, banc GPU (vLLM)

- Contexte : changement de portable (Ryzen 5 9600X, RTX 4060 Ti 16 Go de VRAM, WSL). Dépôt déjà poussé, corpus présent ; `donnees/` et le service de modèles à reconstruire localement.
- Demande de l'utilisateur : mesurer la configuration GPU minimale restée estimée (section 3 de la précédente reprise), avec un service de modèles décorrélé de l'application, réutilisable pour les prochaines solutions (RAGFlow…).
- Fait : LLM-Service basculé sur `service-vllm` (un `git stash` de modifications non commitées trouvées sur `service-ollama` mis de côté, non résolu, voir reprise) ; embedding remplacé par bge-m3 (multilingue, au lieu de nomic-embed-text, anglophone) ; modèle de chat gardé tel quel (Gemma 4 E4B, déjà partagé par d'autres projets sur cette machine) plutôt que de télécharger Qwen3-4B-Instruct comme prévu. `configurer.py` et `banc.py` étendus pour le fournisseur « OpenAI Compatible » à deux crédentials (un par modalité, vLLM ne servant qu'un modèle par conteneur) ; `installer.sh` et `llm_service.sh` paramétrés par `MOTEUR=ollama|vllm` ; chemin par défaut de LLM-Service corrigé (`~/Projets` n'existe pas sur cette machine, `~/mes_projets`). Open Notebook installé et branché sur vLLM ; banc rejoué en chat et en « Demander », avec et sans Docling.
- Incidents : dossier `vllm/entrypoint.sh` créé par erreur en tant que répertoire root par un précédent essai Docker, bloquant le `git switch` (nettoyé via un conteneur Docker, sans sudo) ; bug d'idempotence dans `configurer.py` (même modèle passé en `--chat` et `--second`, doublon refusé par l'API) ; `OPEN_NOTEBOOK_ENABLE_DOCLING` non généré par `installer.sh` malgré ce que décrit le README (corrigé) ; lien mort vers `kit/LANCEMENT.md` (dossier retiré du dépôt depuis, lien supprimé).
- Résultat : banc GPU (Docling actif) identique au CPU en exactitude (28/34, 4/4 refus), 4 fois plus rapide (médiane 1,86 s contre 7,44 s) ; mode « Demander », abandonné sur CPU, devient utilisable (28/34, médiane 7,7 s). VRAM 15,7/16,4 Go, marge faible. Manuel 10, `presentation.md` et README mis à jour avec les chiffres mesurés ; `verifier_docs.py` à 0 point.
- Suite : relire le `git stash` de LLM-Service ; Qwen3-4B-Instruct 4 bits sur vLLM pour une comparaison à modèle identique ; carte à 8 Go de VRAM ; solution suivante (RAGFlow).

### 2026-11-12 09:40 — Reprise au standard du kit : écart et plan

- Début de session : `~/.claude/statut-a-jour.sh` → modifications non commitées (outils communs, `.gitignore`) ; `outils/communs/llm_central_sante.sh --essai` réussi (`chat`, `embed` 1 024 dimensions, `rerank`, `transcribe` sur le message vocal du corpus). Machine : Ryzen 5 9600X, 32 Go, RTX 4060 Ti 16 Go ; service central en profil `gpu` (`llm-swap` CUDA). Commits : `.gitignore` + `.env.example`, outils communs du kit.
- Versions (`outils/resultats/open-notebook/versions-2026-11-12.json`) : Open Notebook v1.15.1 reste la dernière stable (image déjà figée par empreinte) ; SurrealDB v2.7.0 gardée (le compose officiel impose v2 ; dernière stable v4.0.1, raison écrite dans le JSON).
- Écart entre l'existant et le kit :

| Point du kit | Existant | À faire |
|---|---|---|
| Service de modèles | Open Notebook branché sur `vllm-central` / `vllm-embed` (Gemma 4 E4B), puis `ollama-central` ; STT et TTS sur `rag-speaches` | fournisseur « OpenAI Compatible » unique sur `http://llm-central:8080/v1`, noms fixes `chat`, `embed`, `transcribe` ; TTS seul sur `rag-speaches` (non servi par le central) ; anciennes configurations retirées |
| Manuel en deux parties | 13 manuels à plat (`docs/open-notebook/00-12`), mélange utilisateur et preuves | `manuel/01…` (partie 1, sans étiquettes ni renvois aux scripts) et `annexes/A1…A6` (partie 2), contenu vérifié repris |
| Captures annotées | 18 captures sans annotation, 4 manuels sans capture (19 points au vérificateur) | captures refaites à la souris par Playwright, rectangle rouge, pastilles, tableau N° \| Élément \| Rôle, « Où » et « Écran : » |
| Carte de l'interface | absente | `annexes/carte-interface.md` + captures de repérage `img/carte/` |
| Chapitre 01 « Découvrir » | `presentation.md` + `00-notions` | `manuel/01-decouvrir-open-notebook.md`, configurations minimales sans et avec GPU d'après les mesures de LLM-Service |
| Banc | Ollama CPU (qwen3:4b-instruct), vLLM GPU (Gemma 4 E4B) | rejoué avec `chat` (Qwen3.5-4B) ; reranker non accepté par Open Notebook (cadrage) : à revérifier et écrire |
| Relecture novice | jamais faite | sous-agent neuf jusqu'à zéro remarque |
| Rapport | RAPPORT du 8 novembre (Ollama) | mis à jour, rubriques de la phase H |

- Plan : (1) override et `installer.sh` rebranchés sur `llm-central` (clé lue dans `.env` par `--env-file`, jamais recopiée dans `donnees/`), `configurer.py` en mode `central`, ménage des anciennes configurations ; (2) vérification minimale, ports, embeddings reconstruits ; (3) banc avec `chat` ; (4) carte de l'interface (Playwright) ; (5) chapitres de la partie 1 un par un, captures annotées ; (6) annexes à partir des documents existants ; (7) relectures novice et adversariale, rapport, README, commit final.
- Décision prudente : RAGFlow (`rag-ragflow-*`, autre dépôt, peut-être utilisé par une autre session) laissé en marche ; 19 Go de RAM disponibles suffisent pour Open Notebook (moins de 1 Go mesuré).

### 2026-11-12 10:55 — Service central branché, banc rejoué, manuel en cours

- Fait : override, `compose.sh`, `installer.sh`, `configurer.py` rebranchés sur `llm-central` (OpenAI Compatible, `chat`, `embed`, `transcribe` ; TTS seul sur `rag-speaches`) ; anciennes configurations Ollama/vLLM retirées ; juge du banc adapté (`chat`, réflexion coupée) ; diagnostic adapté (`llm-*`, profil) ; sauvegarde, restauration et nettoyage sans l'image Ollama ; banc complet avec `chat` ; carte de l'interface (23 écrans) ; annexes A3 à A5 converties (sous-agent), A6 ; chapitres 01 à 05 et 13 rédigés ; scénarios Playwright des chapitres 02 à 12.
- Résultats : installation 42 s ; ports sur 127.0.0.1 ; banc `central-chat` 28/34 justes, 4/4 refus, médiane 8,7 s, p95 27,9 s, indexation 65 s ; reranker refusé par le code (« out of scope #1087 »).
- Constats d'interface : un nouveau document part au modèle par son seul aperçu (mode « aperçus ») ; choisir le modèle d'embedding ouvre une confirmation « Changement de modèle d'embedding » ; « Attribution automatique des défauts » répond « déjà configurés » quand l'ancien modèle par défaut a été supprimé ; un fichier déjà téléversé sous le même nom reçoit un suffixe « (1) » repris dans le titre lors d'un ajout groupé ; une source scannée en échec garde le titre « Processing... ».
- Suite : captures des chapitres 05 à 12, textes, bancs « Demander » et « aperçus », essai de contexte, exemples, sauvegarde, relectures.

### 2026-11-12 12:10 — Manuel au format du kit, démonstration, podcast

- Fait : captures à la souris des chapitres 02 à 12 (70 captures annotées, 23 de repérage) ; carnet « Démo Vélanor » créé par l'interface (10 sources, notes, quatre conversations dont trois cas pratiques) ; dépassement de contexte provoqué (texte de 80 000 caractères) ; podcast « Vélanor en bref » généré par l'interface (profils `duo-fr`, `court-fr`) ; manuel 01 à 13, annexes A1 à A6 et carte ; ancien manuel à plat retiré (contenu vérifié repris dans les annexes) ; présentation régénérée depuis le chapitre 01 ; README racine (sous-agent), index de la série, rapport.
- Résultats : dépassement → « ContextWindowExceededError … request (21842 … » (compteur 19,8 K) ; cas pratiques en aperçus incomplets, justes en contenu complet ; épisode MP3 d'environ 6 Mo, dialogue en français, chiffres justes ; `verifier_docs.py` à 0 point.
- Incidents : `networkidle` jamais atteint ; titres suffixés « (1) » ; carnet de démonstration recréé une fois (variable d'environnement non transmise au conteneur Playwright) ; scénarios rendus reprenables.
- Non fait (temps) : banc « Demander » et banc en aperçus complets sur le service central, exemples et sauvegarde rejoués ; inscrits dans « Ce qui reste ouvert ».
- Suite : relecture novice de la partie 1 jusqu'à zéro remarque, commit final.

### 2026-11-12 13:30 — Relecture novice et clôture de la reprise

- Fait : relecture novice de la partie 1 par dix sous-agents neufs successifs ; 66 remarques corrigées (dont neuf captures refaites : pastilles décalées par le défilement d'une zone, fenêtres plus hautes que l'écran, icône « Contexte » annotée, modes de contexte côte à côte) ; dixième passage : « Aucune remarque ». Téléchargement du fichier d'origine vérifié (HTTP 200, 53 745 octets).
- Résultat : `verifier_docs.py` à 0 point ; Open Notebook en marche sur http://127.0.0.1:8502 avec le carnet « Démo Vélanor » et le podcast « Vélanor en bref ».
- Reste ouvert : bancs « Demander » et « aperçus » complets, exemples et sauvegarde rejoués sur le service central, relecture adversariale des annexes réécrites (voir `RAPPORT-open-notebook.md`).

### 2026-11-13 — Uniformisation de la série

- `docs/README.md` remplacé par l'index commun aux cinq dépôts (Open Notebook, RAGFlow, AnythingLLM, Kotaemon, Open WebUI) : modèles utilisés, services déportables (OCR, audio, reranker), comparatif à deux lignes par solution (défaut, meilleur réglage). Chiffres repris des résultats bruts du 12 et du 13 novembre, aucun nouveau banc.
- README : section « Résultats » au même format que les autres dépôts, « Le parcours » placé juste après le sommaire.
- Annexes A1 à A3 renommées comme dans les autres dépôts (`A1-evaluation-qualite-et-performances`, `A2-choisir-son-materiel-et-ses-modeles`, `A3-automatiser-par-l-api`), liens mis à jour.
- `verifier_docs.py` : 0 point.

### 2026-11-13 — Index de la série : Docling déporté

- `docs/README.md` mis à jour : résultats des bancs Docling déporté de RAGFlow (34/34) et de Kotaemon (29/34).

### 2026-11-13 — Index de la série : procédures Docling déporté

- `docs/README.md` : colonne « Procédure dans le manuel » (Open WebUI chapitre 08, RAGFlow chapitre 06, Kotaemon chapitre 05).

### 2026-11-13 — Index de la série : comparatif complété

- Lignes « meilleur, Docling déporté » de RAGFlow et Kotaemon ajoutées au comparatif ; reranker de RAGFlow expliqué (essayé, sans gain) ; « Conventions » renommé « Étiquettes des annexes ».

### 2026-11-13 — Index de la série : contradictions levées

- Ligne « RAGFlow, meilleur, avec reranker » ajoutée au comparatif ; colonne « Effet du reranker mesuré au banc » ; résumé « En bref » et sens des colonnes ; Docling intégré possible seulement dans Kotaemon et Open Notebook (Open WebUI et RAGFlow : serveur à part uniquement, vérifié dans le code et les images).

### 2026-11-13 — Index de la série réécrit

- Solutions en colonnes, critères en lignes ; un tableau par sujet : PDF scanné (OCR et Docling), audio, reranker, résultats par cas, détail du meilleur réglage. Parcours de lecture et étiquettes retirés.

### 2026-11-13 — Index de la série : technologies et résultats séparés

- Tableaux OCR et Docling, audio, reranker : capacités seulement ; résultats déplacés dans « Résultats par cas » et « Détail du meilleur réglage » (scores par type de question). Cases vides quand la solution ne le fait pas.
