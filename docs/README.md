# Index de la série

Cinq solutions de RAG local, alternatives auto-hébergées à NotebookLM, testées sur le même corpus avec les mêmes modèles. Cette page est identique dans les cinq dépôts.

## Solutions

| | Open WebUI | RAGFlow | AnythingLLM | Kotaemon | Open Notebook |
|---|---|---|---|---|---|
| Version | 0.13.3 | 1.0.0 | 1.19.0 | 0.12.0 | 1.15.1 |
| Manuel | [OpenWebUI-Test-Bench](https://github.com/floSa/OpenWebUI-Test-Bench/blob/main/docs/open-webui/README.md) | [RAGFlow-Test-Bench](https://github.com/floSa/RAGFlow-Test-Bench/blob/main/docs/ragflow/README.md) | [AnythingLLM-Test-Bench](https://github.com/floSa/AnythingLLM-Test-Bench/blob/main/docs/anythingllm/README.md) | [Kotaemon-Test-Bench](https://github.com/floSa/Kotaemon-Test-Bench/blob/main/docs/kotaemon/README.md) | [Open-Notebook-Test-Bench](https://github.com/floSa/Open-Notebook-Test-Bench/blob/master/docs/open-notebook/README.md) |

Essais : novembre 2026. Machine : Ryzen 5 9600X, RTX 4060 Ti 16 Go, 64 Go de RAM (32 Go attribués à WSL2).

## Modèles

Les cinq solutions appellent le même service de modèles, hors de leur conteneur :

| Rôle | Modèle |
|---|---|
| Réponse | Qwen3.5-4B (Q4_K_M), réflexion activée, 16 384 jetons par requête |
| Embedding | bge-m3 (Q8_0) |
| Reranker | bge-reranker-v2-m3 (Q8_0) |
| Transcription audio | faster-whisper-small |

Toutes les solutions n'acceptent pas tous ces modèles : les trois tableaux suivants disent lesquels.

## PDF scanné : OCR et Docling

Le corpus contient un contrat scanné (4 questions). Sans OCR, il est illisible.

| | Open WebUI | RAGFlow | AnythingLLM | Kotaemon | Open Notebook |
|---|---|---|---|---|---|
| OCR intégré | aucun | DeepDoc | Tesseract | aucun | aucun |
| Docling dans le conteneur | non | non | non | oui | oui, mais sans OCR |
| Docling déporté (serveur à part) | oui | oui ¹ | non | oui | non |
| OCR utilisé au banc | Docling déporté | DeepDoc | Tesseract | Docling dans le conteneur | aucun |
| Scan lu | oui | oui | oui | oui | non |
| Score avec Docling déporté | 34/34 | 34/34 | impossible | 29/34 ² | impossible |

¹ Demande `ALLOW_ANY_HOST=1`, qui autorise RAGFlow à joindre toute adresse du réseau privé, pas seulement Docling.
² 31/34 avec le Docling du conteneur : le Docling déporté relit tous les PDF, le découpage du rapport annuel change et deux questions sur ses tableaux échouent.

## Audio

| | Open WebUI | RAGFlow | AnythingLLM | Kotaemon | Open Notebook |
|---|---|---|---|---|---|
| Transcription | Whisper déporté | Whisper déporté | Whisper déporté | non : l'audio n'est pas lu | Whisper déporté |
| Questions audio réussies | 2/2 | 2/2 | 2/2 | 0/2 | 2/2 |

## Reranker

| | Open WebUI | RAGFlow | AnythingLLM | Kotaemon | Open Notebook |
|---|---|---|---|---|---|
| bge-reranker-v2-m3 branchable | oui | oui | non : seulement son reranker intégré (MiniLM) | oui | non : aucune étape de tri |
| Exactes sans puis avec reranker | 28 puis 28 (sans Docling) | 33 puis 34 (défaut), 34 puis 34 (meilleur) | 33 puis 34 (son reranker) | 25 puis 25 | impossible |

## Résultats par cas

Nombre de réponses exactes sur 34, puis temps de réponse médian.

| Cas | Open WebUI | RAGFlow | AnythingLLM | Kotaemon | Open Notebook |
|---|---|---|---|---|---|
| Réglage par défaut | 28, 60,1 s | 33, 7,8 s | 33 ³, 14,3 s | 25 ⁴, 25,8 s | 28, 8,7 s |
| Meilleur réglage | 34, 24,0 s | 34, 7,8 s | 34, 10,7 s | 31, 22,0 s | 28, 8,7 s |
| Meilleur réglage avec bge-reranker-v2-m3 | 34 (déjà inclus) | 34, 8,8 s | impossible | 31 (déjà inclus) | impossible |
| Meilleur réglage avec Docling déporté | 34 (déjà inclus) | 34, 8,1 s | impossible | 29, 18,4 s | impossible |

³ 3 pièges refusés sur 4 ; tous les autres cas en refusent 4 sur 4.
⁴ Le comptage automatique donne 26 : une réponse qui refuse (Q17) y est comptée juste à tort.

Open WebUI avec la réflexion du modèle coupée : 34/34, 1,3 s ([résultat brut](https://github.com/floSa/OpenWebUI-Test-Bench/blob/main/outils/resultats/open-webui/banc-2026-11-13-sans-reflexion.json)). La durée vient surtout de la réflexion du modèle.

## Détail du meilleur réglage

| | Open WebUI | RAGFlow | AnythingLLM | Kotaemon | Open Notebook |
|---|---|---|---|---|---|
| OCR | Docling déporté | DeepDoc | Tesseract | Docling dans le conteneur | aucun |
| Recherche | hybride | hybride, vecteurs 0,7 | vecteurs | hybride | aucune : documents envoyés en entier |
| Passages envoyés au modèle | 10 | 8 | 8 | 3 | tous |
| Reranker | bge-reranker-v2-m3 | aucun | intégré (MiniLM) | bge-reranker-v2-m3 | aucun |
| Exactes /34 | 34 | 34 | 34 | 31 | 28 |
| Pièges refusés /4 | 4 | 4 | 4 | 4 | 4 |
| Bon document cité /34 | 34 | 34 | 34 | 32 | 29 |
| Temps médian | 24,0 s ⁵ | 7,8 s | 10,7 s | 22,0 s | 8,7 s |
| Temps p95 | 86,9 s | 56,9 s | 37,6 s | 38,7 s | 27,9 s |
| Mémoire de l'application | 3,6 Go | 5,1 Go | 1,6 Go | 1,7 Go | 4,7 Go |
| Résultat brut | [JSON](https://github.com/floSa/OpenWebUI-Test-Bench/blob/main/outils/resultats/open-webui/banc-2026-11-13-taches.json) | [JSON](https://github.com/floSa/RAGFlow-Test-Bench/blob/main/outils/resultats/ragflow/banc-2026-11-12-hybride-vecteurs07-top8.json) | [JSON](https://github.com/floSa/AnythingLLM-Test-Bench/blob/main/outils/resultats/anythingllm/banc-2026-11-12-top8-rerank-natif.json) | [JSON](https://github.com/floSa/Kotaemon-Test-Bench/blob/main/outils/resultats/kotaemon/banc-2026-11-12-docling-rerank-serre-top3.json) | [JSON](https://github.com/floSa/Open-Notebook-Test-Bench/blob/master/outils/resultats/open-notebook/banc-2026-11-12-central-chat.json) |

⁵ Génération des requêtes de recherche coupée ; laissée active (réglage par défaut), 58 s.

Sens des lignes :

- Exactes : la réponse contient la bonne valeur (exemple : « 48,6 » pour le chiffre d'affaires).
- Pièges refusés : sur les 4 questions dont la réponse n'est pas dans le corpus, l'outil dit ne pas savoir au lieu d'inventer.
- Bon document cité : la source affichée sous la réponse est le bon document.
- Temps p95 : 95 % des réponses arrivent en moins de ce temps.
- Mémoire de l'application : pic mesuré pendant le banc, conteneurs de la solution seulement (le service de modèles, commun aux cinq, n'est pas compté).

Corpus : 9 documents d'une entreprise fictive, Vélanor (PDF texte, PDF scanné, PDF en anglais, DOCX, PPTX, XLSX, HTML, Markdown, message vocal MP3). Questions : [corpus/questions.json](../corpus/questions.json), 34 avec réponse et 4 pièges.
