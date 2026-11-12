# Rapport de mission : Open Notebook

Reprise du 12 novembre 2026 : dépôt mis au standard du kit (manuel en deux parties, captures annotées, carte de l'interface, service LLM central). Les essais des 8 et 9 novembre (Ollama, vLLM) restent des preuves historiques.

## 1. Ce qui a été installé

| Élément | Version | Image |
|---|---|---|
| Open Notebook | 1.15.1, dernière stable au 12 novembre 2026 | `lfnovo/open_notebook:1.15.1@sha256:e4e18f12653df5bf48674b7b187c4252be52238b4d706330fd30d9b177b95812` |
| SurrealDB | 2.7.0 (imposée par le compose officiel ; dernière stable 4.0.1) | `surrealdb/surrealdb:v2.7.0@sha256:e5d7387e3727bbe2f7cd6d869e48cd34777272258572ead37c9656b25f745723` |
| Synthèse vocale (podcasts) | Speaches 0.8.3, Kokoro-82M | `ghcr.io/speaches-ai/speaches:0.8.3-cpu` (`rag-speaches`) |
| Captures | Playwright 1.64.1 | `mcr.microsoft.com/playwright/python:v1.64.1-noble@sha256:330d401a…` |

Modèles : service LLM central de LLM-Service (branche `service-llamacpp`, profil `gpu`), fournisseur « OpenAI Compatible » `llm-central` à `http://llm-central:8080/v1` : `chat` = Qwen3.5-4B (réflexion activée, 16 384 jetons), `embed` = bge-m3 Q8_0, `transcribe` = faster-whisper-small. `rerank` n'est pas utilisable : Open Notebook n'accepte aucun reranker. Preuves : [versions](outils/resultats/open-notebook/versions-2026-11-12.json), [configuration](outils/resultats/open-notebook/configuration-2026-11-12.json), [diagnostic](outils/resultats/machine/diagnostic-2026-11-12.json).

## 2. Où ouvrir la solution

- Interface : `http://127.0.0.1:8502` dans le navigateur Windows ; API : `http://127.0.0.1:5055` (documentation sur `/docs`).
- Mot de passe : `donnees/IDENTIFIANTS-LOCAUX.txt` (fichier local, non publié).
- Jeu de démonstration : carnet « Démo Vélanor » (10 sources, notes, quatre conversations citées dont trois cas pratiques), créé à la souris par `outils/open-notebook/captures/manuel.py` ; podcast « Vélanor en bref ».

## 3. Manuel écrit

Page d'accueil : [docs/open-notebook/README.md](docs/open-notebook/README.md).

- Partie 1, manuel utilisateur ([manuel/](docs/open-notebook/manuel/)) : 01 Découvrir, 02 Installer, 03 Premiers pas, 04 Première question, 05 Sources, 06 Discuter, 07 Notes et transformations, 08 Rechercher et demander, 09 Podcast, 10 Régler, 11 Cas pratiques, 12 En cas de problème, 13 Glossaire.
- Partie 2, annexes ([annexes/](docs/open-notebook/annexes/)) : A1 évaluation, A2 matériel, A3 API et MCP, A4 exploitation, A5 fonctionnement interne, A6 rapport d'essais, [carte de l'interface](docs/open-notebook/annexes/carte-interface.md).
- Captures annotées par chapitre : CAPTURES_A_COMPLETER

## 4. Banc en cinq lignes

- 38 questions, 9 documents, `chat` du service central, toutes les sources en contenu complet, Docling actif ([banc](outils/resultats/open-notebook/banc-2026-11-12-central-chat.json)).
- 28 réponses justes sur 34 ; les 6 erreurs viennent du contrat scanné (OCR inopérant).
- 4 refus corrects sur 4 pièges, aucune invention ; bon document cité 29 fois.
- Médiane 8,7 s, p95 27,9 s (réflexion de `chat`) ; indexation 65 s.
- Pas de reranker possible ; mêmes 28/34 que sur l'ancienne pile (Ollama CPU, vLLM GPU), modèles différents.

