# A6. Rapport d'essais

> **Objet** : dire comment chaque information du manuel a été obtenue, et où se trouvent les preuves : scripts, résultats bruts, captures, journaux.
> **Prérequis** : aucun.
> **Version décrite** : Open Notebook 1.15.1 (`lfnovo/open_notebook:1.15.1@sha256:e4e18f12…95812`), SurrealDB v2.7.0 ; service LLM central de LLM-Service (branche `service-llamacpp`, profil `gpu`) : `chat` (Qwen3.5-4B), `embed` (bge-m3), `transcribe` (faster-whisper-small) ; synthèse vocale Speaches 0.8.3 (Kokoro) ; Playwright 1.64.1. Essais du 12 novembre 2026, et essais antérieurs des 8 et 9 novembre 2026 sur l'ancienne pile (Ollama puis vLLM).
> **Statut des informations** : [Vérifié] observé ou mesuré sur la machine d'essai, avec un renvoi au résultat brut ; [Source] documentation officielle ou code source au tag v1.15.1 ; [Estimation] calcul ou déduction non mesurés, avec leur base ; [À tester] non documenté et non essayé.
> **Précautions** : données fictives uniquement (corpus Vélanor) ; la clé du service central reste dans `.env`, jamais dans un résultat, un journal ou une capture (vérifié par recherche de la clé dans le dépôt avant chaque commit) ; les essais de l'ancienne pile ont été faits avec d'autres modèles et ne se comparent pas tels quels.

## Sommaire

