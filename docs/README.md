# Index de la série

Manuels vérifiés de cinq solutions de RAG local, alternatives auto-hébergées à NotebookLM. Chaque solution a son dépôt `https://github.com/floSa/<Solution>-Test-Bench` ; cette page est identique dans les cinq dépôts.

## Solutions décrites

| Solution | Version décrite | Manuel utilisateur |
|---|---|---|
| Open Notebook | 1.15.1 | [Open-Notebook-Test-Bench](https://github.com/floSa/Open-Notebook-Test-Bench/blob/master/docs/open-notebook/README.md) |
| RAGFlow | 1.0.0 | [RAGFlow-Test-Bench](https://github.com/floSa/RAGFlow-Test-Bench/blob/main/docs/ragflow/README.md) |
| AnythingLLM | 1.19.0 | [AnythingLLM-Test-Bench](https://github.com/floSa/AnythingLLM-Test-Bench/blob/main/docs/anythingllm/README.md) |
| Kotaemon | 0.12.0 | [Kotaemon-Test-Bench](https://github.com/floSa/Kotaemon-Test-Bench/blob/main/docs/kotaemon/README.md) |
| Open WebUI | 0.13.3 | [OpenWebUI-Test-Bench](https://github.com/floSa/OpenWebUI-Test-Bench/blob/main/docs/open-webui/README.md) |

Essais : novembre 2026. Machine : Ryzen 5 9600X, RTX 4060 Ti 16 Go, 64 Go de RAM (32 Go attribués à WSL2).

## Modèles utilisés

Les cinq solutions appellent le même service de modèles local (LiteLLM devant llama.cpp et un serveur Whisper), avec les mêmes modèles :

| Rôle | Modèle |
|---|---|
| Réponse | Qwen3.5-4B (Q4_K_M), réflexion activée, 16 384 jetons par requête |
| Embedding | bge-m3 (Q8_0) |
| Reranker | bge-reranker-v2-m3 (Q8_0) |
| Transcription audio | faster-whisper-small |

## Services déportables

Un service « déporté » tourne hors du conteneur de la solution et peut être partagé par plusieurs applications. Dans ce banc, le service de modèles ci-dessus est déporté pour toutes ; Docling (lecture des PDF et OCR) l'est pour Open WebUI, dans un conteneur `docling-serve` 1.38.2 à part.

### Lecture des documents scannés (OCR)

Le corpus contient un contrat scanné (PDF image, 4 questions). Sans OCR, il est illisible.

| Solution | OCR utilisé dans le banc | Scan lu | Docling déporté possible | Docling déporté essayé | Procédure dans le manuel |
|---|---|---|---|---|---|
| Open WebUI | Docling déporté | oui | oui | oui, banc complet | [chapitre 08](https://github.com/floSa/OpenWebUI-Test-Bench/blob/main/docs/open-webui/manuel/08-regler-la-lecture-des-documents.md) |
| RAGFlow | DeepDoc, l'OCR intégré de RAGFlow | oui | oui (réglage `DOCLING_SERVER_URL`, plus `ALLOW_ANY_HOST=1`) | oui, banc complet : 34/34, même score qu'avec DeepDoc | [chapitre 06](https://github.com/floSa/RAGFlow-Test-Bench/blob/main/docs/ragflow/manuel/06-regler-la-lecture-des-documents.md), étapes 31 à 33 |
| Kotaemon | Docling, dans le conteneur de Kotaemon | oui | oui (lecteur ajouté au conteneur) | oui, banc complet : 29/34 (31 avec le Docling intégré, écart expliqué ci-dessous) | [chapitre 05](https://github.com/floSa/Kotaemon-Test-Bench/blob/main/docs/kotaemon/manuel/05-ajouter-et-organiser-ses-documents.md), étapes 17 et 18 |
| AnythingLLM | Tesseract, l'OCR intégré d'AnythingLLM | oui | non | sans objet | sans objet |
| Open Notebook | Docling, dans le conteneur d'Open Notebook, sans moteur d'OCR dans l'image 1.15.1 | non | non | sans objet | sans objet |

DeepDoc est le lecteur de documents propre à RAGFlow (OCR, mise en page, tableaux) ; ses modèles sont dans l'image de RAGFlow et ne se déportent pas.

Docling déporté, ce que les bancs du 13 novembre montrent :

- RAGFlow : même score qu'avec DeepDoc (34/34, 4/4), indexation deux fois plus rapide (35 s contre 64 s). Le branchement demande `ALLOW_ANY_HOST=1`, qui autorise RAGFlow à joindre toute adresse du réseau privé, pas seulement Docling.
- Kotaemon : 29/34 au lieu de 31. Le lecteur déporté relit tous les PDF, alors que le meilleur banc ne relisait que le scan ; deux questions sur les tableaux du rapport annuel échouent à cause de ce découpage différent, pas du déport.
- Le conteneur Docling occupe environ 2,5 Go de mémoire : le déport n'allège l'ensemble que s'il est partagé par plusieurs applications.

### Audio et reranker

| Solution | Transcription audio | Reranker bge-reranker-v2-m3 branchable | Reranker utilisé dans le meilleur réglage |
|---|---|---|---|
| Open WebUI | Whisper déporté | oui | bge-reranker-v2-m3 |
| RAGFlow | Whisper déporté | oui | aucun : essayé, même score (34/34), donc laissé de côté |
| Kotaemon | ne lit pas l'audio | oui | bge-reranker-v2-m3 |
| AnythingLLM | Whisper déporté | non : seulement son reranker intégré (ms-marco-MiniLM-L-6-v2) | intégré |
| Open Notebook | Whisper déporté | non : aucune étape de tri | sans objet |

## Comparatif du banc

Mêmes 38 questions ([corpus/questions.json](../corpus/questions.json) : 34 avec réponse, 4 pièges sans réponse dans le corpus), même corpus fictif de 9 documents (dont le PDF scanné et un message vocal), mêmes modèles. Deux lignes par solution : le réglage livré par défaut, puis le meilleur réglage trouvé ; une troisième ligne quand le meilleur réglage a été rejoué avec Docling déporté. Toutes les variantes essayées sont dans l'annexe A1 de chaque manuel.

| Solution | Réglage | OCR | Recherche | Passages | Reranker | Exactes /34 | Pièges refusés /4 | Bon document cité /34 | Médiane | p95 | Pic RAM de l'application | Résultat brut |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Open WebUI | défaut | aucun : scan refusé | vecteurs | 10 | aucun | 28 | 4 | 30 | 60,1 s | 106,0 s | 2,3 Go | [JSON](https://github.com/floSa/OpenWebUI-Test-Bench/blob/main/outils/resultats/open-webui/banc-2026-11-13-defaut-sans-rerank.json) |
| Open WebUI | meilleur | Docling déporté | hybride | 10 | bge-reranker-v2-m3 | 34 | 4 | 34 | 24,0 s ¹ | 86,9 s | 3,6 Go | [JSON](https://github.com/floSa/OpenWebUI-Test-Bench/blob/main/outils/resultats/open-webui/banc-2026-11-13-taches.json) |
| RAGFlow | défaut | DeepDoc | hybride, vecteurs 0,3 | 6 | aucun | 33 | 4 | 34 | 7,8 s | 50,0 s | 5,4 Go | [JSON](https://github.com/floSa/RAGFlow-Test-Bench/blob/main/outils/resultats/ragflow/banc-2026-11-12-defaut.json) |
| RAGFlow | meilleur | DeepDoc | hybride, vecteurs 0,7 | 8 | aucun ³ | 34 | 4 | 34 | 7,8 s | 56,9 s | 5,1 Go | [JSON](https://github.com/floSa/RAGFlow-Test-Bench/blob/main/outils/resultats/ragflow/banc-2026-11-12-hybride-vecteurs07-top8.json) |
| RAGFlow | meilleur, Docling déporté | Docling déporté | hybride, vecteurs 0,7 | 8 | aucun | 34 | 4 | 34 | 8,1 s | 61,2 s | 7,3 Go, dont 2,5 Go pour Docling | [JSON](https://github.com/floSa/RAGFlow-Test-Bench/blob/main/outils/resultats/ragflow/banc-2026-11-13-docling-deporte-vecteurs07-top8.json) |
| AnythingLLM | défaut | Tesseract | vecteurs | 4 | aucun | 33 | 3 | 33 | 14,3 s | 27,8 s | 0,9 Go | [JSON](https://github.com/floSa/AnythingLLM-Test-Bench/blob/main/outils/resultats/anythingllm/banc-2026-11-12-defaut-sans-rerank.json) |
| AnythingLLM | meilleur | Tesseract | vecteurs | 8 | intégré (MiniLM) | 34 | 4 | 34 | 10,7 s | 37,6 s | 1,6 Go | [JSON](https://github.com/floSa/AnythingLLM-Test-Bench/blob/main/outils/resultats/anythingllm/banc-2026-11-12-top8-rerank-natif.json) |
| Kotaemon | défaut | aucun | hybride | 10 | aucun | 25 ² | 4 | 27 | 25,8 s | 38,2 s | 1,9 Go | [JSON](https://github.com/floSa/Kotaemon-Test-Bench/blob/main/outils/resultats/kotaemon/banc-2026-11-12-defaut-sans-rerank.json) |
| Kotaemon | meilleur | Docling dans le conteneur | hybride | 3 | bge-reranker-v2-m3 | 31 | 4 | 32 | 22,0 s | 38,7 s | 1,7 Go | [JSON](https://github.com/floSa/Kotaemon-Test-Bench/blob/main/outils/resultats/kotaemon/banc-2026-11-12-docling-rerank-serre-top3.json) |
| Kotaemon | meilleur, Docling déporté | Docling déporté | hybride | 3 | bge-reranker-v2-m3 | 29 ⁴ | 4 | 32 | 18,4 s | 27,3 s | 4,9 Go, dont 2,5 Go pour Docling | [JSON](https://github.com/floSa/Kotaemon-Test-Bench/blob/main/outils/resultats/kotaemon/banc-2026-11-13-docling-deporte-rerank-serre-top3.json) |
| Open Notebook | défaut = meilleur | aucun (Docling sans OCR) | aucune : sources entières | toutes | aucun | 28 | 4 | 29 | 8,7 s | 27,9 s | 4,7 Go | [JSON](https://github.com/floSa/Open-Notebook-Test-Bench/blob/master/outils/resultats/open-notebook/banc-2026-11-12-central-chat.json) |

¹ Génération des requêtes de recherche coupée ; laissée active (défaut), la médiane passe à 58 s. ² Le comptage automatique donne 26 : une réponse qui refuse (Q17) y est comptée juste à tort. ³ RAGFlow accepte bge-reranker-v2-m3 : essayé sur ce réglage, même score (34/34) et réponses un peu plus lentes, donc laissé de côté. ⁴ Docling déporté relit tous les PDF, le Docling intégré ne relisait que le scan : deux questions sur les tableaux du rapport annuel échouent à cause de ce découpage différent.

Lecture :

- Le PDF scanné fait l'essentiel des écarts : les solutions qui le lisent atteignent 34/34 ; les autres perdent ses 4 questions et une ou deux questions multi-documents qui en dépendent.
- Kotaemon ne lit pas l'audio : 2 questions perdues quel que soit le réglage.
- La durée vient surtout de la réflexion du modèle et des appels supplémentaires de la solution (génération de requêtes, surlignage des citations). Open WebUI, réflexion coupée, donne 34/34 avec une médiane de 1,3 s ([JSON](https://github.com/floSa/OpenWebUI-Test-Bench/blob/main/outils/resultats/open-webui/banc-2026-11-13-sans-reflexion.json)).
- Mémoire : RAGFlow est le plus lourd (environ 5 Go : Elasticsearch, MySQL, MinIO, DeepDoc), AnythingLLM le plus léger (0,9 à 1,6 Go). Le service de modèles, commun aux cinq, n'est pas compté.

## Parcours de lecture conseillés

| Profil | Parcours |
|---|---|
| Découvrir le RAG local | [glossaire](glossaire.md), puis le chapitre 01 « Découvrir » de chaque manuel |
| Installer et essayer rapidement | chapitres 01 à 04 de chaque manuel |
| Choisir entre solutions | les tableaux ci-dessus, puis les annexes A1 (qualité et performances) et A2 (matériel et modèles) de chaque manuel |

## Étiquettes des annexes

Dans les annexes de chaque manuel, chaque affirmation porte une étiquette qui dit d'où elle vient :

| Étiquette | Sens |
|---|---|
| [Vérifié] | observé ou mesuré sur la machine d'essai ; renvoie à un script et à un résultat brut de `outils/` |
| [Source] | lu dans la documentation officielle ou le code source, non essayé |
| [Estimation] | calcul non mesuré, avec son raisonnement |
| [À tester] | ni documenté ni essayé |
| [Testée] | commande exécutée pendant les essais |
| [Aide] | commande lue dans l'aide, non exécutée |

Les étiquettes ne figurent que dans les annexes (partie 2) ; le manuel (partie 1) se lit sans elles. Les libellés de l'interface sont cités tels qu'affichés. Les données sont fictives (entreprise Vélanor).
