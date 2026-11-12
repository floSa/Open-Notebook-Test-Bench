# Outils

Principe : chaque valeur citée dans les manuels vient d'un script de ce dossier, et le résultat brut de ce script est gardé dans `resultats/`. Les scripts sont rejouables ; ils ne touchent qu'aux ressources Docker préfixées `rag-` et aux dossiers du dépôt.

## Communs

| Fichier | Rôle |
|---|---|
| `communs/diagnostic.sh` | Diagnostic de la machine (Windows, WSL, CPU, RAM, disque, GPU, Docker, accès réseau, port local) vers `resultats/machine/` |
| `communs/inventaire_modeles.py` | Inventaire en lecture seule des modèles déjà présents vers `resultats/socle/modeles-existants.json` |
| `communs/llm_central_sante.sh` | Santé du service LLM central (lecture seule) : liste des modèles, puis avec `--essai` une vraie requête `chat`, `embed`, `rerank` et `transcribe` ; clé lue dans `.env`, jamais affichée |
| `communs/llm_service.sh`, `communs/llm_service_vllm.sh` | Historique : démarraient l'ancienne pile (Ollama, vLLM) ; plus lancés |
| `communs/mesure_modeles.py` | Historique (ancienne pile Ollama) : débit, premier jeton, RAM, contexte vers `resultats/socle/` |
| `communs/generer_corpus.py` | Corpus fictif Vélanor (graine fixe, empreintes dans `corpus/MANIFEST.json`) |
| `communs/banc/commun.py` | Banc : notation, citations, latences, pics de RAM, juge LLM complémentaire (`chat` du service central, réflexion coupée), sorties JSON et Markdown |
| `communs/banc/tests/test_commun.py` | Auto-contrôle de la notation du banc |
| `communs/verifier_docs.py` | Vérification des manuels : liens, images, ancres, en-têtes, ton ; affiche le nombre de points |
| `communs/nettoyer.sh` | Suppression d'une solution (`<solution>`), et du serveur de voix avec `--socle` (LLM-Service jamais touché) ; jamais lancé automatiquement |
| `communs/voix.sh` | Serveur de voix Speaches (`rag-speaches`, `127.0.0.1:8969`) ; ne sert plus qu'à la synthèse vocale (Kokoro) des podcasts, la transcription passant par `transcribe` du service central |
| `communs/generer_audio.py` | Message vocal fictif du corpus (`corpus/documents/message-vocal-production.mp3`), produit par Speaches |
| `communs/identite_github.py` | Identité d'un dépôt GitHub (étoiles, forks, licence, commits, versions) par l'API publique, vers `resultats/<solution>/identite-github-<date>.json` |
| `communs/versions.py` | Dernière version stable de chaque composant (GitHub), comparée à la version utilisée, vers `resultats/<solution>/versions-<date>.json` |
| `communs/nouvelle_solution.sh` | Prépare le dépôt de la solution suivante : kit, corpus vérifié, outils communs, mesures, résultats des bancs précédents |
| `communs/banc/renoter.py` | Recalcul des notes d'un banc déjà joué, après correction de la notation |
| `communs/banc/tableau.py` | Tableau comparatif Markdown de tous les bancs d'un dossier de résultats |
| `communs/captures/lancer.sh` | Lancement d'un script de captures dans le conteneur Playwright officiel, sur le réseau `rag-local` |
| `communs/captures/annoter.py` | Annotation des captures : rectangle rouge, pastille numérotée, masquage des secrets, texte de la page enregistré |

## Open Notebook

| Fichier | Rôle |
|---|---|
| `open-notebook/officiel/` | Compose et exemple de configuration officiels, copiés tels quels (empreinte vérifiée par l'installateur) |
| `open-notebook/compose.override.yml` | Écarts à l'officiel : noms `rag-`, ports sur `127.0.0.1`, versions figées par empreinte, réseaux `rag-local` et `llm-net`, délais, transcription par le service central, synthèse vocale |
| `open-notebook/compose.sh` | Appel de `docker compose` (compose officiel + override, secrets de `donnees/open-notebook/.env`, clé du service central lue dans `.env`) |
| `open-notebook/installer.sh` | Installation complète : secrets, vérification du service central, voix, conteneurs, configuration des modèles |
| `open-notebook/configurer.py` | Fournisseur « OpenAI Compatible » vers le service central (`chat`, `embed`, `transcribe`), modèles par défaut, retrait des anciennes configurations ; `--voix` pour la synthèse vocale |
| `open-notebook/client.py` | Client Python minimal de l'API (authentification, sources, attente d'indexation, chat) |
| `open-notebook/demarrer.sh`, `arreter.sh`, `etat.sh` | Démarrage, arrêt (`--voix` pour arrêter aussi le serveur de voix), état résumé |
| `open-notebook/verifier_ports.sh` | Contrôle que les ports ne répondent que sur `127.0.0.1` |
| `open-notebook/verif_minimale.py` | Vérification minimale de bout en bout (carnet, source, question, citation) |
| `open-notebook/essai_formats.py`, `essai_recherche.py`, `essai_transformations.py`, `essai_chat.py`, `essai_podcast.py` | Essais par fonction, résultats dans `resultats/open-notebook/` |
| `open-notebook/bilan_podcast.py` | Bilan d'un épisode : script, fichier audio, transcription de contrôle |
| `open-notebook/banc.py` | Banc des 38 questions (modes chat et Demander), modèle `chat` du service central |
| `open-notebook/essai_contexte.py` | Dépassement volontaire du contexte de 16 384 jetons dans le chat |
| `open-notebook/demo.py` | Jeu de démonstration : carnet « Démo Vélanor », sources, conversations citées, notes |
| `open-notebook/sauvegarder.sh`, `restaurer.sh` | Sauvegarde à froid et restauration des données |
| `open-notebook/file_essais.sh`, `suite_essais.sh`, `suite_essais2.sh` | Enchaînements d'essais longs, tels que joués |
| `open-notebook/captures/carte.py` | Carte de l'interface : capture de repérage et inventaire des éléments de chaque page |
| `open-notebook/captures/manuel.py` | Scénarios du manuel utilisateur : actions à la souris et captures annotées, chapitre par chapitre |
| `open-notebook/captures/commun_on.py` | Session Playwright commune (connexion, capture annotée, accès à l'API) |
