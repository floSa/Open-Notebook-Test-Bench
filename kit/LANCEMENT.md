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
| 1 | [Open Notebook](fiches/01-open-notebook.md) | La plus proche de NotebookLM, légère et stable. La première mission construit aussi le socle commun (vLLM, corpus de test, banc d'évaluation, outils) : mieux vaut le faire sur une installation simple. |
| 2 | [RAGFlow](fiches/02-ragflow.md) | La plus puissante sur les documents difficiles, mais lourde (16 Go de RAM) et en release candidate. Elle profite d'un socle déjà rodé. |
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

   Adapter à la RAM du PC : au moins 16 Go pour RAGFlow, en laissant 6 à 8 Go à Windows. Puis `wsl --shutdown`.
3. **Pilote NVIDIA** récent installé sous Windows (rien à installer dans WSL). Dans Ubuntu, `nvidia-smi` doit afficher la carte.
4. **Docker Desktop**, avec le backend WSL2 et l'intégration de la distribution Ubuntu activée (Settings, Resources, WSL integration). Test du GPU dans Ubuntu :

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
7. **Modèles déjà présents** : l'agent les cherche dans les dossiers usuels (Hugging Face, LM Studio, Ollama, côté WSL et côté Windows). S'ils sont ailleurs, remplacer `<chemin facultatif>` dans le bloc `/goal` par leur dossier. Seuls les formats Hugging Face (safetensors, AWQ, GPTQ) sont pleinement exploitables par vLLM.
8. **Espace disque** : `df -h ~` doit montrer au moins 150 Go libres (images Docker, modèles, données).
9. **Veille** : Windows, Paramètres, Système, Alimentation : mise en veille sur « Jamais » sur secteur pendant les missions. Docker Desktop reste ouvert.

<a id="kit"></a>

## 3. Installer le kit

Dans Ubuntu :

```bash
mkdir -p ~/manuels-rag-local && cd ~/manuels-rag-local
unzip /mnt/c/Users/<utilisateur>/Downloads/kit-manuels-rag-local.zip -d .
git init && git add -A && git commit -m "Kit : prompt, fiches et réglages"
```

Le dossier doit rester dans le système de fichiers de WSL (`~/…`), pas sous `/mnt/c` : les accès disque y sont bien plus rapides.

<a id="lancer"></a>

## 4. Lancer

```bash
cd ~/manuels-rag-local
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
- **Session fermée** (redémarrage, coupure) : `cd ~/manuels-rag-local && claude --continue --permission-mode auto`. L'objectif actif est restauré à la reprise, et l'agent repart du journal.
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

Les solutions déjà installées peuvent rester en marche : leurs ports sont distincts et elles partagent le même socle vLLM. Si la RAM manque, arrêter les précédentes avec leur `arreter.sh`.
