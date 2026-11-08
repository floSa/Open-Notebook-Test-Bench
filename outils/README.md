# Outils

Principe : chaque valeur citée dans les manuels vient d'un script de ce dossier, et le résultat brut de ce script est gardé dans `resultats/`. Les scripts sont rejouables ; ils ne touchent qu'aux ressources Docker préfixées `rag-` et aux dossiers du dépôt.

## Communs

| Fichier | Rôle |
|---|---|
| `communs/diagnostic.sh` | Diagnostic de la machine (Windows, WSL, CPU, RAM, disque, GPU, Docker, accès réseau, port local) vers `resultats/machine/` |
| `communs/inventaire_modeles.py` | Inventaire en lecture seule des modèles déjà présents vers `resultats/socle/modeles-existants.json` |
| `communs/socle.sh` | Socle de modèles : Ollama sur CPU (`rag-socle-ollama`, alias `rag-ollama`, réseau `rag-local`, `127.0.0.1:11434`), copie des modèles présents, téléchargement de ceux qui manquent |
| `communs/mesure_modeles.py` | Débit, premier jeton, RAM, contexte, dépassement volontaire vers `resultats/socle/mesures-<date>-passe<N>.json` (et `.log`) |
| `communs/generer_corpus.py` | Corpus fictif Vélanor (graine fixe, empreintes dans `corpus/MANIFEST.json`) |
| `communs/banc/commun.py` | Banc : notation, citations, latences, pics de RAM, sorties JSON et Markdown |
| `communs/banc/tests/test_commun.py` | Auto-contrôle de la notation du banc |
| `communs/verifier_docs.py` | Vérification des manuels : liens, images, ancres, en-têtes, ton ; affiche le nombre de points |
| `communs/nettoyer.sh` | Suppression d'une solution (`<solution>`), et du socle avec `--socle` ; jamais lancé automatiquement |
| `communs/voix.sh` | Service vocal Speaches (`rag-speaches`, `127.0.0.1:8969`) : synthèse Kokoro et transcription faster-whisper-small, sur CPU |
| `communs/generer_audio.py` | Message vocal fictif du corpus (`corpus/documents/message-vocal-production.mp3`), produit par Speaches |
| `communs/banc/renoter.py` | Recalcul des notes d'un banc déjà joué, après correction de la notation |
| `communs/banc/tableau.py` | Tableau comparatif Markdown de tous les bancs d'un dossier de résultats |
| `communs/captures/lancer.sh` | Lancement d'un script de captures dans le conteneur Playwright officiel, sur le réseau `rag-local` |

## Open Notebook

| Fichier | Rôle |
|---|---|
| `open-notebook/officiel/` | Compose et exemple de configuration officiels, copiés tels quels (empreinte vérifiée par l'installateur) |
| `open-notebook/compose.override.yml` | Écarts à l'officiel : noms `rag-`, ports sur `127.0.0.1`, versions figées par empreinte, réseau `rag-local`, délais, voix |
| `open-notebook/installer.sh` | Installation complète : secrets, socle, voix, conteneurs, configuration des modèles |
| `open-notebook/configurer.py` | Fournisseur Ollama, modèles et modèles par défaut ; `--voix` pour Speaches |
| `open-notebook/client.py` | Client Python minimal de l'API (authentification, sources, attente d'indexation, chat) |
| `open-notebook/demarrer.sh`, `arreter.sh`, `etat.sh` | Démarrage, arrêt (`--socle` pour arrêter aussi le socle), état résumé |
| `open-notebook/verifier_ports.sh` | Contrôle que les ports ne répondent que sur `127.0.0.1` |
| `open-notebook/verif_minimale.py` | Vérification minimale de bout en bout (carnet, source, question, citation) |
| `open-notebook/essai_formats.py`, `essai_recherche.py`, `essai_transformations.py`, `essai_chat.py`, `essai_podcast.py` | Essais par fonction, résultats dans `resultats/open-notebook/` |
| `open-notebook/bilan_podcast.py` | Bilan d'un épisode : script, fichier audio, transcription de contrôle |
| `open-notebook/banc.py` | Banc des 38 questions (modes chat et Ask) |
| `open-notebook/demo.py` | Jeu de démonstration : carnet « Démo Vélanor », sources, conversations citées, notes |
| `open-notebook/sauvegarder.sh`, `restaurer.sh` | Sauvegarde à froid et restauration des données |
| `open-notebook/file_essais.sh`, `suite_essais.sh`, `suite_essais2.sh` | Enchaînements d'essais longs, tels que joués |
| `open-notebook/captures/explorer.py` | Relevé des libellés et des routes de l'interface |
| `open-notebook/captures/captures.py` | Captures d'écran des manuels, par scénario |
