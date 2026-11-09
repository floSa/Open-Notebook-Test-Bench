# 10. Qualité et performances

> **Objet** : mesurer la justesse des réponses, les citations, les refus et les temps de réponse d'Open Notebook sur un corpus de référence ; savoir quels réglages changent le résultat ; choisir modèles et contexte selon la machine.
> **Prérequis** : [04. Chat et citations](04-chat-et-citations.md), [06. Recherche](06-recherche.md).
> **Version décrite** : Open Notebook 1.15.1, Ollama 0.40.15 (essais du 8 novembre faits sur 0.30.7 ; banc de référence rejoué sur 0.40.15) sur CPU, qwen3:4b-instruct et ministral-3:3b (GGUF Q4_K_M), bge-m3, Docling 2.130.0 ; `num_ctx` 16384, 6144 et 4096 ; banc de 38 questions. Sur GPU : vLLM v0.29.0, Gemma 4 E4B (checkpoint officiel Google, QAT w4a16) et bge-m3, `max_model_len` 32768.
> **Statut des informations** : [Vérifié] observé ou mesuré le 2026-11-08 sur la machine d'essai (profil A : Intel Core Ultra 7 255H, 16 fils, 15,3 Go de RAM dans WSL, sans GPU NVIDIA) et le 2026-11-09 sur la machine de suite (profil B : Ryzen 5 9600X, RTX 4060 Ti 16 Go, WSL) ; [Source] documentation officielle ou code source au tag v1.15.1 ; [Estimation] calcul non mesuré ; [À tester] non documenté et non essayé.
> **Précautions** : corpus fictif Vélanor de 9 documents ([manifeste](../../corpus/MANIFEST.json)) et 38 questions ([questions](../../corpus/questions.json)) ; chaque banc dans `outils/resultats/open-notebook/banc-*.json`.

**Risque signalé.** Avec un petit modèle, une réponse affirmant qu'une information « n'est pas mentionnée » est souvent fausse quand le document existe mais n'a pas été lu (scan sans OCR, source hors contexte). Sur le banc avec qwen3:4b-instruct, toutes les erreurs restantes sont de ce type ; aucune réponse n'a inventé de chiffre [Vérifié]. La notation par mots-clés a aussi ses faux positifs : ministral-3:3b répond à Q24 « 1240 unités … supérieur au seuil d'alerte de 1500 », bons nombres mais conclusion fausse, comptée exacte [Vérifié].

## Sommaire

