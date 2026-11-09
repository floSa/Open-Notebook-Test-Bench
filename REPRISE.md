# Reprise

État au 9 novembre 2026. Ce qui tourne, ce qui reste à faire, et comment lancer la solution suivante.

## 1. État

| Élément | État |
|---|---|
| Machine | nouveau portable : Ryzen 5 9600X, RTX 4060 Ti 16 Go de VRAM, plus de 30 Go de RAM, WSL2 |
| Open Notebook 1.15.1 | en marche : http://127.0.0.1:8502, mot de passe dans `donnees/IDENTIFIANTS-LOCAUX.txt` ; branché sur le GPU (vLLM) |
| Modèles | LLM-Service (`LLM_SERVICE_DIR`, par défaut `~/mes_projets/Projet-IA/LLM-Service`), branche `service-vllm` : conteneurs `vllm-central` (Gemma 4 E4B, checkpoint officiel Google QAT w4a16) et `vllm-embed` (bge-m3), réseau `llm-net` |
| Banc GPU (Docling actif) | chat : 28/34 justes, 4/4 refus, médiane 1,86 s ; Demander : 28/34, médiane 7,7 s ; détails dans `docs/open-notebook/10-qualite-performances.md` section 5 (profil B) |
| Banc CPU (profil A, machine précédente) | 28/34 justes, 4/4 refus, médiane 7,4 s — inchangé, conservé comme référence |
| VRAM | 15,7 Go sur 16,4 Go utilisés par vLLM (chat + embedding) — marge faible |
| Git | branche `master`, à jour avec `origin` (poussé) |

Écart volontaire par rapport au plan précédent : le modèle GPU prévu était Qwen3-4B-Instruct en 4 bits (pour comparer au même modèle que le CPU). LLM-Service avait déjà basculé, pour d'autres projets, sur **Gemma 4 E4B** comme modèle partagé par défaut (déjà en cache, ~11,5 Go) — repris tel quel plutôt que de télécharger un second modèle rien que pour ce banc. L'architecture du socle (une branche Git par moteur, mêmes noms de modèles des deux côtés, bascule par `git switch` + `make up`) a été gardée telle quelle : refondre en un seul flag configurable reste possible mais n'a pas semblé utile pour l'instant.

## 2. À faire tout de suite

1. **Un `git stash` non résolu existe sur LLM-Service**, branche `service-ollama` (message : « etat avant bascule service-vllm (modifs non commitees trouvees sur service-ollama) »). Trouvé en arrivant sur cette machine : des modifications non commitées ressemblant à une fusion partielle vers vLLM, mises de côté sans perte pour pouvoir basculer proprement. À relire (`git stash show -p` dans ce dépôt) et décider : les reprendre, ou les jeter si elles sont obsolètes.
2. `ollama-central` est arrêté (conflit GPU avec vLLM, un seul moteur à la fois sur 16 Go). Pour revenir au profil CPU : `docker stop vllm-central vllm-embed` puis relancer avec `outils/open-notebook/installer.sh` (sans `MOTEUR=vllm`).

## 3. Reste à mesurer

| Tâche | Pourquoi |
|---|---|
| Qwen3-4B-Instruct en 4 bits sur vLLM, pour une comparaison CPU/GPU à modèle identique | aujourd'hui, le profil GPU utilise un autre modèle (Gemma 4 E4B, voir ci-dessus) |
| Carte graphique à 8 Go de VRAM (plutôt que les 16 Go de cette machine) | situer le minimum réel ; la configuration actuelle utilise déjà 15,7 Go sur 16,4 |
| Banc avec un modèle de moins de 3 milliards de paramètres (par exemple qwen3:1.7b), sur CPU | situer le modèle le plus léger qui garde des réponses justes |
| OCR des scans : `onnxruntime` dans le conteneur d'Open Notebook (décision D3) | les 6 erreurs du banc viennent toutes du scan, sur CPU comme sur GPU |

## 4. Lancer RAGFlow dans un nouveau dossier

Le corpus, le banc et les outils communs doivent être identiques d'une solution à l'autre : on les copie depuis ce dépôt.

```bash
~/mes_projets/Tutoriels/Open-Notebook-Test-Bench/outils/communs/nouvelle_solution.sh ~/mes_projets/Tutoriels/RAGFlow-Test-Bench
```

```bash
cd ~/mes_projets/Tutoriels/RAGFlow-Test-Bench && claude --permission-mode auto
```

Le dossier `kit/` (consignes de mission par solution) a été retiré de ce dépôt et distribué à part (voir le journal de commit). Récupérer `kit-ragflow.zip` avant de lancer RAGFlow.

Déjà dans ce dépôt, à réutiliser tel quel :

- les modèles viennent de LLM-Service : aucune solution n'embarque son propre serveur de modèles ; deux branches (`service-ollama`, `service-vllm`), mêmes noms de modèles des deux côtés ;
- même taille de contexte pour toutes les applications et pour le juge du banc ;
- une page `docs/<solution>/presentation.md` au format de celle d'Open Notebook ;
- un `README.md` au format des autres bancs d'essai, et un fichier `LICENSE` ;
- deux configurations minimales mesurées, sans et avec GPU.

Points à surveiller pour RAGFlow : 16 Go de RAM conseillés pour lui seul ; Elasticsearch peut demander un réglage système (`vm.max_map_count`) que l'agent n'a pas le droit de faire (`sysctl` interdit) : prévoir le moteur Infinity, ou faire ce réglage soi-même.

## 5. Décisions en attente

| N° | Sujet | À décider |
|---|---|---|
| D2 | Conteneurs `rag-ollama`, `rag-agent-api`, `rag-frontend` du projet `~/mes_projets/.../rag-agent-chat` (ancienne machine) | sans objet sur cette machine ; à vérifier sur l'ancienne si elle est reprise |
| D3 | OCR de Docling inopérant dans l'image 1.15.1 | autoriser l'installation d'`onnxruntime` dans le conteneur |
