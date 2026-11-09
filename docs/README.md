# Index de la série

## Solutions décrites

| Solution | Version décrite | Date des essais | Machine de test | Langue de l'interface | Manuels |
|---|---|---|---|---|---|
| Open Notebook | 1.15.1 | 2026-11-08 | Intel Core Ultra 7 255H, 15,3 Go de RAM (WSL), sans GPU NVIDIA ; socle Ollama sur CPU | français (langue du navigateur) | [présentation](open-notebook/presentation.md), [index](open-notebook/README.md) |

## Comparatif du banc

Mêmes 38 questions ([corpus/questions.json](../corpus/questions.json)), même corpus fictif, même modèle (qwen3:4b-instruct sur Ollama 0.40.15, CPU, 8 fils de calcul), même machine.

Mode chat de carnet, toutes les sources en « full content », Docling actif, `num_ctx` 16384 [Vérifié] :

| Solution | Exactes (34 questions avec réponse) | Refus corrects (4 pièges) | Bon document cité | Médiane | p95 | Indexation du corpus | Pic RAM de l'application | Détail |
|---|---|---|---|---|---|---|---|---|
| Open Notebook 1.15.1 | 28/34 | 4/4 | 28 | 7,4 s | 24,2 s | 84 s | 3,0 Go | [Qualité et performances](open-notebook/10-qualite-performances.md) |

Les 6 erreurs d'Open Notebook viennent toutes du PDF scanné, illisible faute d'OCR opérationnel dans l'image 1.15.1. Les autres solutions de la série seront ajoutées à ce tableau après leurs essais.

## Parcours de lecture conseillés

| Profil | Parcours |
|---|---|
| Découvrir le RAG local | [glossaire](glossaire.md), puis les notions fondamentales de la solution ([Open Notebook](open-notebook/00-notions-fondamentales.md)) |
| Installer et essayer rapidement | installation puis prise en main ([Open Notebook](open-notebook/01-installation.md)) |
| Choisir entre solutions | comparatif ci-dessus, puis « Qualité et performances » de chaque solution |

## Conventions

| Étiquette | Sens |
|---|---|
| [Vérifié] | observé ou mesuré sur la machine d'essai, à la date indiquée ; renvoie à un script et à un résultat brut de `outils/` |
| [Source] | lu dans la documentation officielle ou le code source, non essayé |
| [Estimation] | calcul non mesuré, avec son raisonnement |
| [À tester] | ni documenté ni essayé |
| [Testée] | commande exécutée pendant les essais |
| [Aide] | commande lue dans l'aide, non exécutée |

Les libellés de l'interface sont cités tels qu'affichés. Les données sont fictives (entreprise Vélanor).
