# Open Notebook — banc d'essai et manuels vérifiés

**Interroger ses propres documents avec une IA qui cite ses sources, sur sa machine, sans service en ligne : Open Notebook 1.15.1 installé, branché sur un service de modèles local, mesuré sur 38 questions et décrit dans un manuel utilisateur vérifié.**

Trois dossiers : `service/` pour lancer Open Notebook, `banc-essai/` pour rejouer les tests, `documentations/` pour lire.

```text
Open-Notebook-Test-Bench/
├── README.md
├── LICENSE
│
├── service/                 lancer Open Notebook (Docker)
│   ├── installer.sh         première installation
│   ├── demarrer.sh
│   ├── arreter.sh
│   └── …                    état, sauvegarde, réglages
│
├── banc-essai/              rejouer les tests
│   ├── corpus/              9 documents et 38 questions
│   ├── open-notebook/       scripts du banc et des captures propres à Open Notebook
│   ├── communs/             outils partagés par les cinq bancs
│   ├── exemples/            appels à l'API, avec leurs sorties vérifiées
│   └── resultats/           scores et preuves brutes
│
└── documentations/          lire
    ├── README.md            sommaire du manuel
    ├── manuel/              le guide, chapitre par chapitre
    ├── annexes/             évaluation, matériel, API, exploitation
    ├── img/                 captures d'écran
    ├── index-serie.md       comparaison des cinq solutions
    ├── fiche-technique.md   architecture, réglages, versions, licences
    ├── rapport.md           bilan
    └── journal.md           avancement
```

Les fichiers locaux, ignorés par git, restent à la racine : `donnees/` (volumes et identifiants), `sources/` le cas échéant.

## Lancer le service

Prérequis : Docker, le service de modèles LLM-Service en marche, sa clé dans `service/.env` (copie de `service/.env.example`).

```bash
cd service
./installer.sh     # première fois seulement
./demarrer.sh
./arreter.sh
```

## Rejouer le banc

Le service doit tourner.

```bash
uv run python banc-essai/open-notebook/banc.py --etiquette central-chat
```

## Lire la documentation

| Besoin | Page |
|---|---|
| Utiliser Open Notebook pas à pas | [Manuel](documentations/README.md) |
| Installer | [Chapitre 02](documentations/manuel/02-installer-open-notebook.md) |
| Résultats détaillés du banc | [Annexe A1](documentations/annexes/A1-evaluation-qualite-et-performances.md) |
| Comparer aux quatre autres solutions | [Index de la série](documentations/index-serie.md) |
| Architecture, réglages, versions, licences | [Fiche technique](documentations/fiche-technique.md) |
| Bilan | [Rapport](documentations/rapport.md) |

## Résultats

Banc de 38 questions (34 avec réponse, 4 pièges), modèles du service central : Qwen3.5-4B avec réflexion, bge-m3, bge-reranker-v2-m3.

| Réglage | OCR | Recherche | Passages | Reranker | Exactes /34 | Pièges refusés /4 | Médiane | Pic RAM de l'application |
|---|---|---|---|---|---|---|---|---|
| défaut = meilleur |  | sources envoyées en entier | toutes |  | 28 | 4 | 8,7 s | 4,7 Go |

Les 6 erreurs viennent du contrat scanné, illisible : le Docling de l'image 1.15.1 n'a pas de moteur d'OCR (4 questions sur le scan, 2 multi-documents qui en dépendent).

Toutes les variantes : [annexe A1](documentations/annexes/A1-evaluation-qualite-et-performances.md). Méthode et preuves : [annexe A6](documentations/annexes/A6-rapport-d-essais.md). Bilan : [documentations/rapport.md](documentations/rapport.md). Comparaison avec les quatre autres solutions : [index de la série](documentations/index-serie.md).
