# Glossaire

Termes employés dans la série de manuels. Quand un terme est propre à une solution, elle est indiquée entre parenthèses.

| Terme | Définition simple |
|---|---|
| API REST | Interface qui permet à un programme d'envoyer des requêtes HTTP (GET, POST…) à une application, par exemple pour créer un carnet ou poser une question sans passer par l'interface. |
| Base URL | Adresse de départ d'un service d'API, par exemple `http://ollama-central:11434`. |
| Budget de contexte | Nombre de jetons qu'un modèle accepte en une fois, réparti entre les consignes, les passages retrouvés, l'historique et la réponse. |
| Carnet (notebook) | Espace de travail qui regroupe des sources, des notes et des conversations sur un même sujet (Open Notebook). |
| Chunk, passage | Morceau de texte issu du découpage d'un document ; c'est l'unité retrouvée par la recherche. |
| Citation | Renvoi, dans une réponse, vers la source ou le passage qui la justifie. |
| Compose (Docker Compose) | Outil qui démarre plusieurs conteneurs décrits dans un fichier `docker-compose.yml` ou `compose.yml`. |
| Conteneur | Programme isolé lancé par Docker à partir d'une image. |
| CPU, GPU | Processeur central ; carte graphique. Les modèles de langage sont bien plus rapides sur un GPU NVIDIA. |
| Découpage (chunking) | Opération qui coupe un document en passages de taille fixe, avec un éventuel recouvrement. |
| Embedding, plongement | Vecteur de nombres qui représente le sens d'un texte ; deux textes proches ont des vecteurs proches. |
| Empreinte d'image (digest) | Identifiant `sha256:…` qui désigne une image Docker exacte, contrairement à une étiquette comme `latest`, qui peut changer. |
| GGUF | Format de fichier de modèle quantifié utilisé par llama.cpp et Ollama. |
| Jeton (token) | Unité de texte manipulée par un modèle, environ trois quarts de mot en français. |
| LLM, SLM | Grand modèle de langage ; petit modèle de langage (quelques milliards de paramètres), adapté à une machine ordinaire. |
| MCP (Model Context Protocol) | Protocole qui permet à un assistant (client MCP) d'appeler les fonctions d'une application (serveur MCP). |
| Modèle de raisonnement | Modèle qui produit une réflexion intermédiaire avant sa réponse ; plus lent, parfois plus juste. |
| `num_ctx` | Taille de contexte d'un modèle dans Ollama, en jetons. Au-delà, le début du prompt est tronqué. |
| Ollama | Serveur de modèles local, qui fonctionne sur CPU ou GPU et expose une API. |
| OpenAPI, `/docs` | Description machine d'une API REST, souvent affichée comme page interactive à l'adresse `/docs`. |
| Podcast (Open Notebook) | Épisode audio généré à partir des sources d'un carnet, avec un ou plusieurs locuteurs synthétiques. |
| Profil d'épisode, profil de locuteur | Réglages d'un podcast : modèle, durée, consignes ; voix et personnalité de chaque locuteur (Open Notebook). |
| Quantification | Réduction de la précision des poids d'un modèle (par exemple 4 bits) pour qu'il occupe moins de mémoire. |
| RAG (génération augmentée par récupération) | Méthode qui retrouve des passages pertinents dans des documents, puis les donne au modèle pour qu'il réponde à partir d'eux. |
| Recherche hybride | Combinaison de la recherche plein texte (mots exacts) et de la recherche vectorielle (sens). |
| Recherche plein texte | Recherche par mots, comme un moteur de recherche classique. |
| Recherche vectorielle | Recherche par proximité de sens entre l'embedding de la question et ceux des passages. |
| Reranker | Modèle qui reclasse les passages retrouvés pour mettre les plus pertinents en tête. |
| Source (Open Notebook) | Document, page web, texte ou média ajouté à un carnet. |
| STT, TTS | Transcription de la parole en texte ; synthèse vocale du texte en parole. |
| SurrealDB | Base de données utilisée par Open Notebook pour les carnets, les sources et les vecteurs. |
| Top-k | Nombre de passages retrouvés et transmis au modèle. |
| Transformation (Open Notebook) | Consigne appliquée à une source pour produire une note (résumé, points clés, etc.). |
| vLLM | Serveur de modèles rapide pour GPU NVIDIA, compatible avec l'API d'OpenAI. Non utilisé sur la machine d'essai, qui n'a pas de GPU NVIDIA. |
| WSL2 | Sous-système Linux de Windows ; Docker Desktop y fait tourner ses conteneurs. |
