#!/usr/bin/env bash
# Arrête Open Notebook (données conservées). Option --voix : arrête aussi le serveur de voix.
# LLM-Service n'est jamais arrêté ici : il est partagé avec d'autres applications.
set -euo pipefail
cd "$(dirname "$0")/../.."
docker compose --env-file donnees/open-notebook/.env -f outils/open-notebook/officiel/docker-compose.yml \
  -f outils/open-notebook/compose.override.yml stop
[ "${1:-}" = --voix ] && docker stop rag-speaches >/dev/null && echo "serveur de voix arrêté"
echo "Open Notebook arrêté."
