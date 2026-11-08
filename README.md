# Manuels vérifiés de solutions de RAG local

Série de manuels pratiques, en français, pour installer et utiliser sous Windows 11 et WSL2 des alternatives locales à NotebookLM. Chaque affirmation a été vérifiée sur une machine réelle : commandes exécutées, mesures, captures.

Solution traitée à ce jour : **Open Notebook 1.15.1** ([index des manuels](docs/open-notebook/README.md), [rapport de mission](RAPPORT-open-notebook.md)).

## Ce qu'on y apprend

- installer la solution en local, ports fermés au réseau, mot de passe actif ;
- la brancher à des modèles locaux (Ollama, serveur de voix) ;
- importer des documents, interroger, vérifier les citations ;
- mesurer la qualité des réponses et les performances sur un banc commun ;
- exploiter, sauvegarder, dépanner.

## Objectif et lecture

| Objectif | Lire |
|---|---|
| Choisir une solution | [docs/README.md](docs/README.md) (comparatif du banc) |
| Installer Open Notebook | [01. Installation](docs/open-notebook/01-installation.md) |
| Prendre en main | [02. Prise en main](docs/open-notebook/02-prise-en-main.md) |
| Automatiser par l'API | [08. API REST et MCP](docs/open-notebook/08-api-et-mcp.md) |
| Comprendre les termes | [glossaire](docs/glossaire.md) |
| Savoir comment les manuels sont produits | [outils/README.md](outils/README.md) |

## Arborescence

```text
docs/            manuels (un dossier par solution), glossaire, index et comparatif
outils/          scripts d'installation, d'essai, de mesure ; résultats bruts dans outils/resultats/
corpus/          documents fictifs (entreprise Vélanor) et questions de référence
exemples/        exemples courts et leurs sorties vérifiées
kit/             mission et fiches des solutions
donnees/         volumes et identifiants locaux (non versionné)
```

## Lancer un exemple

Open Notebook doit être démarré (`outils/open-notebook/demarrer.sh`). Puis :

```bash
bash exemples/open-notebook/01_etat_api.sh
```

Les sorties obtenues lors des essais sont dans [exemples/open-notebook/sorties_verifiees.txt](exemples/open-notebook/sorties_verifiees.txt).