1. [Le banc](#1-le-banc)
2. [Résultats](#2-résultats)
3. [Réglages qui changent le résultat](#3-réglages-qui-changent-le-résultat)
4. [Taille de contexte](#4-taille-de-contexte)
5. [Profils matériels](#5-profils-matériels)
6. [Dépannage](#dépannage)
7. [Sources](#sources)

## 1. Le banc

### Essentiel

| Élément | Contenu |
|---|---|
| Corpus | rapport PDF de 10 pages avec tableaux, contrat PDF scanné, procédure DOCX avec tableau, présentation PPTX, classeur XLSX, page HTML, note Markdown, audit PDF en anglais, message audio MP3 |
| Questions | 38 : 13 faits simples, 10 tableaux, 4 sur le scan, 2 en anglais, 3 multi-documents, 2 sur l'audio, 4 pièges sans réponse dans le corpus |
| Mode | une session de chat par question dans le carnet « Banc », toutes les sources en « full content » (et un échantillon en « Demander ») |
| Exactitude | chaque élément attendu (valeur exacte ou mot-clé) présent dans la réponse ; un nombre ne doit pas être collé à d'autres chiffres |
| Refus | sur un piège, la réponse doit dire que l'information est absente |
| Citation | un `[source:…]` de la réponse désigne le document attendu ; pas de page (Open Notebook ne la fournit pas) |
| Complément | juge LLM local (qwen3:4b-instruct, réponse OUI ou NON), signalé comme tel |
| Mesures | latence par question (p50, p95), durée d'indexation, pic de RAM par conteneur (`docker stats`) ; VRAM par `nvidia-smi` en fin de banc sur le profil B (vLLM réserve sa VRAM au démarrage et la garde, une mesure suffit) |

Outils : `outils/communs/banc/commun.py` (notation, mesures), `outils/open-notebook/banc.py` (adaptateur par l'API REST) [Testée] :

```bash
python3 outils/open-notebook/banc.py --etiquette essai --reindexer
```

### Pour aller plus loin

La notation par mots-clés a d'abord compté juste une réponse qui disait « non mentionné » parce que « 8 » apparaissait dans « 87 » ; elle a été corrigée (bornes des nombres) et les bancs renotés sans relancer les questions (`outils/communs/banc/renoter.py`) [Vérifié]. Le juge LLM n'est pas fiable sur ce banc : il valide quatre réponses fausses (Q15, Q17, Q30, Q33) et en rejette une juste (Q03) dans le banc de référence ; il ne sert que de second avis [Vérifié].

## 2. Résultats

### Essentiel

Tableau produit par `outils/communs/banc/tableau.py` [Vérifié] :

| Banc | Mode | Modèle | Contexte | `num_ctx` | Docling | Exactes | Refus pièges | Bon document cité | p50 (s) | p95 (s) | Indexation (s) | Pic RAM application (Mo) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [defaut-qwen-fullcontent](../../outils/resultats/open-notebook/banc-2026-11-08-defaut-qwen-fullcontent.json) | chat | qwen3:4b-instruct | full content | 16384 | false | 25/34 | 4/4 | 26 | 10.81 | 23.83 | 70.0 | 976 |
| [docling-ministral-fullcontent](../../outils/resultats/open-notebook/banc-2026-11-08-docling-ministral-fullcontent.json) | chat | ministral-3:3b | full content | 16384 | true | 28/34 | 4/4 | 30 | 10.03 | 44.68 | - | 3207 |
| [docling-qwen-fullcontent-ctx4096](../../outils/resultats/open-notebook/banc-2026-11-08-docling-qwen-fullcontent-ctx4096.json) | chat | qwen3:4b-instruct | full content | 4096 | true | 0/34 | 0/4 | 0 | - | - | - | 2661 |
| [docling-qwen-fullcontent-ctx6144](../../outils/resultats/open-notebook/banc-2026-11-08-docling-qwen-fullcontent-ctx6144.json) | chat | qwen3:4b-instruct | full content | 6144 | true | 28/34 | 4/4 | 30 | 91.82 | 114.13 | - | 2555 |
| [docling-qwen-fullcontent](../../outils/resultats/open-notebook/banc-2026-11-08-docling-qwen-fullcontent.json) | chat | qwen3:4b-instruct | full content | 16384 | true | 28/34 | 4/4 | 28 | 9.05 | 23.79 | 125.6 | 3765 |
| [docling-qwen-fullcontent-ollama040](../../outils/resultats/open-notebook/banc-2026-11-08-docling-qwen-fullcontent-ollama040.json) | chat | qwen3:4b-instruct | full content | 16384 | true | 28/34 | 4/4 | 28 | 7.44 | 24.19 | 84.3 | 2989 |
| [gpu-vllm-docling](../../outils/resultats/open-notebook/banc-2026-11-09-gpu-vllm-docling.json) (profil B, GPU) | chat | gemma4:e4b (vLLM) | full content | 32768 | true | 28/34 | 4/4 | 24 | 1.86 | 4.59 | 70.1 | 7414 |
| [gpu-vllm-docling-demander](../../outils/resultats/open-notebook/banc-2026-11-09-gpu-vllm-docling-demander.json) (profil B, GPU) | ask (Demander) | gemma4:e4b (vLLM) | - | 32768 | true | 28/34 | 4/4 | 30 | 7.70 | 13.35 | - | 7210 |

Les latences du banc à 6144 ne sont pas représentatives : le juge LLM du banc appelle le même modèle à `num_ctx` 16384, ce qui oblige Ollama à recharger le modèle deux fois par question (38 chargements à 6144 dans le [journal d'Ollama](../../outils/resultats/socle/ollama-journal-extrait-2026-11-08.log)) et efface le cache de préfixe ; chaque question relit donc tout le prompt (87 à 148 s). Dans un usage normal, sans changement de `num_ctx` entre deux questions, les latences seraient proches de celles à 16384 [Estimation]. L'exactitude, elle, est mesurée sans biais [Vérifié].

Par type de question (qwen3:4b-instruct, `num_ctx` 16384) [Vérifié] :

| Type | Sans Docling | Avec Docling |
|---|---|---|
| fait simple | 13/13 | 13/13 |
| tableau | 9/10 | 10/10 |
| scan | 0/4 | 0/4 |
| anglais | 2/2 | 2/2 |
| multi-documents | 1/3 | 1/3 |
| audio | 0/2 | 2/2 |
| piège (refus correct) | 4/4 | 4/4 |

### Après passage sur LLM-Service

Banc complet rejoué sur Ollama 0.40.15, dernière version stable, servi par LLM-Service avec 8 fils de calcul (ligne `ollama040` du tableau) [Vérifié] : mêmes 28 réponses justes sur 34 et 4 refus sur 4, mêmes 6 erreurs (scan) ; médiane 7,4 s au lieu de 9,1 s ; indexation 84 s au lieu de 126 s.


Échantillon de 6 questions rejoué sur le service de modèles partagé, mêmes poids [Vérifié] ([banc](../../outils/resultats/open-notebook/banc-2026-11-08-llm-service-qwen-echantillon.json)) : mêmes réponses justes et fausses qu'avant (Q01, Q08, Q24, Q32 justes, Q35 refusée, Q18 fausse car issue du scan) ; temps de 8,6 à 20,4 s, 127 s pour la première question. Condition : 8 fils de calcul (`LLAMA_ARG_THREADS=8` dans LLM-Service) ; avec les 16 cœurs vus par WSL, la génération tombe à 0,4 jeton/s ([mesures](../../outils/resultats/socle/migration-llm-service-2026-11-08.txt)).

### Sur GPU (profil B, vLLM)

Même corpus, mêmes 38 questions, Docling actif, servi par LLM-Service branche `service-vllm` (Gemma 4 E4B, bge-m3) [Vérifié] : 28 réponses justes sur 34 et 4 refus sur 4, exactement les mêmes 6 erreurs qu'en CPU (le contrat scanné) ; médiane 1,86 s au lieu de 7,44 s ; p95 4,59 s au lieu de 24,19 s ; indexation 70,1 s au lieu de 84,3 s — l'indexation gagne peu, car elle est dominée par Docling (CPU), pas par le modèle. Le mode « Demander », abandonné sur CPU (section 3), devient utilisable : médiane 7,7 s, p95 13,4 s, mêmes 28/34 et 4/4 refus, plus de citations avec le bon document (30 contre 24 en chat, la recherche vectorielle cible mieux que l'envoi du document entier).

Écart au modèle prévu : la configuration GPU devait reprendre qwen3:4b-instruct en 4 bits (section 5, estimation antérieure), pour comparer au même modèle que sur CPU. Le service de modèles partagé (LLM-Service) avait déjà basculé, pour d'autres projets, sur Gemma 4 E4B (checkpoint officiel Google QAT w4a16, environ 11,5 Go, déjà en cache) : ce modèle a été repris tel quel plutôt que d'en télécharger un second rien que pour ce banc — l'architecture visée est un service de modèles partagé entre tous les projets, pas un modèle par solution testée. La comparaison CPU/GPU porte donc sur deux modèles différents de taille voisine (qwen3:4b-instruct contre Gemma 4 E4B), pas sur un même modèle à deux vitesses ; qwen3:4b-instruct en 4 bits sur vLLM reste [À tester].

VRAM : 15,7 Go sur 16,4 Go utilisés en fin de banc (Gemma 4 E4B + bge-m3, les deux chargés en permanence par vLLM) — tient sur une carte 16 Go mais avec peu de marge ; un modèle ou un contexte plus gros déborderait.

### Pour aller plus loin

- Les 6 erreurs restantes avec Docling viennent toutes du contrat scanné (4 questions directes, 2 multi-documents qui en dépendent) : l'OCR ne fonctionne pas dans l'image 1.15.1 ([03](03-carnets-sources-formats.md#3-docling--tableaux-et-ocr)).
- Les 4 pièges sont refusés par tous les modèles essayés, sans invention [Vérifié].
- Les questions en anglais et la question en français sur le document anglais sont justes [Vérifié].

## 3. Réglages qui changent le résultat

### Essentiel

| Réglage | Effet mesuré |
|---|---|
| Docling activé | +3 réponses exactes (tableau DOCX, deux questions audio grâce au contournement STT appliqué en même temps) ; indexation 70 s → 126 s ; RAM de l'application 1,0 Go → 3,8 Go en pointe |
| Contournement STT (`OPENAI_COMPATIBLE_BASE_URL_STT`) | le message audio devient lisible : 0/2 → 2/2 |
| Modèle ministral-3:3b au lieu de qwen3:4b-instruct | 28/34 selon la notation, 27/34 après relecture (Q24 fausse), médiane semblable, p95 presque doublé (44,7 s contre 23,8 s) |
| `num_ctx` 4096 | 0 réponse : le corpus (environ 4 230 jetons de prompt) dépasse le contexte, erreur à chaque question |
| `num_ctx` 6144 | même exactitude qu'à 16384 (28/34, 4/4 refus, aucune erreur de contexte) : le corpus entier tient ; latences faussées par le banc (voir section 2) |
| Mode « Demander » au lieu du chat, sur CPU | échantillon de 6 questions de 5 types (sans audio ni piège) : 1 juste, 1 refus à tort, 4 réponses vides ; 74 à 1 089 s par question ; banc complet abandonné ([journal](../../outils/resultats/open-notebook/essai-2026-11-08-banc-ask.log)) |
| Mode « Demander » au lieu du chat, sur GPU (profil B) | banc complet, utilisable : 28/34, 4/4 refus, médiane 7,7 s, p95 13,4 s ([résultat](../../outils/resultats/open-notebook/banc-2026-11-09-gpu-vllm-docling-demander.json)) |

Valeurs [Vérifié] : voir le tableau de la section 2.

### Pour aller plus loin

Réglages non essayés [À tester] : taille de découpage (`OPEN_NOTEBOOK_CHUNK_SIZE`), qui n'agit que sur la recherche et « Demander » ; mode « insights » sur des sources préalablement transformées (essai ponctuel défavorable dans [04](04-chat-et-citations.md#1-ce-que-le-chat-envoie-au-modèle)). Open Notebook 1.15.1 n'offre ni reranker ni recherche hybride [Source].

## 4. Taille de contexte

### Essentiel

Budget de prompt du chat de carnet = consignes du système (environ 1 150 jetons) + sources en « full content » + historique + question, plus la réponse à produire. Sur le corpus d'essai : 3 084 jetons de sources, environ 4 230 jetons de prompt au total [Vérifié] ([chat](../../outils/resultats/open-notebook/chat-2026-11-08.json), [erreurs à 4096](../../outils/resultats/open-notebook/banc-2026-11-08-docling-qwen-fullcontent-ctx4096.json)).

| `num_ctx` | Ce qui tient | RAM d'Ollama (2 requêtes simultanées, qwen3:4b-instruct) |
|---|---|---|
| 4096 | une ou deux sources courtes en « full content » | 7,3 Go |
| 6144 | le corpus d'essai entier, une question à la fois (banc sans erreur [Vérifié]) | entre 7,3 et 9,2 Go [Estimation] |
| 16384 | le corpus et une longue conversation | 11,4 Go |
| 32768 | tient en mémoire, mais 15 minutes avant le premier mot pour 16 000 jetons | 13,9 Go |

RAM [Vérifié] ([mesures du socle](../../outils/resultats/socle/mesures-2026-11-08-passe2.json), [passe 1](../../outils/resultats/socle/mesures-2026-11-08-passe1.log)).

### Pour aller plus loin

Le dépassement volontaire a été provoqué deux fois : par l'API `/api/generate` d'Ollama (troncature silencieuse, `truncated = 1`) et par le chat d'Open Notebook à 4096 (erreur 502 explicite) ; les deux sont documentés dans [Dépannage](12-depannage.md#3-chat-contexte-et-modèles) [Vérifié].

## 5. Profils matériels

### Essentiel

**Profil A, machine d'essai** (Intel Core Ultra 7 255H, 15,3 Go de RAM dans WSL, sans GPU NVIDIA) — mesuré :

| Élément | Réglage | Résultat |
|---|---|---|
| Serveur de modèles | LLM-Service, Ollama 0.40.15 sur CPU, 8 fils de calcul, `OLLAMA_NUM_PARALLEL=1` (premiers essais : Ollama 0.30.7, `OLLAMA_NUM_PARALLEL=2`) | génération 16,4 jetons/s, lecture du prompt 64 jetons/s ([migration](../../outils/resultats/socle/migration-llm-service-2026-11-08.txt)) |
| Chat | qwen3:4b-instruct (GGUF, 2,5 Go) | 14,7 à 17,9 jetons/s en génération (14,7 à `num_ctx` 16384), 24 à 67 jetons/s en lecture de prompt |
| Embedding | bge-m3 | environ 130 jetons/s |
| `num_ctx` | 16384 (6144 suffit pour ce corpus, sans marge pour l'historique) | voir sections 2 et 4 |
| Open Notebook | Docling actif, `OPEN_NOTEBOOK_WORKER_MAX_TASKS=1`, `ESPERANTO_LLM_TIMEOUT=900` | 28/34 exactes, 4/4 refus, médiane 9,1 s, p95 23,8 s |
| Mémoire totale en pointe | application 3,8 Go + Ollama 8,3 à 10 Go | tient dans 15,3 Go |

**Configuration minimale sans GPU** déduite du profil A [Vérifié] ([mesures du socle](../../outils/resultats/socle/mesures-2026-11-08-passe1.log), [migration](../../outils/resultats/socle/migration-llm-service-2026-11-08.txt)) : 16 Go de RAM, 8 cœurs, qwen3:4b-instruct et bge-m3, `num_ctx` 16384, `OLLAMA_NUM_PARALLEL=1`, 8 fils de calcul. RAM d'Ollama à 16384 et une requête : 5,5 Go. Lecture du prompt : 36 à 39 jetons/s ; un prompt de 8 192 jetons demande 290 s avant le premier mot. Volume de documents en « Contenu complet » par conversation : 3,5 caractères par jeton sur le corpus (10 677 caractères pour 3 084 jetons) ; au plus environ 13 000 jetons de documents, soit 45 000 caractères, une fois retirés les consignes (environ 1 150 jetons), la réponse et l'historique [Estimation] ; 4 000 jetons (12 000 caractères) pour une première réponse en 1 min 30 [Vérifié]. Modèles de moins de 3 milliards de paramètres : [À tester].

**Profil B** (Ryzen 5 9600X, RTX 4060 Ti 16 Go, plus de 30 Go de RAM, WSL) — mesuré le 2026-11-09 [Vérifié] :

| Élément | Réglage | Résultat |
|---|---|---|
| Serveur de modèles | LLM-Service, branche `service-vllm` : deux conteneurs `vllm-central` (chat) et `vllm-embed` (embedding), un modèle par serveur vLLM v0.29.0 | socle de référence de la série ; le reranker du socle ne sert pas, Open Notebook 1.15.1 n'en utilise pas |
| Chat | Gemma 4 E4B, checkpoint officiel Google QAT w4a16 (environ 11,5 Go sur disque) — et non Qwen3-4B-Instruct en 4 bits comme estimé plus haut (voir section 2, « écart au modèle prévu ») | `VLLM_GPU_MEMORY_UTILIZATION=0.80`, `VLLM_KV_CACHE_DTYPE=fp8` |
| Embedding | bge-m3 | `VLLM_EMBED_GPU_MEMORY_UTILIZATION=0.05` |
| `max_model_len` | 32768 | voir sections 2 et 4 |
| Open Notebook | Docling actif | 28/34 exactes, 4/4 refus, médiane 1,86 s, p95 4,59 s (chat) ; 28/34, médiane 7,7 s (Demander) |
| VRAM en pointe | 15,7 Go sur 16,4 Go (chat + embedding chargés en permanence) | marge faible sur une carte 16 Go ; un modèle plus gros ou un contexte plus long déborderait |
| Mémoire vive en pointe | application 7,4 Go (Docling), vLLM mesuré côté hôte (`docker stats`) : 6,8 Go (chat) + 4,9 Go (embedding) | tient largement dans 30 Go de RAM |

### Pour aller plus loin

Fournisseur déclaré dans Open Notebook pour vLLM : « OpenAI Compatible », deux crédentials distincts (vLLM n'a qu'un modèle par conteneur, contrairement à Ollama) : Base URL `http://vllm-central:8000/v1` pour le langage, `http://vllm-embed:8000/v1` pour l'embedding (réseau `llm-net`), branchés par `outils/open-notebook/configurer.py --moteur vllm` [Vérifié]. Qwen3-4B-Instruct en 4 bits sur vLLM, et une carte graphique de 8 Go (le minimum réellement nécessaire plutôt que les 16 Go de la machine d'essai), restent [À tester].

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| 0 réponse sur le banc, erreurs 502 | `num_ctx` trop petit pour les sources en « full content » | augmenter `num_ctx` ou réduire les sources |
| « Demander » très lent ou sans réponse sur CPU | plusieurs appels au modèle et sortie de stratégie longue, coupée par le délai de 900 s | utiliser le chat de carnet sur CPU ; « Demander » est utilisable avec un GPU (section 5, profil B) |
| Résultats du juge LLM incohérents | petit modèle juge | se fier à la correspondance exacte, relire les réponses |

## Sources

- Banc : `outils/communs/banc/commun.py`, `renoter.py`, `tableau.py`, `tests/test_commun.py` ; `outils/open-notebook/banc.py`, `file_essais.sh`, `suite_essais.sh`, `suite_essais2.sh`
- Résultats : `outils/resultats/open-notebook/banc-2026-11-08-*.json` et `.md` (profil A, CPU) ; `banc-2026-11-09-gpu-vllm*.json` (profil B, GPU) ; [mesures du socle](../../outils/resultats/socle/mesures-2026-11-08-passe2.json)
- Corpus : `outils/communs/generer_corpus.py`, [questions](../../corpus/questions.json)
