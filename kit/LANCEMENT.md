# Lancer une mission

Ce kit fait écrire par Claude Code, sans surveillance, les manuels d'installation et d'utilisation d'une solution de RAG local, en testant tout sur la machine. Il contient :

- un prompt générique, `kit/PROMPT.md`, commun à toutes les solutions ;
- une fiche par solution dans `kit/fiches/`, qui contient la commande de lancement prête à coller ;
- les règles permanentes (`CLAUDE.md`) et les réglages de Claude Code (`.claude/settings.json`) : permissions, interdits, pas de mention de Claude dans les commits.

## Sommaire

1. [Ordre conseillé](#ordre)
2. [Préparation de la machine](#preparation)
3. [Installer le kit](#kit)
4. [Lancer](#lancer)
5. [Pendant l'exécution](#pendant)
6. [À la fin](#fin)
7. [Solution suivante](#suivante)

<a id="ordre"></a>

## 1. Ordre conseillé

| Ordre | Fiche | Pourquoi à ce rang |
|---|---|---|
| 1 | [Open Notebook](fiches/01-open-notebook.md) | La plus proche de NotebookLM, légère et stable. Faite le 8 novembre 2026 : elle a construit le corpus, le banc et les outils communs, repris tels quels par les suivantes. |
| 2 | [RAGFlow](fiches/02-ragflow.md) | La plus puissante sur les documents difficiles, mais lourde (16 Go de RAM conseillés pour elle seule). Version 1.0.0 finale depuis le 6 novembre 2026. |
| 3 | [Kotaemon](fiches/03-kotaemon.md) | Référence pour vérifier les citations dans le PDF. |
| 4 | [AnythingLLM](fiches/04-anythingllm.md) | Rapide ; sert de point de comparaison « simple ». |
| 5 | [Open WebUI](fiches/05-open-webui.md) | Interface généraliste ; utile si un usage multi-utilisateur est visé. |
| 6 | [SurfSense](fiches/06-surfsense.md) | En dernier : projet instable et réorienté vers d'autres usages. |

L'ordre se change librement : une fiche ne dépend pas des précédentes. La première mission lancée, quelle qu'elle soit, construit le socle.

<a id="preparation"></a>

## 2. Préparation de la machine (une seule fois, environ 30 minutes)

Ces étapes demandent des droits d'administrateur, que l'agent n'a pas. Tout le reste, il le fait seul.

1. **WSL2 et Ubuntu.** Dans PowerShell : `wsl --install -d Ubuntu-24.04`, puis `wsl --version` pour vérifier qu'il s'agit de WSL2.
2. **Mémoire donnée à WSL.** Créer ou compléter `%UserProfile%\.wslconfig` :

   ```ini
   [wsl2]
   memory=24GB
   swap=8GB
   ```

   Adapter à la RAM du PC, en laissant 6 à 8 Go à Windows (sur un portable de 24 Go, environ 16 Go pour WSL). Puis `wsl --shutdown`.
3. **GPU NVIDIA, facultatif.** Sans carte NVIDIA, les modèles tournent sur CPU (LLM-Service, branche `service-ollama`). Avec une carte : pilote récent sous Windows (rien à installer dans WSL) ; dans Ubuntu, `nvidia-smi` doit afficher la carte.
4. **Docker Desktop**, avec le backend WSL2 et l'intégration de la distribution Ubuntu activée (Settings, Resources, WSL integration). `docker compose version` doit répondre ; sinon redémarrer Docker Desktop. Test du GPU dans Ubuntu, s'il y en a un :

   ```bash
   docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
   ```

5. **Paquets de base** dans Ubuntu :

   ```bash
   sudo apt update && sudo apt install -y git python3-venv python3-pip jq curl unzip
   git config --global user.name "Prénom Nom"
   git config --global user.email "adresse@exemple.fr"
   ```

6. **Claude Code dans Ubuntu** : suivre la [documentation officielle](https://code.claude.com/docs/en/overview), lancer `claude` une fois pour se connecter, puis `claude update`.
7. **Service de modèles LLM-Service** (un seul pour toutes les applications) :

   ```bash
   cd ~/Projets/Projet-IA/LLM-Service && git switch service-ollama && cp .env.example .env
   ```

   Dans `.env` : `PRELOAD_MODELS=qwen3:4b-instruct bge-m3`, `OLLAMA_CONTEXT_LENGTH=16384`, `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_KEEP_ALIVE=30m`, `OLLAMA_FLASH_ATTENTION=0`, `OLLAMA_KV_CACHE_TYPE=f16`. Sans GPU, créer `docker-compose.override.yml` (non versionné) :

   ```yaml
   services:
     ollama-central:
       image: ollama/ollama:<dernière version stable>@sha256:<empreinte>
       deploy: !reset {}
       environment:
         - LLAMA_ARG_THREADS=8
         - LLAMA_ARG_THREADS_BATCH=8
   ```

   `LLAMA_ARG_THREADS` : nombre de cœurs performants du processeur ; sur un processeur hybride, sans ce réglage, la génération tombe à 0,4 jeton/s. Puis `make up`. Avec une carte NVIDIA : branche `service-vllm`.
8. **Espace disque** : `df -h ~` doit montrer au moins 150 Go libres (images Docker, modèles, données).
9. **Veille** : Windows, Paramètres, Système, Alimentation : mise en veille sur « Jamais » sur secteur pendant les missions. Docker Desktop reste ouvert.

<a id="kit"></a>

## 3. Installer le kit

Dans Ubuntu :

Un dépôt par solution, dans `~/Projets/Tutoriels/<Solution>-Test-Bench` (comme `Open-Notebook-Test-Bench`). Le kit, le corpus et les outils communs sont repris du banc précédent pour que les mesures restent comparables :

```bash
~/Projets/Tutoriels/Open-Notebook-Test-Bench/outils/communs/nouvelle_solution.sh ~/Projets/Tutoriels/RAGFlow-Test-Bench
```

Le script copie le kit, le corpus (empreintes vérifiées), les outils communs, les mesures du socle, les résultats des bancs précédents (pour le comparatif) et les modèles de README et de présentation (`kit/modeles/`), puis crée le premier commit.

Le dossier doit rester dans le système de fichiers de WSL (`~/…`), pas sous `/mnt/c` : les accès disque y sont bien plus rapides.

<a id="lancer"></a>

## 4. Lancer

```bash
cd ~/Projets/Tutoriels/RAGFlow-Test-Bench
claude --permission-mode auto
```

1. Au premier lancement, accepter de faire confiance au dossier : les permissions du kit ne s'appliquent qu'après cette confirmation.
2. Ouvrir la fiche voulue, copier le bloc de la section « Lancement » (il commence par `/goal`) et le coller dans Claude Code.

Le mode `auto` laisse l'agent travailler sans demander d'autorisation, avec un contrôle de sécurité en arrière-plan. La commande `/goal` le fait continuer tour après tour jusqu'à ce que le critère de fin soit atteint. Les autorisations écrites dans le `/goal` (images Docker, modèles, budget de téléchargement) évitent que le contrôle de sécurité bloque des actions prévues.

Pour ajuster les limites (taille des modèles, volume total téléchargé, nombre de tours), modifier les chiffres dans le bloc avant de le coller.

<a id="pendant"></a>

## 5. Pendant l'exécution

- Une mission dure plusieurs heures, davantage pour RAGFlow.
- Suivi : `JOURNAL.md` à la racine (une entrée par étape) et `git log --oneline`.
- **Limite d'usage atteinte** : l'objectif se met en pause, puis reprend quand la limite se réinitialise si la session est restée ouverte.
- **Session fermée** (redémarrage, coupure) : `claude --continue --permission-mode auto` depuis le dossier de la solution. L'objectif actif est restauré à la reprise, et l'agent repart du journal.
- Pour arrêter : `Échap`, ou `/goal clear` pour retirer l'objectif.

<a id="fin"></a>

## 6. À la fin

1. Lire `RAPPORT-<solution>.md` : ce qui a été installé, l'URL à ouvrir, ce qui est vérifié ou non, les décisions qui restent à prendre.
2. Ouvrir la solution dans le navigateur Windows à l'adresse indiquée (toujours `http://127.0.0.1:<port>`). Les identifiants locaux de démonstration sont dans `donnees/IDENTIFIANTS-LOCAUX.txt`.
3. Lire les manuels : `docs/<solution>/README.md` en est l'index. Ils s'ouvrent dans Typora et forment un coffre Obsidian valide si le dossier `docs/` est ouvert comme coffre.
4. Arrêter la solution : `outils/<solution>/arreter.sh`. La supprimer entièrement : `outils/communs/nettoyer.sh <solution>`.

<a id="suivante"></a>

## 7. Solution suivante

Nouvelle session (`/clear` dans Claude Code, ou relancer `claude --permission-mode auto`), puis coller le bloc `/goal` de la fiche suivante. Le socle (vLLM, modèles, corpus, banc) est réutilisé, et le comparatif de `docs/README.md` s'enrichit à chaque solution passée au banc.

Arrêter les solutions précédentes avant d'en lancer une nouvelle (`outils/<solution>/arreter.sh` dans leur dossier) : sur 16 Go, deux piles et le modèle ne tiennent pas ensemble. LLM-Service reste en marche : toutes les solutions le partagent.
