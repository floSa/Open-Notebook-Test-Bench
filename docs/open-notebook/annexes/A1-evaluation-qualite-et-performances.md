# A1. Évaluation : qualité et performances

> **Objet** : mesurer la justesse des réponses, les citations, les refus et les temps de réponse d'Open Notebook sur un corpus de référence, avec les modèles du service LLM central ; dire quels réglages changent le résultat.
> **Prérequis** : [Discuter avec ses sources](../manuel/06-discuter-avec-les-sources.md), [Rechercher et demander](../manuel/08-rechercher-et-demander.md).
> **Version décrite** : Open Notebook 1.15.1, Docling actif, découpage de 400 jetons (chevauchement 60) ; service LLM central : `chat` (Qwen3.5-4B, réflexion activée, 16 384 jetons par requête), `embed` (bge-m3), `transcribe` (faster-whisper-small) ; profil `gpu` (RTX 4060 Ti 16 Go). Bancs antérieurs : Ollama sur processeur (qwen3:4b-instruct), vLLM sur carte (Gemma 4 E4B).
> **Statut des informations** : [Vérifié] mesuré sur la machine d'essai, avec renvoi au résultat brut ; [Source] documentation officielle ou code source au tag v1.15.1 ; [Estimation] calcul non mesuré, avec sa base ; [À tester] non essayé.
> **Précautions** : corpus fictif Vélanor de 9 documents ([manifeste](../../../corpus/MANIFEST.json)) et 38 questions ([questions](../../../corpus/questions.json)) ; un banc par fichier `outils/resultats/open-notebook/banc-*.json` ; le modèle ne répond pas deux fois exactement pareil.

**Risque signalé.** Une réponse citée n'est pas forcément juste, et une réponse « je ne trouve pas d'information » est souvent fausse quand le document existe mais n'a pas été lu (scan sans OCR). Sur le banc, toutes les erreurs viennent du contrat scanné ; aucune réponse n'a inventé de chiffre [Vérifié].

## Sommaire

