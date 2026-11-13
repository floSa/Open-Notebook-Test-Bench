# Index de la série

Cinq solutions de RAG local, alternatives auto-hébergées à NotebookLM, testées sur le même corpus avec les mêmes modèles. Cette page est identique dans les cinq dépôts. Une case vide : la solution ne le fait pas.

## Solutions

<table>
<tr><th width="200" align="left"></th><th width="150" align="left">Open WebUI</th><th width="150" align="left">RAGFlow</th><th width="150" align="left">AnythingLLM</th><th width="150" align="left">Kotaemon</th><th width="150" align="left">Open Notebook</th></tr>
<tr><td>Version</td><td>0.13.3</td><td>1.0.0</td><td>1.19.0</td><td>0.12.0</td><td>1.15.1</td></tr>
<tr><td>Manuel</td><td><a href="https://github.com/floSa/OpenWebUI-Test-Bench/blob/main/docs/open-webui/README.md">OpenWebUI-Test-Bench</a></td><td><a href="https://github.com/floSa/RAGFlow-Test-Bench/blob/main/docs/ragflow/README.md">RAGFlow-Test-Bench</a></td><td><a href="https://github.com/floSa/AnythingLLM-Test-Bench/blob/main/docs/anythingllm/README.md">AnythingLLM-Test-Bench</a></td><td><a href="https://github.com/floSa/Kotaemon-Test-Bench/blob/main/docs/kotaemon/README.md">Kotaemon-Test-Bench</a></td><td><a href="https://github.com/floSa/Open-Notebook-Test-Bench/blob/master/docs/open-notebook/README.md">Open-Notebook-Test-Bench</a></td></tr>
</table>

Essais : novembre 2026. Machine : Ryzen 5 9600X, RTX 4060 Ti 16 Go, 64 Go de RAM (32 Go attribués à WSL2).

## Modèles

Les cinq solutions appellent le même service de modèles, hors de leur conteneur.

<table>
<tr><th width="200" align="left">Rôle</th><th width="750" align="left">Modèle</th></tr>
<tr><td>Réponse</td><td>Qwen3.5-4B (Q4_K_M), réflexion activée, 16 384 jetons par requête</td></tr>
<tr><td>Embedding</td><td>bge-m3 (Q8_0)</td></tr>
<tr><td>Reranker</td><td>bge-reranker-v2-m3 (Q8_0)</td></tr>
<tr><td>Transcription audio</td><td>faster-whisper-small</td></tr>
</table>


## Lecture des PDF : Docling et OCR

Docling est un lecteur de documents : il transforme un PDF (ou un Word, un PowerPoint) en texte en retrouvant la mise en page et les tableaux. Pour lire un PDF scanné, qui n'est qu'une image, il lui faut en plus un moteur d'OCR (lecture des caractères). Docling peut tourner dans le conteneur de la solution, ou à part, dans son propre conteneur partagé (déporté).

<table>
<tr><th width="200" align="left"></th><th width="150" align="left">Open WebUI</th><th width="150" align="left">RAGFlow</th><th width="150" align="left">AnythingLLM</th><th width="150" align="left">Kotaemon</th><th width="150" align="left">Open Notebook</th></tr>
<tr><td>Docling</td><td>déporté</td><td>déporté ¹</td><td></td><td>conteneur ou déporté</td><td>conteneur, sans OCR ²</td></tr>
<tr><td>OCR intégré, autre que Docling</td><td></td><td>DeepDoc</td><td>Tesseract</td><td></td><td></td></tr>
</table>

¹ Demande `ALLOW_ANY_HOST=1`, qui autorise RAGFlow à joindre toute adresse du réseau privé, pas seulement Docling.
² Le moteur d'OCR de Docling manque dans l'image 1.15.1 : les PDF avec texte sont lus, le PDF scanné ne l'est pas.

## Audio

<table>
<tr><th width="200" align="left"></th><th width="150" align="left">Open WebUI</th><th width="150" align="left">RAGFlow</th><th width="150" align="left">AnythingLLM</th><th width="150" align="left">Kotaemon</th><th width="150" align="left">Open Notebook</th></tr>
<tr><td>Transcription</td><td>Whisper déporté</td><td>Whisper déporté</td><td>Whisper déporté</td><td></td><td>Whisper déporté</td></tr>
</table>

## Reranker

<table>
<tr><th width="200" align="left"></th><th width="150" align="left">Open WebUI</th><th width="150" align="left">RAGFlow</th><th width="150" align="left">AnythingLLM</th><th width="150" align="left">Kotaemon</th><th width="150" align="left">Open Notebook</th></tr>
<tr><td>bge-reranker-v2-m3 branchable</td><td>oui</td><td>oui</td><td></td><td>oui</td><td></td></tr>
<tr><td>Reranker intégré</td><td></td><td></td><td>MiniLM</td><td></td><td></td></tr>
</table>

## Résultats par cas

Nombre de réponses exactes sur 34, puis temps de réponse médian. Une case vide : cas impossible pour cette solution.

<table>
<tr><th width="200" align="left">Cas</th><th width="150" align="left">Open WebUI</th><th width="150" align="left">RAGFlow</th><th width="150" align="left">AnythingLLM</th><th width="150" align="left">Kotaemon</th><th width="150" align="left">Open Notebook</th></tr>
<tr><td>Réglage par défaut</td><td>28, 60,1 s</td><td>33, 7,8 s</td><td>33 ³, 14,3 s</td><td>25 ⁴, 25,8 s</td><td>28, 8,7 s</td></tr>
<tr><td>Meilleur réglage</td><td>34, 24,0 s ⁵</td><td>34, 7,8 s</td><td>34, 10,7 s</td><td>31, 22,0 s</td><td>28, 8,7 s</td></tr>
<tr><td>Meilleur réglage avec bge-reranker-v2-m3</td><td>= meilleur réglage</td><td>34, 8,8 s</td><td></td><td>= meilleur réglage</td><td></td></tr>
<tr><td>Meilleur réglage avec Docling déporté</td><td>= meilleur réglage</td><td>34, 8,1 s</td><td></td><td>29 ⁶, 18,4 s</td><td></td></tr>
<tr><td>Meilleur réglage, réflexion du modèle coupée</td><td>34, 1,3 s</td><td></td><td></td><td></td><td></td></tr>
</table>

