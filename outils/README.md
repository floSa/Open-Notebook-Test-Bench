# Outils

Principe : chaque valeur citée dans les manuels vient d'un script de ce dossier, et le résultat brut de ce script est gardé dans `resultats/`. Les scripts sont rejouables ; ils ne touchent qu'aux ressources Docker préfixées `rag-` et aux dossiers du dépôt.

## Communs

| Fichier | Rôle |
|---|---|
| `communs/diagnostic.sh` | Diagnostic de la machine (Windows, WSL, CPU, RAM, disque, GPU, Docker, accès réseau, port local) vers `resultats/machine/` |
| `communs/inventaire_modeles.py` | Inventaire en lecture seule des modèles déjà présents vers `resultats/socle/modeles-existants.json` |
| `communs/socle.sh` | Socle de modèles : Ollama sur CPU (`rag-socle-ollama`, alias `rag-ollama`, réseau `rag-local`, `127.0.0.1:11434`), copie des modèles présents, téléchargement de ceux qui manquent |
| `communs/mesure_modeles.py` | Débit, premier jeton, RAM, contexte, dépassement volontaire vers `resultats/socle/mesures-<date>.json` |
| `communs/generer_corpus.py` | Corpus fictif Vélanor (graine fixe, empreintes dans `corpus/MANIFEST.json`) |
| `communs/banc/commun.py` | Banc : notation, citations, latences, pics de RAM, sorties JSON et Markdown |
| `communs/banc/tests/test_commun.py` | Auto-contrôle de la notation du banc |
| `communs/verifier_docs.py` | Vérification des manuels : liens, images, ancres, en-têtes, ton ; affiche le nombre de points |
| `communs/nettoyer.sh` | Suppression d'une solution (`<solution>`), et du socle avec `--socle` ; jamais lancé automatiquement |
