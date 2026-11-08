# Open Notebook — manuels vérifiés

Alternative libre à NotebookLM : carnets de sources, chat avec citations, notes, transformations, recherche, podcasts. Installation locale sous Windows 11 et WSL2, branchée à des modèles locaux.

| Version décrite | Date des essais | Machine | Langue de l'interface |
|---|---|---|---|
| Open Notebook 1.15.1 (image `lfnovo/open_notebook:1.15.1`), SurrealDB 2.7.0, Ollama 0.30.7 sur CPU, Speaches 0.8.3 | 2026-11-08 | Intel Core Ultra 7 255H, 15,3 Go de RAM dans WSL, sans GPU NVIDIA (profil A) | français (suit la langue du navigateur) |

**Commencer par** : [Open Notebook en bref](presentation.md), qui dit ce que fait la solution, son identité (licence, activité du projet), une grille de comparaison critère par critère et les résultats des essais.

## Manuels

| N° | Manuel | Contenu |
|---|---|---|
| 00 | [Notions fondamentales](00-notions-fondamentales.md) | RAG, briques, particularités d'Open Notebook, schéma des services et des ports |
| 01 | [Installation sous Windows et WSL2](01-installation.md) | prérequis mesurés, socle Ollama, installation, ports, mémoire, mise à jour, désinstallation |
| 02 | [Prise en main](02-prise-en-main.md) | premier carnet, première source, première réponse citée |
| 03 | [Carnets, sources et formats](03-carnets-sources-formats.md) | ce qui est extrait de chaque format, OCR avec Docling, audio |
| 04 | [Chat et citations](04-chat-et-citations.md) | contexte par source, citations, troncature, modèles |
| 05 | [Notes et transformations](05-notes-et-transformations.md) | notes, transformations fournies et personnalisées |
| 06 | [Recherche](06-recherche.md) | plein texte, vectorielle, « Demander » |
| 07 | [Podcasts](07-podcasts.md) | profils, voix locales, français |
| 08 | [API REST et MCP](08-api-et-mcp.md) | automatisation, exemples, serveur MCP tiers |
| 09 | [Recettes](09-recettes.md) | cas d'usage de bout en bout |
| 10 | [Qualité et performances](10-qualite-performances.md) | banc de 38 questions, réglages, profils matériels |
| 11 | [Exploitation](11-exploitation.md) | sauvegarde, restauration, mise à jour, journaux, sécurité |
| 12 | [Dépannage et FAQ](12-depannage.md) | échecs réels et solutions |

Plan détaillé : [plan des manuels](plan-des-manuels.md). Termes : [glossaire](../glossaire.md).

## Parcours de lecture

| Objectif | Lire |
|---|---|
| Installer et essayer | 01, 02 |
| Comprendre avant de choisir | 00, 10 |
| Travailler sur ses documents | 02, 03, 04, 05, 06 |
| Automatiser | 08, 09 |
| Exploiter au quotidien | 11, 12 |

## Limites connues

- Citations au niveau de la source, sans page ni passage.
- Chat de carnet sans recherche : les sources choisies sont envoyées en entier au modèle.
- Tableaux des documents DOCX non extraits par le moteur par défaut ; scans illisibles sans Docling.
- Sur CPU, chaque nouvelle question sur un grand contexte coûte une lecture lente du prompt.

## Ce qui reste ouvert

Décisions laissées à l'utilisateur ; l'option la plus prudente a été appliquée en attendant (détail dans le journal de la mission, `JOURNAL.md`).

| Sujet | État dans ces manuels | Ce qui permettrait de conclure |
|---|---|---|
| Absence de GPU NVIDIA sur la machine d'essai | socle Ollama sur CPU ; vLLM non installé ; temps mesurés sur CPU | rejouer l'installation et le banc sur une machine avec GPU NVIDIA |
| OCR de Docling inopérant (`onnxruntime` absent de l'image 1.15.1) | le contrat scanné reste illisible ; contournement non essayé [À tester] | installer `onnxruntime` dans le conteneur, ou signaler le défaut au projet |
| Banc en mode **Demander** (Ask) | échantillon de six questions seulement, trop lent sur CPU ([Qualité et performances](10-qualite-performances.md)) | rejouer le banc Ask complet avec un GPU |
| Anciens conteneurs `rag-ollama`, `rag-agent-api`, `rag-frontend` d'un autre projet | laissés intacts, arrêtés ; le socle de cette série s'appelle `rag-socle-ollama` | les renommer ou les supprimer à la main |
| Image `ubuntu:24.04` tirée pendant le diagnostic | inutilisée, laissée en place | `docker image rm ubuntu:24.04` à la main si elle ne sert pas ailleurs |
| Serveur MCP tiers `open-notebook-mcp` 0.3.0 | `create_source` en échec ([API et MCP](08-api-et-mcp.md)) | version corrigée du serveur |
