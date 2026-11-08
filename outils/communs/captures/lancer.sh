#!/usr/bin/env bash
# Lance un script de captures Playwright dans le conteneur officiel (rien à installer dans WSL).
# Le conteneur est branché sur le réseau rag-local : les applications s'ouvrent par leur nom de conteneur.
# Le paquet Python playwright (même version que l'image) est installé une fois dans donnees/playwright/site.
# Usage : outils/communs/captures/lancer.sh <script.py relatif au dépôt> [arguments]
set -euo pipefail
cd "$(dirname "$0")/../../.."
IMAGE="mcr.microsoft.com/playwright/python:v1.64.1-noble@sha256:330d401ae23c905896a0c26c66c36fc971b621519e7b11b435a8328d7bf6e031"
mkdir -p donnees/playwright
if [ ! -d donnees/playwright/site/playwright ]; then
  docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD/donnees/playwright:/pw" "$IMAGE" \
    pip install -q --target /pw/site playwright==1.64.1
fi
docker run --rm --name rag-captures --network rag-local --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -e PYTHONPATH=/pw/site:/depot/outils/communs/captures -v "$PWD/donnees/playwright:/pw" -v "$PWD:/depot" -w /depot \
  "$IMAGE" python "$@"
