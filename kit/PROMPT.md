# Mission : manuels vérifiés d'une solution de RAG local

> Ce fichier est générique. La solution à traiter, sa version, ses ports et ses particularités sont dans la fiche indiquée au lancement (`kit/fiches/NN-<solution>.md`). Ordre de priorité en cas de conflit : message de lancement (`/goal`), fiche, ce fichier, `CLAUDE.md`.

## 1. Objectif

Produire dans ce dépôt, pour la solution de la fiche, un ensemble de manuels pratiques en français : installation sous Windows 11 + WSL2, prise en main, usage avancé, qualité et performances, exploitation, dépannage. Public : celui de la fiche (par défaut : utilisateur technique à l'aise avec un terminal, pas forcément développeur).

Chaque affirmation des manuels est vérifiée par l'essai sur cette machine : commandes exécutées, code lancé, captures, mesures. Rien n'est écrit de mémoire.

À la fin, la solution reste installée et en marche sur `127.0.0.1`, avec un jeu de démonstration chargé, pour que l'utilisateur l'ouvre dans son navigateur Windows et voie comment elle tourne.

Machine cible : Windows 11, WSL2 (Ubuntu), Docker Desktop avec backend WSL2 et intégration de la distribution activée, GPU NVIDIA. La session tourne dans WSL, à la racine de ce dépôt. Les interfaces s'ouvrent depuis le navigateur Windows sur `127.0.0.1`.

Cible matérielle : machines normalement dimensionnées, avec des petits modèles (SLM).

| Profil | Machine | Statut |
|---|---|---|
| A | Machine d'exécution (PC portable) | mesuré |
| B | Ryzen 5 9600X, RTX 4060 Ti 16 Go | mesuré si c'est la machine d'exécution, sinon [Estimation] à partir des mesures du profil A |

Les manuels donnent pour chaque profil : modèles, taille de contexte, réglages de la solution qui tiennent dans la mémoire.

## 2. Mode de travail autonome

Personne ne répond pendant l'exécution.

- **Ne jamais poser de question ni attendre une réponse.** Quand une décision sort de l'enveloppe ci-dessous, choisir l'option la plus prudente qui permet de continuer, l'écrire dans « Décisions en attente » (`docs/<solution>/README.md` et `JOURNAL.md`), puis avancer.
- **Bloquant réel** (Docker absent, GPU invisible depuis Docker, disque ou RAM insuffisants pour la fiche) : écrire `RAPPORT-<solution>.md` avec le diagnostic et ce que l'utilisateur doit corriger, committer, s'arrêter.
- **Enveloppe autorisée :**
  - images Docker officielles : celles du docker-compose officiel de la solution, `vllm/vllm-openai`, `ollama/ollama` (repli), `mcr.microsoft.com/playwright/python`, et les images de services annexes citées dans la fiche ;
  - lecture seule des modèles déjà présents sur la machine ; téléchargement de modèles seulement s'ils manquent, dans la limite fixée au lancement ;
  - paquets PyPI ou npm installés dans `.venv/` ou `node_modules/` du dépôt ;
  - comptes locaux dans l'outil testé, avec des identifiants fictifs rangés dans `donnees/IDENTIFIANTS-LOCAUX.txt` ;
  - commits git locaux.
- **Hors enveloppe, jamais :** `sudo` ; modification de Windows ou de WSL hors du dépôt (`.wslconfig`, pilotes, services système, `sysctl`) ; `git push` ; création de compte en ligne ; clé d'API payante ; dépense ; port publié ailleurs que sur `127.0.0.1` ; suppression hors du dépôt et des ressources Docker préfixées `rag-` ; `docker system|volume|image prune` ; installation par `curl … | bash` ; mise à jour automatique (Watchtower ou équivalent).
- **Ressources Docker :** projet compose nommé `rag-<solution>` ; conteneurs, volumes et réseaux préfixés `rag-` ; données persistantes dans `donnees/<solution>/` (ignoré par git).
- **Journal :** `JOURNAL.md` à la racine, complété à la fin de chaque étape : date et heure, phase, ce qui a été fait, résultat, fichiers touchés, prochaine étape. Après une compaction, une reprise (`claude --continue`) ou un doute : relire `JOURNAL.md`, la fiche et ce fichier avant toute action. Ne jamais refaire une étape déjà committée sans raison écrite au journal.
- **Contexte :** confier à des sous-agents les lectures volumineuses (documentation complète, code source, longs journaux) et ne garder que leur synthèse. Les résultats bruts vont dans des fichiers, jamais recopiés en entier dans la conversation.
- **Temps :** un essai qui tourne plus de 30 minutes sans progrès est arrêté, consigné tel quel comme comportement observé, puis contourné.

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
│   ├── communs/                   # diagnostic, socle, corpus, banc, captures, vérification, nettoyage
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
- GPU, VRAM, pilote (`nvidia-smi`) ; test GPU dans un conteneur (`--gpus all`) ;
- versions de Docker et Compose ;
- accès sortant aux registres (Docker Hub, ghcr.io, PyPI, ollama.com) ;
- accès depuis WSL à un port publié par Docker sur `127.0.0.1`.

Comparer aux besoins de la fiche. Un manque bloquant déclenche l'arrêt décrit au §2.

### Phase B. Socle commun (seulement s'il manque ou est incomplet)

Le socle sert à toutes les solutions. Ne jamais écraser les résultats d'une solution précédente ; versionner par date.

1. **Inventaire des modèles déjà présents** (`outils/communs/inventaire_modeles.sh`, résultat dans `outils/resultats/socle/modeles-existants.json`). Chercher au moins dans : le chemin donné au lancement (`MODELES_EXISTANTS`), `~/.cache/huggingface/hub`, `/mnt/c/Users/*/.cache/huggingface/hub`, `/mnt/c/Users/*/.lmstudio/models`, `/mnt/c/Users/*/.ollama/models`. Relever pour chacun : nom, format (safetensors, AWQ, GPTQ, GGUF), taille, type (chat, embedding, reranker). Ne rien modifier ni supprimer dans ces dossiers.
2. **Serveur de modèles : vLLM d'abord.** Réseau Docker `rag-local`. Image officielle `vllm/vllm-openai`, version figée. Trois conteneurs qui se partagent le GPU :

   | Conteneur | Rôle | Port |
   |---|---|---|
   | `rag-vllm-chat` | modèle de chat | `127.0.0.1:8000` |
   | `rag-vllm-embed` | modèle d'embedding (mode pooling ou embed selon la version) | `127.0.0.1:8001` |
   | `rag-vllm-rerank` | reranker, seulement s'il tient en mémoire | `127.0.0.1:8002` |

   - Monter les modèles existants en lecture seule. Si le chargement depuis `/mnt/c` est trop lent, copier dans un volume WSL (copie, pas téléchargement) et le mesurer.
   - Partager la VRAM avec `--gpu-memory-utilization` (somme des trois inférieure à 0,95). Fixer `--max-model-len`. Utiliser `--enforce-eager` si la mémoire manque.
   - Ollama (`ollama/ollama`, conteneur `rag-ollama`, `127.0.0.1:11434`) seulement en repli : modèle disponible uniquement en GGUF et refusé par vLLM, ou solution qui ne marche pas avec vLLM. Chaque repli est justifié dans le journal.
3. **Choix des modèles (SLM)**, justifié dans `outils/resultats/socle/modeles.json`. Priorité aux modèles déjà présents. Téléchargement seulement si rien ne convient, dans la limite fixée au lancement.
   - Chat : modèle instruct récent, bon en français, quantifié 4 bits (AWQ ou GPTQ) pour vLLM. Repères : environ 3 à 4 milliards de paramètres sous 8 Go de VRAM, 7 à 8 milliards sous 12 Go, jusqu'à 14 milliards avec 16 Go.
   - Embedding : multilingue, `BAAI/bge-m3` ou équivalent.
   - Reranker : `BAAI/bge-reranker-v2-m3` ou équivalent, s'il tient.
4. **Contexte.** Pour chaque profil, mesurer la plus grande `--max-model-len` qui démarre et tient en charge (deux requêtes simultanées). Déduire un budget de prompt : taille des passages × nombre de passages + historique + réponse. Chaque solution est ensuite réglée pour rester dans ce budget (taille de découpage, top-k, longueur d'historique). Provoquer volontairement un dépassement, consigner l'erreur obtenue et la documenter dans le Dépannage.
5. **Mesures du socle** (`outils/communs/mesure_modeles.py`) : débit en génération (jetons/s), temps du premier jeton, VRAM par conteneur, RAM, pour chaque modèle et chaque taille de contexte retenue.
6. Corpus fictif généré par `outils/communs/generer_corpus.py` (graine fixe, empreintes SHA-256 dans `corpus/MANIFEST.json`). Une entreprise fictive cohérente, avec au moins :
   - un rapport PDF texte d'une dizaine de pages, avec tableaux et chiffres ;
   - un PDF scanné (pages rendues en image, légère rotation, bruit) ;
   - une procédure DOCX, une présentation PPTX, un classeur XLSX ;
   - une page HTML, une note Markdown ;
   - un document en anglais ;
   - un fichier audio court si la fiche couvre l'audio (synthèse vocale locale ; à défaut, ignoré et noté).
7. Questions de référence `corpus/questions.json` (au moins 30) : question, réponse attendue (valeur exacte ou mots-clés), document et page sources, type (fait simple, tableau, scan, multi-documents, anglais, question piège sans réponse dans le corpus).
8. Banc `outils/communs/banc/` : une interface commune (indexer le corpus, poser une question, récupérer la réponse et les citations), un adaptateur par solution via son API. Métriques :
   - exactitude (correspondance avec la réponse attendue ; jugement par LLM local en complément, signalé comme tel) ;
   - citation correcte (bon document, et bonne page si la solution l'expose) ;
   - refus correct sur les questions pièges ;
   - latence p50 et p95, temps d'indexation, pic de VRAM (échantillonnage `nvidia-smi`), RAM de l'application seule (`docker stats`, hors conteneurs de modèles).

   Sortie en JSON et en tableau Markdown.
9. Captures : Playwright exécuté dans le conteneur officiel `mcr.microsoft.com/playwright/python` (version figée), branché sur le réseau `rag-local`, scripts dans `outils/communs/captures/`. Rien à installer sur WSL.
10. `outils/communs/verifier_docs.py` (règles du §7).
11. `outils/communs/nettoyer.sh <solution>` : arrête et supprime uniquement les ressources `rag-<solution>` ; option `--socle` pour vLLM et Ollama. Ce script n'est jamais lancé automatiquement en fin de mission.

### Phase C. Cadrage

- Lire la documentation officielle, le dépôt au tag choisi, le changelog et les notes de version (via sous-agent).
- Figer la version selon la règle de la fiche : numéro exact, date, empreinte des images.
- Relire le docker-compose, les scripts d'installation et tout composant tiers avant de les lancer. Consigner ce qui a été relu et les points relevés dans `outils/resultats/<solution>/relecture.md`.
- Inventorier la surface publique : interface, API, réglages, variables d'environnement, formats acceptés, fournisseurs de modèles.
- Écrire `docs/<solution>/plan-des-manuels.md` à partir du plan type (§5) et des thèmes de la fiche. Pas d'attente d'accord : le plan est committé puis suivi ; les écarts ultérieurs sont notés.

### Phase D. Installation testée

Script rejouable et idempotent `outils/<solution>/installer.sh` :

1. récupération à la version figée ;
2. fichier d'override compose : ports sur `127.0.0.1`, réseau `rag-local`, volumes dans `donnees/<solution>/`, secrets générés localement ;
3. démarrage et attente de l'état sain ;
4. branchement au socle (vLLM, fournisseur « OpenAI-compatible » ou fournisseur vLLM natif) ;
5. création du compte local et des clés d'essai ;
6. vérification fonctionnelle minimale : import d'un document, une question, une citation affichée.

Mesurer la durée, la taille des images, le disque occupé, et la RAM de chaque service de l'application, au repos et pendant une indexation, séparément des conteneurs de modèles. Le manuel d'installation explique ce qui consomme la mémoire. Écrire aussi `demarrer.sh`, `arreter.sh` et `etat.sh`. Chaque erreur rencontrée est gardée dans `outils/resultats/<solution>/installation-*.log` et alimente le Dépannage.

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
5. Mettre à jour `docs/README.md` : tableau comparatif des solutions déjà passées au banc (mêmes questions, même modèle, même machine).

### Phase G. Profils matériels

1. Rejouer le banc avec le réglage de contexte le plus serré (profil le plus petit) et noter la perte de qualité.
2. Écrire, dans le manuel « Qualité et performances », un tableau par profil : modèles, `--max-model-len`, `--gpu-memory-utilization`, réglages de la solution, résultats du banc. Les valeurs non mesurées sur la machine d'exécution sont marquées [Estimation] avec leur calcul.

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
| 01 | Installation sous Windows et WSL2 | prérequis mesurés, socle vLLM, mémoire consommée par l'application seule, installation, ports, premier démarrage, mise à jour, désinstallation complète |
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
> **Version décrite** : version exacte, OS, versions du socle (vLLM, modèles, taille de contexte).
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

- `README.md` (racine) : court et direct. Ce que contient la série, ce qu'on y apprend, un tableau « Objectif → Lire », l'arborescence, comment lancer un exemple. Ni détail de configuration ni mention superflue.
- `docs/README.md` : index général. Tableau par solution : version décrite, date des essais, machine de test, langue de l'interface, lien vers l'index de la solution. Puis comparatif du banc, parcours de lecture conseillés, conventions (étiquettes).
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

- Commits en français, un par étape, préfixés par le périmètre : « Outils : … », « Socle : … », « <Solution> : résultats bruts … », « <Solution> : captures … », « <Solution> : manuel NN, … », « Index, plans et renvois : … », « Journal : … ».
- Aucun trailer Co-Authored-By et aucune mention d'outil dans les messages.
- `.gitignore` : `donnees/`, `.venv/`, `node_modules/`, fichiers de plus de 20 Mo.

## 10. Critère de fin

La mission est terminée quand toutes ces conditions sont remplies et montrées dans la conversation :

1. `RAPPORT-<solution>.md` existe et couvre les rubriques de la phase H ;
2. `python3 outils/communs/verifier_docs.py` affiche 0 point ;
3. `exemples/<solution>/sorties_verifiees.txt` contient la sortie de chaque exemple ;
4. au moins un fichier `outils/resultats/<solution>/banc-*.json` existe ;
5. l'URL de la solution répond depuis WSL (sortie de `curl` montrée) ;
6. `git status` est propre après le commit final.
