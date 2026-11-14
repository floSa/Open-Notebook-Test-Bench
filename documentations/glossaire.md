# Glossaire

Termes employés dans la série de manuels. Quand un terme est propre à une solution, elle est indiquée entre parenthèses.

| Terme | Définition simple |
|---|---|
| API REST | Interface qui permet à un programme d'envoyer des requêtes HTTP (GET, POST…) à une application, par exemple pour créer un carnet ou poser une question sans passer par l'interface. |
| Base URL | Adresse de départ d'un service d'API, par exemple `http://llm-central:8080/v1` pour le service LLM central. |
| Budget de contexte | Nombre de jetons qu'un modèle accepte en une fois, réparti entre les consignes, les passages retrouvés, l'historique et la réponse. |
| Carnet (notebook) | Espace de travail qui regroupe des sources, des notes et des conversations sur un même sujet (Open Notebook). |
| Chunk, passage | Morceau de texte issu du découpage d'un document ; c'est l'unité retrouvée par la recherche. |
| Citation | Renvoi, dans une réponse, vers la source ou le passage qui la justifie. |
| Compatible OpenAI | Se dit d'un service qui accepte les mêmes requêtes que l'API d'OpenAI (`/v1/chat/completions`, `/v1/embeddings`…) ; une application qui sait parler à OpenAI peut alors s'y brancher en changeant l'adresse. |
| Compose (Docker Compose) | Outil qui démarre plusieurs conteneurs décrits dans un fichier `docker-compose.yml` ou `compose.yml`. |
| Conteneur | Programme isolé lancé par Docker à partir d'une image. |
| CPU, GPU | Processeur central ; carte graphique. Les modèles de langage sont bien plus rapides sur un GPU NVIDIA. |
| Découpage (chunking) | Opération qui coupe un document en passages de taille fixe, avec un éventuel recouvrement. |
| Embedding, plongement | Vecteur de nombres qui représente le sens d'un texte ; deux textes proches ont des vecteurs proches. |
| Empreinte d'image (digest) | Identifiant `sha256:…` qui désigne une image Docker exacte, contrairement à une étiquette comme `latest`, qui peut changer. |
| GGUF | Format de fichier de modèle quantifié utilisé par llama.cpp (et donc par le service LLM central) et par Ollama. |
| Jeton (token) | Unité de texte manipulée par un modèle, environ trois quarts de mot en français. |
| LLM, SLM | Grand modèle de langage ; petit modèle de langage (quelques milliards de paramètres), adapté à une machine ordinaire. |
| MCP (Model Context Protocol) | Protocole qui permet à un assistant (client MCP) d'appeler les fonctions d'une application (serveur MCP). |
| Modèle de raisonnement, réflexion | Modèle qui produit une réflexion intermédiaire avant sa réponse ; plus lent, parfois plus juste. Le modèle `chat` du service LLM central réfléchit par défaut. |
| Noms fixes | Noms stables sous lesquels le service LLM central expose ses modèles, quel que soit le modèle réel : `chat` (réponse), `embed` (embedding), `rerank` (reranker), `transcribe` (transcription). |
| Ollama | Serveur de modèles local, qui fonctionne sur CPU ou GPU et expose une API. Utilisé dans les premiers essais de la série, remplacé depuis par le service LLM central. |
| OpenAPI, `/docs` | Description machine d'une API REST, souvent affichée comme page interactive à l'adresse `/docs`. |
| Podcast (Open Notebook) | Épisode audio généré à partir des sources d'un carnet, avec un ou plusieurs locuteurs synthétiques. |
| Profil d'épisode, profil de locuteur | Réglages d'un podcast : modèle, durée, consignes ; voix et personnalité de chaque locuteur (Open Notebook). |
| Quantification | Réduction de la précision des poids d'un modèle (par exemple 4 bits) pour qu'il occupe moins de mémoire. |
| RAG (génération augmentée par récupération) | Méthode qui retrouve des passages pertinents dans des documents, puis les donne au modèle pour qu'il réponde à partir d'eux. |
| Recherche hybride | Combinaison de la recherche plein texte (mots exacts) et de la recherche vectorielle (sens). |
| Recherche plein texte | Recherche par mots, comme un moteur de recherche classique. |
| Recherche vectorielle | Recherche par proximité de sens entre l'embedding de la question et ceux des passages. |
| Service LLM central | Service de modèles partagé par toutes les applications de la série (dépôt LLM-Service) : une seule adresse compatible OpenAI (`http://llm-central:8080/v1` depuis un conteneur, `http://127.0.0.1:8080/v1` depuis la machine), une clé, des noms fixes. Il tourne sur carte graphique NVIDIA ou, plus lentement, sur processeur seul. |
| Reranker | Modèle qui reclasse les passages retrouvés pour mettre les plus pertinents en tête. |
| Source (Open Notebook) | Document, page web, texte ou média ajouté à un carnet. |
| STT, TTS | Transcription de la parole en texte ; synthèse vocale du texte en parole. |
| SurrealDB | Base de données utilisée par Open Notebook pour les carnets, les sources et les vecteurs. |
| Top-k | Nombre de passages retrouvés et transmis au modèle. |
| Transformation (Open Notebook) | Consigne appliquée à une source pour produire une analyse (résumé, points clés, etc.), rangée dans l'onglet « Analyses » de la source. |
| vLLM | Serveur de modèles rapide pour GPU NVIDIA, compatible avec l'API d'OpenAI. Utilisé pour un banc GPU de la série le 9 novembre 2026, remplacé depuis par le service LLM central. |
| WSL2 | Sous-système Linux de Windows ; Docker Desktop y fait tourner ses conteneurs. |