1. [Le banc](#1-le-banc)
2. [Résultats avec le service central](#2-résultats-avec-le-service-central)
3. [Réglages qui changent le résultat](#3-réglages-qui-changent-le-résultat)
4. [Comparaison avec l'ancienne pile](#4-comparaison-avec-lancienne-pile)
5. [Préconisations](#5-préconisations)
6. [Dépannage](#dépannage)
7. [Sources](#sources)

## 1. Le banc

| Élément | Contenu |
|---|---|
| Corpus | rapport PDF de 10 pages avec tableaux, contrat PDF scanné, procédure DOCX avec tableau, présentation PPTX, classeur XLSX, page HTML, note Markdown, audit PDF en anglais, message audio MP3 |
| Questions | 38 : 13 faits simples, 10 tableaux, 4 sur le scan, 2 en anglais, 3 multi-documents, 2 sur l'audio, 4 pièges sans réponse dans le corpus |
| Mode « chat » | une session de chat par question dans le carnet « Banc », toutes les sources en « full content » (contenu complet) |
| Mode « Demander » | `POST /api/search/ask/simple` : recherche vectorielle puis synthèse, modèle `chat` aux trois étapes |
| Exactitude | chaque élément attendu (valeur exacte ou mot-clé) présent dans la réponse ; un nombre ne doit pas être collé à d'autres chiffres |
| Refus | sur un piège, la réponse doit dire que l'information est absente |
| Citation | un `[source:…]` de la réponse désigne le document attendu ; pas de page (Open Notebook ne la fournit pas) |
| Juge LLM | complément, signalé comme tel : `chat` du service central, réflexion coupée, réponse OUI ou NON |
| Mesures | latence par question (p50, p95), durée d'indexation, pic de RAM par conteneur (`docker stats`, application séparée des conteneurs `llm-*`), mémoire de carte (`nvidia-smi`, fin de banc) |
| Reranker | aucun : Open Notebook 1.15.1 n'en accepte pas (« Reranking is out of scope (#1087) » dans son code) [Vérifié] ([relevé](../../../outils/resultats/open-notebook/reranker-2026-11-12.txt)) ; le banc sans puis avec `rerank` est donc sans objet |

Commande [Testée] (`outils/resultats/open-notebook/essai-2026-11-12-banc-chat.log`) :

```bash
python3 outils/open-notebook/banc.py --etiquette central-chat --reindexer
```

## 2. Résultats avec le service central

| Banc | Mode | Modèle | Sources | Exactes | Refus pièges | Bon document cité | p50 | p95 | Indexation | Pic RAM application |
|---|---|---|---|---|---|---|---|---|---|---|
| [central-chat](../../../outils/resultats/open-notebook/banc-2026-11-12-central-chat.json) | conversation de carnet | `chat` (Qwen3.5-4B) | contenu complet, Docling | 28/34 | 4/4 | 29 | 8,7 s | 27,9 s | 65 s | 4,7 Go |

Valeurs [Vérifié] ([journal](../../../outils/resultats/open-notebook/essai-2026-11-12-banc-chat.log)).

Par type de question, banc `central-chat` [Vérifié] : faits simples 13/13, tableaux 10/10, anglais 2/2, audio 2/2, multi-documents 1/3, scan 0/4, pièges 4/4.

- Les quatre questions sur le contrat scanné échouent : le PDF scanné ne produit aucun texte (OCR de Docling inopérant dans l'image 1.15.1, [Fonctionnement interne](A5-fonctionnement-interne.md)). Le modèle répond « je n'ai pas trouvé d'information », ou donne le délai constaté du classeur à la place du délai contractuel (Q16).
- Deux des trois questions multi-documents dépendent du contrat (Q30, Q31) : réponse partielle, juste sur la partie lisible.
- Q32 (objectif 2026 et embauches de l'usine) : juste, mais en 58 s ; la réflexion de `chat` allonge certaines réponses (p95 27,9 s).
- Juge LLM : 31 OUI sur 38 ; il rejette une réponse juste (Q35, piège correctement refusé) et suit sinon la notation par mots-clés [Vérifié].
- Mémoire en pointe : application 4,7 Go (Docling compris), service central `llm-swap` 5,8 Go, carte graphique 8,4 Go sur 16 [Vérifié].

## 3. Réglages qui changent le résultat

| Réglage | Effet | Statut |
|---|---|---|
| Sources en « aperçus » au lieu du contenu complet | réponses incomplètes : sur les mêmes questions des cas pratiques, le trimestre le plus élevé n'est pas trouvé, alors qu'il l'est en contenu complet ; contexte 4,5 K jetons au lieu de 7,0 K | [Vérifié] sur 5 questions ([aperçus](../../../outils/resultats/open-notebook/cas-pratiques-apercus-2026-11-12.json), [contenu complet](../../../outils/resultats/open-notebook/demo-2026-11-12.json)) ; banc complet en aperçus [À tester] |
| Contexte au-delà de 16 384 jetons | erreur explicite « ContextWindowExceededError … request (21842 … » ; rien n'est tronqué en silence | [Vérifié] ([dépassement](../../../outils/resultats/open-notebook/contexte-2026-11-12.txt)) |
| Mode « Demander » (recherche vectorielle puis synthèse) | une question essayée dans l'interface : score de 87/100 et non-conformités de l'audit retrouvés, avec citations ; banc complet sur le service central non rejoué | [Vérifié] pour la question (captures du chapitre 08) ; banc [À tester] ; sur l'ancienne pile GPU : 28/34, médiane 7,7 s ([banc](../../../outils/resultats/open-notebook/banc-2026-11-09-gpu-vllm-docling-demander.json)) |
| Docling activé | +3 réponses justes sur l'ancienne pile (tableau DOCX, audio) | [Vérifié] ancienne pile |
| Reranker `rerank` | impossible : non accepté par Open Notebook 1.15.1 | [Vérifié] ([relevé](../../../outils/resultats/open-notebook/reranker-2026-11-12.txt)) |
| Réflexion de `chat` coupée | impossible depuis Open Notebook (aucun paramètre de requête réglable par modèle) ; levier qui relève de LLM-Service | [Vérifié] (fenêtres de configuration, chapitres 03 et 06) |

### Recherche plein texte et vectorielle

Dix requêtes, rang du document attendu dans chaque mode, sur l'ancienne pile (bge-m3 servi par Ollama, même modèle d'embedding qu'aujourd'hui, autre quantification) [Vérifié] (`outils/open-notebook/essai_recherche.py`, [résultat](../../../outils/resultats/open-notebook/recherche-2026-11-08.json)) :

| Nature | Requête | Plein texte | Vectoriel (score du 1er) |
|---|---|---|---|
| référence exacte | BAT-48V-14Ah | 1er | 1er (0,61) |
| nom propre | Motodrive | 2e | 2e (0,42) |
| mots exacts | prime d'intéressement | 1er | 1er (0,57) |
| reformulation | Combien de temps le cadre est-il couvert en cas de défaut ? | aucun résultat | 1er (0,60) |
| synonyme | Où ranger les accumulateurs et à quelle température ? | aucun résultat | 1er (0,58) |
| paraphrase | nouvelle usine près de l'estuaire de la Loire | aucun résultat | 3e (0,49) |
| anglais | battery supplier audit score | aucun résultat | 1er (0,70) |
| français vers document anglais | score de l'audit du fournisseur de batteries | aucun résultat | 1er (0,68) |
| thème | chiffre d'affaires par trimestre | 1er | 1er (0,68) |
| absent du corpus | trottinette électrique | aucun résultat | 6 résultats sans rapport (0,46) |

Le plein texte ne sert qu'aux mots exacts ; le vectoriel retrouve les reformulations et passe d'une langue à l'autre, mais renvoie toujours quelque chose, même pour un sujet absent, avec un score proche de celui des vraies réponses. Constat refait le 12 novembre dans l'interface : « Où ranger les accumulateurs et à quelle température ? » ne donne aucun résultat en recherche textuelle et ramène des passages en recherche vectorielle [Vérifié] (captures du chapitre 08, texte dans `outils/resultats/open-notebook/captures/08-rechercher/`).

## 4. Comparaison avec l'ancienne pile

Mêmes 38 questions, même corpus, autres modèles : modèles différents, non comparable tel quel [Vérifié] (fichiers datés du 8 et du 9 novembre dans `outils/resultats/open-notebook/`).

| Banc | Service de modèles | Modèle de réponse | Exactes | Refus | Médiane | p95 |
|---|---|---|---|---|---|---|
| [docling-qwen-fullcontent-ollama040](../../../outils/resultats/open-notebook/banc-2026-11-08-docling-qwen-fullcontent-ollama040.json) | Ollama 0.40.15, processeur (profil A) | qwen3:4b-instruct | 28/34 | 4/4 | 7,4 s | 24,2 s |
| [gpu-vllm-docling](../../../outils/resultats/open-notebook/banc-2026-11-09-gpu-vllm-docling.json) | vLLM, carte (profil B) | Gemma 4 E4B | 28/34 | 4/4 | 1,9 s | 4,6 s |
| [central-chat](../../../outils/resultats/open-notebook/banc-2026-11-12-central-chat.json) | service central, carte (profil B) | Qwen3.5-4B, réflexion activée | 28/34 | 4/4 | 8,7 s | 27,9 s |

Les trois bancs font les mêmes six erreurs (le contrat scanné). Le modèle `chat` réfléchit avant de répondre, ce qui explique une médiane plus haute que Gemma 4 E4B sans réflexion sur la même carte ; Open Notebook n'offre aucun réglage pour couper cette réflexion (pas de paramètre `chat_template_kwargs` dans la configuration d'un modèle) [Vérifié] (fenêtres « Ajouter une configuration » et « Configuration du modèle », chapitre 03 et 06).

## 5. Préconisations

- Garder Docling actif : sans lui, le tableau du document Word est perdu (−3 réponses justes sur l'ancienne pile) [Vérifié] ([banc sans Docling](../../../outils/resultats/open-notebook/banc-2026-11-08-defaut-qwen-fullcontent.json)).
- Mettre les sources utiles en « contenu complet » : un nouveau document n'est envoyé que par son aperçu tant que ce mode n'est pas choisi [Vérifié] (chapitre 04, étape 8).
- Faire passer les documents scannés par un OCR avant de les ajouter [À tester] avec un outil extérieur.
- Pour un grand nombre de documents, préférer « Demander », qui ne lit que les passages trouvés, à la conversation, qui envoie tout ([taille de contexte](A2-choisir-son-materiel-et-ses-modeles.md#4-taille-de-contexte-et-volume-de-documents)).

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| « Je ne trouve pas d'information » alors que le document existe | document scanné non lu, ou source exclue du contexte | vérifier la carte de la source (« Échec ») et son mode de contexte |
| Une réponse sur cinq dépasse 20 s | réflexion de `chat` | normal avec ce modèle ; non réglable dans Open Notebook |
| Juge LLM en désaccord avec la notation | petit modèle juge | relire la réponse ; la notation par mots-clés fait foi |

## Sources

- Scripts : `outils/communs/banc/commun.py` (notation, mesures, juge), `outils/open-notebook/banc.py` (adaptateur), `outils/communs/banc/tableau.py` (tableau comparatif).
- Résultats : `outils/resultats/open-notebook/banc-*.json` et `.md`.
- Code d'Open Notebook 1.15.1 : `open_notebook/ai/provider_registry.py`, `model_discovery.py` (reranker), `api/routers/models.py` (types de modèles).
