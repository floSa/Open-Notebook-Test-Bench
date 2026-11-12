# Index de la série

## Solutions décrites

| Solution | Version décrite | Date des essais | Machine de test | Langue de l'interface | Manuel |
|---|---|---|---|---|---|
| Open Notebook | 1.15.1 | 2026-11-12 | Ryzen 5 9600X, 32 Go, RTX 4060 Ti 16 Go, WSL2 ; modèles du service LLM central (profil `gpu`) | français | [manuel](open-notebook/README.md), [présentation](open-notebook/presentation.md) |

Dépôt de chaque solution : `https://github.com/floSa/<Solution>-Test-Bench` (ici [Open-Notebook-Test-Bench](https://github.com/floSa/Open-Notebook-Test-Bench)).

## Comparatif du banc

Mêmes 38 questions ([corpus/questions.json](../corpus/questions.json)), même corpus fictif, mêmes modèles du service LLM central (`chat` = Qwen3.5-4B, réflexion activée, 16 384 jetons ; `embed` = bge-m3), même machine.

| Solution | Réglages | Exactes (34 questions avec réponse) | Refus corrects (4 pièges) | Bon document cité | Médiane | p95 | Indexation du corpus | Pic RAM de l'application | Détail |
|---|---|---|---|---|---|---|---|---|---|
| Open Notebook 1.15.1 | conversation de carnet, toutes les sources en contenu complet, Docling actif, pas de reranker possible | 28/34 | 4/4 | 29 | 8,7 s | 27,9 s | 65 s | 4,7 Go | [évaluation](open-notebook/annexes/A1-qualite-et-performances.md), [résultat brut](../outils/resultats/open-notebook/banc-2026-11-12-central-chat.json) |

Les 6 erreurs d'Open Notebook viennent toutes du PDF scanné, illisible faute d'OCR opérationnel dans l'image 1.15.1. Les autres solutions de la série seront ajoutées à ce tableau après leurs essais.

### Bancs sur l'ancienne pile (modèles différents, non comparable tel quel)

| Solution | Service de modèles | Modèle | Exactes | Refus | Médiane | Résultat brut |
|---|---|---|---|---|---|---|
| Open Notebook 1.15.1 | Ollama 0.40.15 sur processeur (8 novembre) | qwen3:4b-instruct | 28/34 | 4/4 | 7,4 s | [banc](../outils/resultats/open-notebook/banc-2026-11-08-docling-qwen-fullcontent-ollama040.json) |
| Open Notebook 1.15.1 | vLLM sur carte graphique (9 novembre) | Gemma 4 E4B | 28/34 | 4/4 | 1,9 s | [banc](../outils/resultats/open-notebook/banc-2026-11-09-gpu-vllm-docling.json) |

## Parcours de lecture conseillés

| Profil | Parcours |
|---|---|
| Découvrir le RAG local | [glossaire](glossaire.md), puis le chapitre « Découvrir » de chaque solution ([Open Notebook](open-notebook/manuel/01-decouvrir-open-notebook.md)) |
| Installer et essayer rapidement | chapitres 02 à 04 de chaque manuel ([Open Notebook](open-notebook/manuel/02-installer-open-notebook.md)) |
| Choisir entre solutions | comparatif ci-dessus, puis l'annexe A1 de chaque solution |

## Conventions

| Étiquette | Sens |
|---|---|
| [Vérifié] | observé ou mesuré sur la machine d'essai, à la date indiquée ; renvoie à un script et à un résultat brut de `outils/` |
| [Source] | lu dans la documentation officielle ou le code source, non essayé |
| [Estimation] | calcul non mesuré, avec son raisonnement |
| [À tester] | ni documenté ni essayé |
| [Testée] | commande exécutée pendant les essais |
| [Aide] | commande lue dans l'aide, non exécutée |

Les étiquettes ne figurent que dans la partie 2 des manuels (annexes) ; la partie 1 se lit sans elles. Les libellés de l'interface sont cités tels qu'affichés. Les données sont fictives (entreprise Vélanor).