³ 3 pièges refusés sur 4 ; tous les autres cas en refusent 4 sur 4.
⁴ Le comptage automatique donne 26 : une réponse qui refuse (Q17) y est comptée juste à tort.
⁵ Génération des requêtes de recherche coupée ; laissée active (réglage par défaut), 58 s.
⁶ 31 avec le Docling du conteneur : le Docling déporté relit tous les PDF, le découpage du rapport annuel change et deux questions sur ses tableaux échouent.

La réflexion coupée n'a été mesurée que sur Open WebUI : la durée vient surtout de la réflexion du modèle.

## Détail du meilleur réglage

<table>
<tr><th width="200" align="left"></th><th width="150" align="left">Open WebUI</th><th width="150" align="left">RAGFlow</th><th width="150" align="left">AnythingLLM</th><th width="150" align="left">Kotaemon</th><th width="150" align="left">Open Notebook</th></tr>
<tr><td>Lecture des PDF</td><td>Docling déporté</td><td>DeepDoc</td><td>Tesseract</td><td>Docling dans le conteneur</td><td>Docling sans OCR</td></tr>
<tr><td>Recherche</td><td>hybride</td><td>hybride, vecteurs 0,7</td><td>vecteurs</td><td>hybride</td><td>documents envoyés en entier</td></tr>
<tr><td>Passages envoyés au modèle</td><td>10</td><td>8</td><td>8</td><td>3</td><td>tous</td></tr>
<tr><td>Reranker</td><td>bge-reranker-v2-m3</td><td></td><td>MiniLM</td><td>bge-reranker-v2-m3</td><td></td></tr>
<tr><td>Exactes /34</td><td>34</td><td>34</td><td>34</td><td>31</td><td>28</td></tr>
<tr><td>dont faits simples /13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td></tr>
<tr><td>dont tableaux /10</td><td>10</td><td>10</td><td>10</td><td>10</td><td>10</td></tr>
<tr><td>dont scan /4</td><td>4</td><td>4</td><td>4</td><td>4</td><td></td></tr>
<tr><td>dont anglais /2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td></tr>
<tr><td>dont multi-documents /3</td><td>3</td><td>3</td><td>3</td><td>2</td><td>1</td></tr>
<tr><td>dont audio /2</td><td>2</td><td>2</td><td>2</td><td></td><td>2</td></tr>
<tr><td>Pièges refusés /4</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
<tr><td>Bon document cité /34</td><td>34</td><td>34</td><td>34</td><td>32</td><td>29</td></tr>
<tr><td>Temps médian</td><td>24,0 s</td><td>7,8 s</td><td>10,7 s</td><td>22,0 s</td><td>8,7 s</td></tr>
<tr><td>Temps p95</td><td>86,9 s</td><td>56,9 s</td><td>37,6 s</td><td>38,7 s</td><td>27,9 s</td></tr>
<tr><td>Mémoire de l'application</td><td>3,6 Go</td><td>5,1 Go</td><td>1,6 Go</td><td>1,7 Go</td><td>4,7 Go</td></tr>
<tr><td>Résultat brut</td><td><a href="https://github.com/floSa/OpenWebUI-Test-Bench/blob/main/outils/resultats/open-webui/banc-2026-11-13-taches.json">JSON</a></td><td><a href="https://github.com/floSa/RAGFlow-Test-Bench/blob/main/outils/resultats/ragflow/banc-2026-11-12-hybride-vecteurs07-top8.json">JSON</a></td><td><a href="https://github.com/floSa/AnythingLLM-Test-Bench/blob/main/outils/resultats/anythingllm/banc-2026-11-12-top8-rerank-natif.json">JSON</a></td><td><a href="https://github.com/floSa/Kotaemon-Test-Bench/blob/main/outils/resultats/kotaemon/banc-2026-11-12-docling-rerank-serre-top3.json">JSON</a></td><td><a href="https://github.com/floSa/Open-Notebook-Test-Bench/blob/master/outils/resultats/open-notebook/banc-2026-11-12-central-chat.json">JSON</a></td></tr>
</table>

Une case vide pour le scan ou l'audio : la solution ne lit pas ce document ; ses questions comptent comme manquées dans « Exactes /34 ».

Sens des lignes :

- Exactes : la réponse contient la bonne valeur (exemple : « 48,6 » pour le chiffre d'affaires).
- Pièges refusés : sur les 4 questions dont la réponse n'est pas dans le corpus, l'outil dit ne pas savoir au lieu d'inventer.
- Bon document cité : la source affichée sous la réponse est le bon document.
- Temps p95 : 95 % des réponses arrivent en moins de ce temps.
- Mémoire de l'application : pic mesuré pendant le banc, conteneurs de la solution seulement (le service de modèles, commun aux cinq, n'est pas compté).

Corpus : 9 documents d'une entreprise fictive, Vélanor (PDF texte, PDF scanné, PDF en anglais, DOCX, PPTX, XLSX, HTML, Markdown, message vocal MP3). Questions : [corpus/questions.json](../corpus/questions.json), 34 avec réponse et 4 pièges.
