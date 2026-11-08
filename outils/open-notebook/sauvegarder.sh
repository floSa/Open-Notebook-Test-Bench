#!/usr/bin/env bash
# Sauvegarde à froid de donnees/open-notebook (base, fichiers, .env) dans donnees/sauvegardes/.
# Arrête l'application le temps de l'archive, puis la redémarre.
set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p donnees/sauvegardes
A="donnees/sauvegardes/open-notebook-$(date +%Y%m%d-%H%M%S).tar.gz"
IMG="ollama/ollama@sha256:46399ef084d97b381955b5dc585c5d836dbe7ed3f79f170d1c04660fed511e3a"  # image déjà présente, sert d'outil tar
outils/open-notebook/arreter.sh >/dev/null
# certains fichiers appartiennent à root (écrits par les conteneurs) : archive faite dans un conteneur jetable
docker run --rm --entrypoint tar -v "$PWD/donnees:/d" "$IMG" -czf "/d/${A#donnees/}" \
  --exclude=open-notebook/notebook_data/.cache -C /d open-notebook  # .cache : paquets et modèles Docling (6 Go), réinstallés au démarrage
docker run --rm --entrypoint chown -v "$PWD/donnees:/d" "$IMG" "$(id -u):$(id -g)" "/d/${A#donnees/}"
outils/open-notebook/demarrer.sh >/dev/null
echo "$A ($(du -h "$A" | cut -f1))"