## 5. Vérifié, non vérifié

| Vérifié (12 novembre) | Non vérifié, et pourquoi |
|---|---|
| Installation, branchement au service central, ports sur 127.0.0.1, vérification minimale | Banc « Demander » complet sur le service central : une question essayée seulement (temps de mission) |
| Banc complet avec `chat` ; dépassement de contexte provoqué (erreur explicite) | Banc complet en mode aperçus : effet vu sur cinq questions |
| Chaque chapitre de la partie 1 rejoué à la souris, captures annotées | Profil sans carte graphique avec le service central : chiffres tirés des mesures de LLM-Service |
| Carte de l'interface (23 écrans), relecture novice de la partie 1 | Exemples de l'API et essai de sauvegarde : sorties de l'ancienne pile, non rejouées |

## 6. Incidents

- `networkidle` de Playwright jamais atteint (l'interface interroge l'API en continu) : attente du chargement puis d'un élément.
- Fichier déjà téléversé sous le même nom : suffixe « (1) » dans le titre ; le carnet de démonstration a été créé avant le carnet d'essai pour garder les noms.
- Choisir le modèle d'embedding ouvre une confirmation ; « Attribution automatique des défauts » répond « déjà configurés » quand l'ancien modèle par défaut a été supprimé.
- Les cas pratiques ont d'abord été joués avec les sources en aperçus : réponses incomplètes, rejoués en contenu complet ([preuve](outils/resultats/open-notebook/cas-pratiques-apercus-2026-11-12.json)).
- Scripts de sauvegarde, restauration et nettoyage : image Ollama de l'ancienne pile remplacée par l'image d'Open Notebook ; diagnostic et juge du banc adaptés au service central.

## 7. Décisions en attente

| N° | Décision | Option retenue | À trancher |
|---|---|---|---|
| D3 | OCR de Docling inopérant dans l'image 1.15.1 | conteneur non modifié ; scan documenté en échec | autoriser l'installation du moteur d'OCR dans le conteneur, ou signaler le défaut au projet |
| D5 | Réflexion de `chat` non réglable depuis Open Notebook | laissée par défaut | proposer dans LLM-Service un nom fixe sans réflexion ou un modèle plus léger |
| D6 | RAGFlow (`rag-ragflow-*`, autre dépôt) en marche pendant la mission | laissé en marche (peut servir à une autre session), mémoire suffisante | l'arrêter depuis son dépôt si inutile |
| D2 | Anciens conteneurs `rag-ollama`, `rag-agent-api`, `rag-frontend` d'un autre projet | non touchés | les supprimer à la main si inutiles |

## 8. Disque, RAM et VRAM

- Application : 2,8 Go de RAM au repos (Docling chargé), 4,7 Go en pointe de banc ([banc](outils/resultats/open-notebook/banc-2026-11-12-central-chat.json)).
- Service central (hors mission) : `llm-swap` 5,8 Go, `llm-central` 0,7 Go, `llm-speaches` 1,5 Go en pointe ; carte 8,4 Go sur 16, Windows compris.
- Disque : image Open Notebook 2,46 Go, SurrealDB 118 Mo, Speaches 2,1 Go ; cache Docling environ 6 Go dans `donnees/open-notebook/notebook_data/.cache`.

## 9. Arrêter ou supprimer

```bash
outils/open-notebook/arreter.sh
```

```bash
outils/communs/nettoyer.sh open-notebook
```

`arreter.sh --voix` arrête aussi le serveur de voix. `nettoyer.sh` supprime les conteneurs, le réseau et `donnees/open-notebook/` après confirmation ; le service LLM central n'est jamais touché.

## 10. Proposition pour la solution suivante

RAGFlow (fiche 02) : reprendre le corpus, le banc et les outils communs (`outils/communs/nouvelle_solution.sh`), et réutiliser dès le départ `annoter.py`, la session Playwright commune et le relevé de carte (`carte.py`, `sonde.py`), qui ont fait gagner le plus de temps ici.
