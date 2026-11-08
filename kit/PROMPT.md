# Mission : manuels vérifiés d'une solution de RAG local

> Ce fichier est générique. La solution à traiter, sa version, ses ports et ses particularités sont dans la fiche indiquée au lancement (`kit/fiches/NN-<solution>.md`). Ordre de priorité en cas de conflit : message de lancement (`/goal`), fiche, ce fichier, `CLAUDE.md`.

## 1. Objectif

Produire dans ce dépôt, pour la solution de la fiche, un ensemble de manuels pratiques en français : installation sous Windows 11 + WSL2, prise en main, usage avancé, qualité et performances, exploitation, dépannage. Public : celui de la fiche (par défaut : utilisateur technique à l'aise avec un terminal, pas forcément développeur).

Chaque affirmation des manuels est vérifiée par l'essai sur cette machine : commandes exécutées, code lancé, captures, mesures. Rien n'est écrit de mémoire.

À la fin, la solution reste installée et en marche sur `127.0.0.1`, avec un jeu de démonstration chargé, pour que l'utilisateur l'ouvre dans son navigateur Windows et voie comment elle tourne.

Machine cible : Windows 11, WSL2 (Ubuntu), Docker Desktop avec backend WSL2 et intégration de la distribution activée. GPU NVIDIA facultatif : sans GPU, les modèles tournent sur CPU (LLM-Service, branche `service-ollama`) ; avec GPU, sur vLLM (branche `service-vllm`). La session tourne dans WSL, à la racine de ce dépôt. Les interfaces s'ouvrent depuis le navigateur Windows sur `127.0.0.1`.

Cible matérielle : machines normalement dimensionnées, avec des petits modèles (SLM).

| Profil | Machine | Statut |
|---|---|---|
| A | PC portable sans GPU NVIDIA (Intel Core Ultra 7 255H, 15,3 Go de RAM dans WSL) | mesuré si c'est la machine d'exécution |
| B | Ryzen 5 9600X, RTX 4060 Ti 16 Go | mesuré si c'est la machine d'exécution, sinon [Estimation] à partir des mesures du profil A |

Les manuels donnent pour chaque profil : modèles, taille de contexte, réglages de la solution qui tiennent dans la mémoire.

## 2. Mode de travail autonome

Personne ne répond pendant l'exécution.

- **Ne jamais poser de question ni attendre une réponse.** Quand une décision sort de l'enveloppe ci-dessous, choisir l'option la plus prudente qui permet de continuer, l'écrire dans « Décisions en attente » (`docs/<solution>/README.md` et `JOURNAL.md`), puis avancer.
- **Bloquant réel** (Docker absent, LLM-Service introuvable, disque insuffisant, RAM insuffisante après les réductions prévues par la fiche) : l'absence de GPU n'est pas un bloquant. Dans ce cas, écrire `RAPPORT-<solution>.md` avec le diagnostic et ce que l'utilisateur doit corriger, committer, s'arrêter.
- **Enveloppe autorisée :**
  - images Docker officielles : celles du docker-compose officiel de la solution, `ghcr.io/speaches-ai/speaches`, `mcr.microsoft.com/playwright/python`, et les images de services annexes citées dans la fiche ; toujours à leur dernière version stable (§4, « Versions ») ;
  - LLM-Service : démarrage, ajout de modèles par `ollama pull` dans `ollama-central`, fichiers locaux non suivis (`.env`, `docker-compose.override.yml`) ; jamais de modification de ses fichiers suivis par git ;
  - téléchargement de modèles seulement s'ils manquent, dans la limite fixée au lancement (modèles Ollama et modèles propres à la solution, par exemple OCR) ;
  - paquets PyPI ou npm installés dans `.venv/` ou `node_modules/` du dépôt ;
  - comptes locaux dans l'outil testé, avec des identifiants fictifs rangés dans `donnees/IDENTIFIANTS-LOCAUX.txt` ;
  - commits git locaux.
- **Hors enveloppe, jamais :** `sudo` ; `pkill -f` ou `killall` (un motif peut tuer le shell de l'agent : arrêter par `docker stop` ou par un PID enregistré) ; modification de Windows ou de WSL hors du dépôt (`.wslconfig`, pilotes, services système, `sysctl`) ; `git push` ; création de compte en ligne ; clé d'API payante ; dépense ; port publié ailleurs que sur `127.0.0.1` ; suppression hors du dépôt et des ressources Docker préfixées `rag-` ; `docker system|volume|image prune` ; installation par `curl … | bash` ; mise à jour automatique (Watchtower ou équivalent).
- **Ressources Docker :** projet compose nommé `rag-<solution>` ; conteneurs, volumes et réseaux préfixés `rag-` ; données persistantes dans `donnees/<solution>/` (ignoré par git).
- **Journal :** `JOURNAL.md` à la racine, complété à la fin de chaque étape : date et heure, phase, ce qui a été fait, résultat, fichiers touchés, prochaine étape. Après une compaction, une reprise (`claude --continue`) ou un doute : relire `JOURNAL.md`, la fiche et ce fichier avant toute action. Ne jamais refaire une étape déjà committée sans raison écrite au journal.
- **Contexte :** confier à des sous-agents les lectures volumineuses (documentation complète, code source, longs journaux) et ne garder que leur synthèse. Les résultats bruts vont dans des fichiers, jamais recopiés en entier dans la conversation.
- **Temps :** un essai qui tourne plus de 30 minutes sans progrès est arrêté, consigné tel quel comme comportement observé, puis contourné.
- **Mémoire :** un seul essai lourd à la fois (indexation, banc, captures, génération de podcast) ; `free -m` relevé avant chacun ; les autres solutions du banc arrêtées avant de démarrer celle-ci (`outils/<solution>/arreter.sh`). Sous 2 Go disponibles, l'essai en cours est arrêté et consigné : une saturation de WSL coupe la session pendant de longues minutes.
- **Docker Compose :** si `docker compose version` échoue (greffon de Docker Desktop cassé dans WSL), utiliser `/usr/libexec/docker/cli-plugins/docker-compose` et le noter au journal.

## 3. Arborescence

```text
.
├── CLAUDE.md                      # règles permanentes (court)
├── JOURNAL.md                     # avancement, pour reprendre après interruption
├── README.md                      # présentation de la série de manuels
├── RAPPORT-<solution>.md          # bilan de fin de mission, un par solution
├── kit/                           # ce prompt et les fiches (ne pas modifier, sauf erreur factuelle notée au journal)
├── docs/
│   ├── README.md                  # index général de la série et comparatif du banc
│   ├── glossaire.md               # partagé par toutes les solutions
│   └── <solution>/
│       ├── README.md              # index de la solution
│       ├── plan-des-manuels.md
│       ├── NN-titre.md
│       └── img/<manuel>/
├── outils/
│   ├── README.md
│   ├── communs/                   # diagnostic, LLM-Service, voix, versions, corpus, banc, captures, vérification, nettoyage
│   ├── <solution>/                # installer, démarrer, arrêter, état, essais
│   └── resultats/
│       ├── machine/
│       ├── socle/
│       └── <solution>/
├── corpus/                        # documents fictifs et questions de référence, partagés
├── exemples/<solution>/           # NN_*.py ou NN_*.sh, et sorties_verifiees.txt
└── donnees/                       # volumes, identifiants locaux (ignoré par git)
```

## 4. Déroulé

Chaque phase se termine par une entrée au journal et un commit.

### Phase A. Diagnostic de la machine (à chaque solution, rapide)

`outils/communs/diagnostic.sh` écrit `outils/resultats/machine/diagnostic-<date>.json` :

- versions de Windows et de WSL (`wsl.exe --version` si accessible), distribution, noyau ;
- CPU, RAM visible dans WSL, swap, disque libre du dépôt et de Docker ;
- GPU, VRAM, pilote (`nvidia-smi`) ; test GPU dans un conteneur (`--gpus all`) ; sans GPU, le noter et continuer sur CPU ;
- processeur hybride (cœurs performants et cœurs économes) : nombre de fils de calcul d'Ollama (`LLAMA_ARG_THREADS` dans `ollama-central`, 8 sur la machine A ; sans ce réglage, 0,4 jeton/s au lieu de 16) ;
- `vm.max_map_count` de la VM de Docker (lecture seule, avec une image déjà présente : `docker run --rm --entrypoint cat <image> /proc/sys/vm/max_map_count` ; 262144 sur la machine A) ;
- versions de Docker et Compose, et santé du greffon `docker compose` ;
- LLM-Service : branche, image d'Ollama (comparée à la dernière stable par `outils/communs/versions.py`), modèles présents, `OLLAMA_CONTEXT_LENGTH`, fils de calcul ;
- accès sortant aux registres (Docker Hub, ghcr.io, PyPI, ollama.com) ;
- accès depuis WSL à un port publié par Docker sur `127.0.0.1`.

Comparer aux besoins de la fiche. Un manque bloquant déclenche l'arrêt décrit au §2.

### Phase B. Socle commun (repris, pas reconstruit)

Le socle (service de modèles, voix, corpus, questions, banc, outils) est repris du banc précédent pour que les mesures restent comparables. Ne jamais écraser les résultats d'une solution précédente ; versionner par date. Le reconstruire seulement s'il manque, et le noter au journal.

1. **Service de modèles : LLM-Service, jamais un serveur propre à la solution.** Les modèles de chat et d'embedding sont servis par le dépôt séparé LLM-Service (`~/Projets/Projet-IA/LLM-Service`), partagé par toutes les applications. Aucune solution n'embarque ni ne lance son propre Ollama ou vLLM ; si son compose officiel en contient un, l'override le retire.

   | Machine | Branche de LLM-Service | Conteneurs | Adresse vue par l'application (réseau `llm-net`) |
   |---|---|---|---|
   | sans GPU NVIDIA | `service-ollama` (sur CPU : `docker-compose.override.yml` local qui retire la réservation de GPU, fige l'image d'Ollama et fixe `LLAMA_ARG_THREADS`) | `ollama-central` (chat et embedding) | `http://ollama-central:11434` (fournisseur Ollama) ou `http://ollama-central:11434/v1` (compatible OpenAI) |
   | avec GPU NVIDIA | `service-vllm` | `vllm-central` (chat), `vllm-embed` (embedding) ; un serveur vLLM ne sert qu'un modèle | `http://vllm-central:8000/v1`, `http://vllm-embed:8000/v1` |

   - Démarrage et contrôle : `outils/communs/llm_service.sh`. Ne jamais arrêter ni supprimer LLM-Service depuis ce dépôt (`arreter.sh`, `nettoyer.sh`) : d'autres applications l'utilisent.
   - Le conteneur de l'application rejoint le réseau externe `llm-net` (en plus de `rag-local` pour la voix).
   - Modèles fixés pour toute la série : qwen3:4b-instruct (réponses), bge-m3 (embedding), ministral-3:3b (second modèle du banc). Ne pas en changer sans raison écrite au journal : la comparaison entre solutions en dépend.
   - Même taille de contexte pour toutes les applications et pour le juge du banc (`num_ctx` 16384, `OLLAMA_CONTEXT_LENGTH=16384` dans le `.env` de LLM-Service) : avec Ollama, deux tailles différentes forcent un rechargement du modèle à chaque alternance. Vérifier au cadrage comment la solution fixe `num_ctx` ; si elle le fait varier, passer par le fournisseur compatible OpenAI (`/v1`), qui garde le contexte du serveur.
   - Reranker : Ollama n'en sert pas. Une solution qui en utilise un garde son reranker intégré, documenté comme tel ; sinon le banc se fait sans reranker et le reranking est noté [À tester] ; avec `service-vllm`, un conteneur reranker peut être ajouté à LLM-Service.
   - Voix (transcription, synthèse) : serveur commun `rag-speaches` (`outils/communs/voix.sh`, `http://rag-speaches:8000/v1`, réseau `rag-local`).
   - Mesures du service de modèles : reprises de `outils/resultats/socle/` ; ne les refaire que si la version d'Ollama ou les modèles changent (`outils/communs/mesure_modeles.py`).
2. **Inventaire** (`outils/communs/inventaire_modeles.py`) seulement si un modèle manque dans LLM-Service : chercher d'abord dans `~/.ollama`, `~/.cache/huggingface/hub`, `/mnt/c/Users/*/.ollama/models`, `/mnt/c/Users/*/.cache/huggingface/hub`, et copier plutôt que télécharger.
3. **Contexte.** Budget de prompt de la solution : taille des passages × nombre de passages + historique + réponse, à faire tenir dans 16 384 jetons. Provoquer volontairement un dépassement, consigner l'erreur obtenue et la documenter dans le Dépannage.
4. Corpus fictif (repris tel quel, empreintes vérifiées contre `corpus/MANIFEST.json`) généré par `outils/communs/generer_corpus.py` (graine fixe, empreintes SHA-256 dans `corpus/MANIFEST.json`). Une entreprise fictive cohérente, avec au moins :
   - un rapport PDF texte d'une dizaine de pages, avec tableaux et chiffres ;
   - un PDF scanné (pages rendues en image, légère rotation, bruit) ;
   - une procédure DOCX, une présentation PPTX, un classeur XLSX ;
   - une page HTML, une note Markdown ;
   - un document en anglais ;
   - un fichier audio court si la fiche couvre l'audio (synthèse vocale locale ; à défaut, ignoré et noté).
5. Questions de référence `corpus/questions.json` (au moins 30) : question, réponse attendue (valeur exacte ou mots-clés), document et page sources, type (fait simple, tableau, scan, multi-documents, anglais, question piège sans réponse dans le corpus).
6. Banc `outils/communs/banc/` : une interface commune (indexer le corpus, poser une question, récupérer la réponse et les citations), un adaptateur par solution via son API. Métriques :
   - exactitude (correspondance avec la réponse attendue ; jugement par LLM local en complément, signalé comme tel) ;
   - citation correcte (bon document, et bonne page si la solution l'expose) ;
   - refus correct sur les questions pièges ;
   - latence p50 et p95, temps d'indexation, RAM de l'application seule (`docker stats`, hors conteneurs de modèles), pic de VRAM (`nvidia-smi`) s'il y a un GPU.

   Sortie en JSON et en tableau Markdown.
7. Captures : Playwright exécuté dans le conteneur officiel `mcr.microsoft.com/playwright/python` (version figée), branché sur le réseau `rag-local`, scripts dans `outils/communs/captures/`. Rien à installer sur WSL.
8. `outils/communs/verifier_docs.py` (règles du §7).
9. `outils/communs/nettoyer.sh <solution>` : arrête et supprime uniquement les ressources `rag-<solution>` ; option `--socle` pour le serveur de voix ; LLM-Service n'est jamais touché. Ce script n'est jamais lancé automatiquement en fin de mission.

### Phase C. Cadrage

- Lire la documentation officielle, le dépôt au tag choisi, le changelog et les notes de version (via sous-agent).
- **Versions : toujours la dernière version stable.** Pour la solution et pour chaque image ou dépendance, relever la dernière version stable avec `outils/communs/versions.py <solution> <dépôt>=<version> …` (préversions exclues : `rc`, `beta`, `alpha`, `dev`, `nightly`, et jamais l'étiquette `latest`) ; résultat brut gardé dans `outils/resultats/<solution>/versions-<date>.json`. Figer chaque image par étiquette exacte et empreinte `@sha256`.
  - Images annexes du compose officiel (base de données, moteur de recherche, stockage) : garder la version que le compose impose au tag choisi (compatibilité), noter à côté la dernière stable, ne jamais monter une version sans essai ; l'écart est justifié dans le JSON (`--raison`).
  - Paquets clients (SDK) : même version que le serveur.
  - LLM-Service : si l'image d'Ollama n'est plus la dernière stable, la mettre à jour dans l'override local (étiquette et empreinte) et rejouer `outils/communs/llm_service.sh` ; si les mesures du socle changent, les refaire et le noter.
- Relire le docker-compose, les scripts d'installation et tout composant tiers avant de les lancer. Consigner ce qui a été relu et les points relevés dans `outils/resultats/<solution>/relecture.md`.
- Inventorier la surface publique : interface, API, réglages, variables d'environnement, formats acceptés, fournisseurs de modèles.
- Écrire `docs/<solution>/plan-des-manuels.md` à partir du plan type (§5) et des thèmes de la fiche. Pas d'attente d'accord : le plan est committé puis suivi ; les écarts ultérieurs sont notés.

### Phase D. Installation testée

Script rejouable et idempotent `outils/<solution>/installer.sh` :

1. récupération à la version figée ;
2. fichier d'override compose : ports sur `127.0.0.1`, réseaux `rag-local` et `llm-net`, volumes dans `donnees/<solution>/`, secrets générés localement ;
3. démarrage et attente de l'état sain ;
4. branchement à LLM-Service (réseau `llm-net` ; fournisseur Ollama, « OpenAI-compatible » ou vLLM natif selon la branche) ;
5. création du compte local et des clés d'essai ;
6. vérification fonctionnelle minimale : import d'un document, une question, une citation affichée.

Vérifier par un test consigné que chaque port publié est lié à `127.0.0.1` (`docker ps --format '{{.Names}} {{.Ports}}'`). Mesurer la durée, la taille des images, le disque occupé, et la RAM de chaque service de l'application, au repos et pendant une indexation, séparément des conteneurs de modèles. Le manuel d'installation explique ce qui consomme la mémoire. Écrire aussi `demarrer.sh`, `arreter.sh` et `etat.sh`. Chaque erreur rencontrée est gardée dans `outils/resultats/<solution>/installation-*.log` et alimente le Dépannage.

### Phase E. Essais et rédaction, manuel par manuel

Pour chaque manuel du plan, dans l'ordre :

1. script(s) d'essai dans `outils/<solution>/`, résultats bruts dans `outils/resultats/<solution>/` ;
2. captures dans `docs/<solution>/img/<manuel>/`, numérotées ; une figure annotée est suivie d'un tableau N° | Élément | Rôle ;
3. rédaction à partir des seuls résultats bruts ; chaque valeur mesurée renvoie au script et au fichier de résultat qui l'ont produite ;
4. exemples courts dans `exemples/<solution>/NN_*.py` ou `.sh`, avec le moins de dépendances possible, exécutés, sortie réelle ajoutée à `exemples/<solution>/sorties_verifiees.txt` ;
5. mise en cohérence : index, plan, glossaire, renvois croisés, « Ce qui reste ouvert » ;
6. `verifier_docs.py` à 0 point, puis commit.

### Phase F. Banc qualité et performances

1. Écrire l'adaptateur de la solution et indexer le corpus complet.
2. Passer les questions avec le modèle principal, puis le second modèle s'il existe.
3. D'abord avec les réglages par défaut, puis avec un ou deux réglages recommandés par la documentation (découpage, top-k, reranking, recherche hybride).
4. Résultats dans `outils/resultats/<solution>/banc-<date>.json`, puis manuel « Qualité et performances ».
5. Mettre à jour `docs/README.md` : tableau comparatif des solutions déjà passées au banc (mêmes questions, même modèle, même machine), à partir de `outils/resultats/*/banc-*.json` (`outils/communs/banc/tableau.py`) ; chaque solution précédente renvoie à son dépôt GitHub (`https://github.com/floSa/<Solution>-Test-Bench`).

### Phase G. Profils matériels

1. Rejouer le banc avec le réglage de contexte le plus serré qui tient le corpus et noter la perte de qualité (le juge du banc garde le même `num_ctx` que la solution).
2. **Deux configurations minimales, mesurées autant que possible, à faire figurer dans la présentation de la solution (`docs/<solution>/presentation.md`) et dans « Qualité et performances »** :
   - **sans GPU** : processeur (nombre de cœurs ; nombre de fils de calcul d'Ollama si le processeur est hybride), RAM, disque, modèle de réponse le plus léger qui garde l'exactitude du banc, modèle d'embedding, taille de contexte ;
   - **avec GPU NVIDIA** : mémoire de la carte, mêmes rubriques, branche `service-vllm` de LLM-Service ;
   - pour chacune, en langage courant : la mémoire consommée (modèles, application, options comme l'OCR), le volume de documents utilisable (pages, caractères, nombre de documents selon la façon dont la solution les envoie au modèle) et le temps d'attente correspondant (première question, questions suivantes, indexation).
   Essayer au moins un modèle plus léger que le modèle principal (moins de 3 milliards de paramètres) pour situer le plancher de qualité. Mêmes modèles et même taille de contexte que les solutions déjà passées, pour que la comparaison tienne.
3. Écrire, dans le manuel « Qualité et performances », un tableau par profil : modèles, taille de contexte, réglages du service de modèles (sans GPU : fils de calcul, requêtes simultanées ; avec GPU : `--max-model-len`, `--gpu-memory-utilization`), réglages de la solution, résultats du banc. Les valeurs non mesurées sur la machine d'exécution sont marquées [Estimation] avec leur calcul.

### Phase H. Clôture

1. **Relecture adversariale** par un sous-agent neuf, qui n'a pas écrit les manuels : chaque affirmation [Vérifié] a-t-elle un résultat brut ? chaque commande [Testée] figure-t-elle dans un journal d'essai ? chaque lien et chaque image existent-ils ? Corriger les écarts en requalifiant ([Source], [À tester]) plutôt qu'en supprimant.
2. **Nettoyage** des artefacts d'essai (conversations de test, fichiers temporaires), sans toucher au jeu de démonstration.
3. **Jeu de démonstration** : un carnet ou espace « Démo » avec le corpus indexé et trois conversations exemples avec citations.
4. **Solution laissée en marche.** Vérifier l'URL depuis WSL et noter celle à ouvrir dans le navigateur Windows.
5. **`RAPPORT-<solution>.md`** :
   - ce qui a été installé (versions, images, modèles) ;
   - où ouvrir la solution, avec renvoi vers `donnees/IDENTIFIANTS-LOCAUX.txt` ;
   - manuels écrits (liens) ;
   - résultats du banc en cinq lignes ;
   - ce qui a été vérifié, ce qui ne l'a pas été et pourquoi ;
   - incidents rencontrés ;
   - décisions en attente ;
   - disque, RAM et VRAM occupés ;
   - comment tout arrêter ou tout supprimer ;
   - proposition pour la solution suivante.
6. `verifier_docs.py` à 0 point, commit final, `git status` propre.

## 5. Plan type des manuels

À adapter à la solution ; les thèmes 03 et suivants viennent de la fiche.

| N° | Manuel | Contenu |
|---|---|---|
| 00 | Notions fondamentales | RAG, embeddings, découpage, recherche hybride, reranking, citations ; architecture de la solution (schéma des services et des ports) |
| 01 | Installation sous Windows et WSL2 | prérequis mesurés, branchement à LLM-Service, mémoire consommée par l'application seule, installation, ports, premier démarrage, mise à jour, désinstallation complète |
| 02 | Prise en main | du premier import à la première réponse citée |
| 03 et suivants | Un manuel par thème de la fiche | fonctions majeures de la solution |
| avant-dernier − 2 | Recettes | cas d'usage complets, de bout en bout |
| avant-dernier − 1 | Qualité et performances | résultats du banc, réglages qui changent le résultat, profils matériels, taille de contexte |
| avant-dernier | Exploitation | sauvegarde et restauration, mise à jour, journaux, sécurité, multi-utilisateur, API |
| dernier | Dépannage et FAQ | tiré des échecs réels |

## 6. Gabarit d'un manuel (`docs/<solution>/NN-titre.md`)

En-tête en citation :

> **Objet** : ce que le manuel apprend.
> **Prérequis** : manuels à lire avant (liens).
> **Version décrite** : version exacte, OS, service de modèles (LLM-Service, Ollama ou vLLM et sa version, modèles, taille de contexte).
> **Statut des informations** : [Vérifié] observé ou mesuré le {date} sur {machine} ; [Source] documentation officielle ou code source ; [Estimation] calcul non mesuré ; [À tester] non documenté et non essayé.
> **Précautions** : données fictives, dossiers de test dédiés, ce qui a été relu avant installation.

Puis :

- `## Sommaire` avec ancres ;
- des sections numérotées `## N. Titre`, chacune découpée en `### Essentiel` (ce qu'il faut savoir et faire) et `### Pour aller plus loin` (détails, cas limites, mesures) ;
- les commandes portent [Testée] ou [Aide] (lue dans l'aide seulement) ;
- `## Dépannage` : tableau Symptôme | Cause probable | Action, tiré de ce qui a réellement échoué pendant les essais ;
- `## Sources` : liens officiels, versions des paquets et des images, scripts et résultats du dépôt.

Un risque (perte de données, exposition réseau, réglage dangereux, bogue) est signalé en tête du manuel concerné, juste après l'en-tête.

## 7. Fichiers transverses

- `README.md` (racine) : au format des autres bancs d'essai de `~/Projets/Tutoriels` (modèles : `kit/modeles/README-exemple.md`, et `~/Projets/Tutoriels/OpenMetadata-Test-Bench/README.md`). Dans cet ordre : titre « <Solution> — banc d'essai et manuels vérifiés » ; une phrase en gras qui dit ce que fait l'outil et ce que contient le dépôt ; badges (Docker, solution et version, Ollama ou vLLM, Python, WSL2) ; un paragraphe de présentation ; `## Sommaire` ; `## Architecture` (tableau Service | Conteneur | Image | Rôle, schéma mermaid, réseaux) ; `## Démarrage` (prérequis, commandes, tableau Service | URL | Note) ; `## Configuration` (variables générées, écarts au compose officiel, réglages de LLM-Service) ; `## API / Endpoints` ; `## Tests` (commandes et sortie obtenue) ; `## Structure du projet` ; `## Licences & composants` (avec « Ce projet : MIT — Copyright (c) 2026 floSa ») ; `## Le parcours` (tableau des manuels « Ce qu'on saura faire » et parcours conseillés) ; `## Commandes utiles` ; `## Données du banc` ; `## Les pièges que ce banc documente` ; `## Résultats` ; `## Versions` ; `## Ressources`. Ajouter un fichier `LICENSE` (MIT, floSa).
- `docs/README.md` : index général. Tableau par solution : version décrite, date des essais, machine de test, langue de l'interface, lien vers l'index de la solution. Puis comparatif du banc, parcours de lecture conseillés, conventions (étiquettes).
- `docs/<solution>/presentation.md` : première page à lire, sans étiquettes ni renvoi à un concurrent, phrases courtes. Ce que fait la solution en six lignes ; pour qui (adapté, peu adapté) ; le projet (dépôt, licence, étoiles, activité relevés par `outils/communs/identite_github.py`) ; fonctions en Oui, Non ou Partiel avec la limite en une phrase, mêmes rubriques pour toutes les solutions (modèles d'IA, documents acceptés, recherche et réponses, production, installation et exploitation), termes techniques expliqués sur place ; matériel nécessaire (configurations minimales sans et avec GPU) ; résultats mesurés en cinq lignes. Modèle : `kit/modeles/presentation-exemple.md`.
- `docs/<solution>/README.md` : index de la solution. Tableau Version décrite / Date des essais / Machine / Langue de l'interface ; tableau des manuels (N°, lien, contenu) ; parcours de lecture ; limites connues ; « Ce qui reste ouvert » (non traité, décisions en attente, ménage à faire à la main, écarts de version).
- `docs/<solution>/plan-des-manuels.md` : une phrase par manuel, puis chaque section avec son contenu et un lien vers l'ancre.
- `docs/glossaire.md` : termes techniques définis simplement, avec la solution concernée quand un terme lui est propre.
- `outils/README.md` : principe de production et tableau Fichier | Rôle.
- `outils/communs/verifier_docs.py` : vérifie les liens et images relatifs, les ancres internes, la présence des étiquettes dans l'en-tête, et le ton (aucun « vous », « nous », « notre », « vos », aucun pictogramme ni émoji dans `docs/`). Affiche le nombre de points ; lancé avant chaque commit et corrigé jusqu'à 0 point.

## 8. Règles de rédaction et d'honnêteté

- Ton impersonnel, phrases courtes, vocabulaire simple. Les libellés de l'interface sont cités tels quels, dans la langue affichée.
- Ce qui n'a pas été exécuté est marqué [Source] ou [À tester] et listé dans les limites.
- Un échec ou un comportement surprenant (bogue, réglage sans effet, danger) est documenté tel quel, avec le journal qui le montre.
- Sécurité : relire le code d'un plugin, d'une extension ou d'un service tiers avant de l'installer. Données fictives uniquement. Les jetons et clés sont créés pour l'essai, floutés sur les captures et supprimés en fin de mission, sauf ceux nécessaires au jeu de démonstration (listés dans `donnees/IDENTIFIANTS-LOCAUX.txt`).
- Aucune exposition réseau : chaque port publié est lié à `127.0.0.1`, et c'est vérifié par un test consigné.

## 9. Git

- Commits en français, un par fonctionnalité, essai ou manuel (jamais un commit fourre-tout de fin de phase), préfixés par le périmètre : « Outils : … », « Socle : … », « <Solution> : résultats bruts … », « <Solution> : captures … », « <Solution> : manuel NN, … », « Index, plans et renvois : … », « Journal : … ».
- Aucun trailer Co-Authored-By et aucune mention d'outil dans les messages.
- `.gitignore` : `donnees/`, `.venv/`, `node_modules/`, fichiers de plus de 20 Mo.

## 10. Critère de fin

La mission est terminée quand toutes ces conditions sont remplies et montrées dans la conversation :

1. `RAPPORT-<solution>.md` existe et couvre les rubriques de la phase H ;
2. `python3 outils/communs/verifier_docs.py` affiche 0 point ;
3. `exemples/<solution>/sorties_verifiees.txt` contient la sortie de chaque exemple ;
4. au moins un fichier `outils/resultats/<solution>/banc-*.json` existe ;
5. l'URL de la solution répond depuis WSL (sortie de `curl` montrée) ;
6. chaque port publié est lié à `127.0.0.1` (sortie de `docker ps --format '{{.Names}} {{.Ports}}'` montrée) ;
7. `README.md` (format du §7), `LICENSE`, `docs/<solution>/presentation.md` (avec les deux configurations minimales) et `outils/resultats/<solution>/versions-*.json` existent ;
8. `git status` est propre après le commit final.