1. [Méthode](#1-méthode)
2. [Machines et service de modèles](#2-machines-et-service-de-modèles)
3. [Essais du 12 novembre 2026](#3-essais-du-12-novembre-2026)
4. [Essais antérieurs (ancienne pile)](#4-essais-antérieurs-ancienne-pile)
5. [Captures d'écran](#5-captures-décran)
6. [Relectures](#6-relectures)
7. [Dépannage](#dépannage)
8. [Sources](#sources)

## 1. Méthode

- Rien n'est écrit de mémoire. Chaque procédure du manuel a été faite dans l'interface, à la souris, par un scénario Playwright ; chaque valeur vient d'un script de `outils/` dont la sortie brute est gardée dans `outils/resultats/`.
- Les étiquettes de la partie 2 : [Vérifié] (observé, avec renvoi), [Source] (lu dans la documentation ou le code au tag v1.15.1), [Estimation] (calcul, avec sa base), [À tester] (non essayé). La partie 1 n'en porte pas : elle ne reprend que ce qui a été vu pendant les essais, et renvoie ici pour les preuves.
- Commandes : [Testée] quand elles figurent dans un journal d'essai, [Aide] sinon.
- Avant chaque série d'essais qui interroge un modèle : `outils/communs/llm_central_sante.sh --essai` [Testée] ; sortie gardée en tête du journal d'essai.

## 2. Machines et service de modèles

| Élément | Valeur | Preuve |
|---|---|---|
| Machine d'exécution (12 novembre) | AMD Ryzen 5 9600X, 32 Go de RAM, RTX 4060 Ti 16 Go, Windows 11 + WSL2, Docker 29.9.3 [Vérifié] | [diagnostic](../../../outils/resultats/machine/diagnostic-2026-11-12.json) |
| Service LLM central | profil `gpu` : `llm-central` (LiteLLM v1.109.0), `llm-swap` (llama-swap v272, CUDA), `llm-speaches` (Speaches 0.8.3) ; noms fixes `chat`, `embed`, `rerank`, `transcribe` [Vérifié] | [diagnostic](../../../outils/resultats/machine/diagnostic-2026-11-12.json), [santé](../../../outils/resultats/open-notebook/essai-2026-11-12-banc-chat.log) |
| Versions | Open Notebook v1.15.1, dernière stable au 12 novembre ; SurrealDB v2.7.0 gardée (le compose officiel impose v2) [Vérifié] | [versions](../../../outils/resultats/open-notebook/versions-2026-11-12.json) |
| Projet | 41 884 étoiles, MIT, 114 commits sur 90 jours, 98 contributeurs [Vérifié] | [identité GitHub](../../../outils/resultats/open-notebook/identite-github-2026-11-12.json) |
| Machine des premiers essais (8 novembre) | Intel Core Ultra 7 255H, 15,3 Go de RAM dans WSL, sans GPU NVIDIA [Vérifié] | [diagnostic](../../../outils/resultats/machine/diagnostic-2026-11-08.json) |

## 3. Essais du 12 novembre 2026

| Essai | Script | Résultat principal | Preuve |
|---|---|---|---|
| Installation et branchement au service central | `outils/open-notebook/installer.sh`, `configurer.py` | 42 s, test de connexion réussi (« 9 models available »), modèles `chat`, `embed`, `transcribe` [Vérifié] | [journal](../../../outils/resultats/open-notebook/installation-2026-11-12.log), [configuration](../../../outils/resultats/open-notebook/configuration-2026-11-12.json) |
| Ports | `outils/open-notebook/verifier_ports.sh` | 8502 et 5055 sur `127.0.0.1` seulement, refusés sur l'adresse de WSL [Vérifié] | [ports](../../../outils/resultats/open-notebook/ports-2026-11-12.txt) |
| Vérification minimale | `outils/open-notebook/verif_minimale.py` | 401 sans mot de passe ; source indexée en 5,4 s ; réponse « 7 ans » citée en 9,9 s ; RAM de l'application 2,8 Go (Docling chargé) [Vérifié] | [résultat](../../../outils/resultats/open-notebook/verif-minimale-2026-11-12.json) |
| Reranker | `docker exec … grep rerank` | « Reranking is out of scope (#1087) » ; types de modèles acceptés : language, embedding, text_to_speech, speech_to_text [Vérifié] | [relevé](../../../outils/resultats/open-notebook/reranker-2026-11-12.txt) |
| Banc de 38 questions, `chat` | `outils/open-notebook/banc.py --etiquette central-chat --reindexer` | 28/34 justes, 4/4 refus, médiane 8,7 s [Vérifié] | [banc](../../../outils/resultats/open-notebook/banc-2026-11-12-central-chat.json), [journal](../../../outils/resultats/open-notebook/essai-2026-11-12-banc-chat.log) |
| Carte de l'interface | `outils/open-notebook/captures/carte.py`, `sonde.py` | 23 écrans relevés [Vérifié] | [relevés](../../../outils/resultats/open-notebook/captures/carte/) |
| Manuel à la souris | `outils/open-notebook/captures/manuel.py` | chaque chapitre de la partie 1 rejoué dans l'interface [Vérifié] | texte des pages dans `outils/resultats/open-notebook/captures/<chapitre>/` |

## 4. Essais antérieurs (ancienne pile)

Les essais des 8 et 9 novembre 2026 ont été faits avec Ollama sur processeur (qwen3:4b-instruct, bge-m3), puis vLLM sur carte graphique (Gemma 4 E4B, bge-m3), et Speaches pour la voix. Leurs résultats restent des preuves historiques : formats extraits avec et sans Docling, recherche plein texte et vectorielle, transformations, podcast, sauvegarde et restauration, MCP. Ils sont cités dans les annexes avec la mention « ancienne pile ». Liste complète et chronologie : `JOURNAL.md` et `outils/resultats/open-notebook/` (fichiers datés du 2026-11-08 et du 2026-11-09).

## 5. Captures d'écran

- Outil : `outils/communs/captures/annoter.py` (rectangle rouge, pastille numérotée, masque noir sur les secrets) ; navigateur Chromium 1440 × 900, langue fr-FR, dans le conteneur `mcr.microsoft.com/playwright/python:v1.64.1-noble` branché sur le réseau `rag-local` (`outils/communs/captures/lancer.sh`).
- Chaque capture du manuel est produite par une fonction de `outils/open-notebook/captures/manuel.py`, qui fait les clics et les saisies de l'étape ; le texte de la page est enregistré à côté de la capture.
- La clé du service central est saisie dans un champ masqué et recouverte d'un rectangle noir avant la capture (chapitre 03, étape 9).

## 6. Relectures

- Relecture novice de la partie 1 : dix lecteurs neufs successifs (sous-agents sans accès au logiciel ni aux annexes), 66 remarques corrigées au total, dont neuf captures refaites ; le dixième n'a fait « Aucune remarque » [Vérifié] (historique des commits du 12 novembre 2026).
- Relecture adversariale de la partie 2 : faite le 8 novembre sur l'ancien manuel (22 points) ; non refaite sur les annexes réécrites pendant la reprise [À tester]. Les liens et images sont contrôlés par `outils/communs/verifier_docs.py` (0 point).

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| Un lien de preuve ne s'ouvre pas | fichier renommé ou supprimé | `python3 outils/communs/verifier_docs.py` liste les liens cassés |
| Un résultat ne se reproduit pas à l'identique | le modèle `chat` ne répond pas deux fois exactement pareil | rejouer le banc ; comparer les synthèses, pas le mot à mot |

## Sources

- Mission et règles : `kit/PROMPT.md` (distribué à part), journal `JOURNAL.md`.
- Résultats bruts : `outils/resultats/open-notebook/`, `outils/resultats/machine/`.
