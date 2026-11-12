#!/usr/bin/env bash
# Sauvegarde à froid de donnees/open-notebook (base, fichiers, .env) dans donnees/sauvegardes/.
# Arrête l'application le temps de l'archive, puis la redémarre.
set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p donnees/sauvegardes
A="donnees/sauvegardes/open-notebook-$(date +%Y%m%d-%H%M%S).tar.gz"
IMG="lfnovo/open_notebook:1.15.1@sha256:e4e18f12653df5bf48674b7b187c4252be52238b4d706330fd30d9b177b95812"  # image de l'application, déjà présente : sert d'outil tar
outils/open-notebook/arreter.sh >/dev/null
# certains fichiers appartiennent à root (écrits par les conteneurs) : archive faite dans un conteneur jetable
docker run --rm --entrypoint tar -v "$PWD/donnees:/d" "$IMG" -czf "/d/${A#donnees/}" \
  --exclude=open-notebook/notebook_data/.cache -C /d open-notebook  # .cache : paquets et modèles Docling (6 Go), réinstallés au démarrage
docker run --rm --entrypoint chown -v "$PWD/donnees:/d" "$IMG" "$(id -u):$(id -g)" "/d/${A#donnees/}"
outils/open-notebook/demarrer.sh >/dev/null
echo "$A ($(du -h "$A" | cut -f1))"
