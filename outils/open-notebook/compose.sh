#!/usr/bin/env bash
# docker compose pour Open Notebook : compose officiel figé + override du dépôt.
# Variables : donnees/open-notebook/.env (secrets locaux) puis .env du dépôt (clé LLM_CENTRAL_KEY du service central,
# jamais recopiée ailleurs). Usage : outils/open-notebook/compose.sh up -d | stop | ps | logs …
set -euo pipefail
cd "$(dirname "$0")/../.."
[ -f .env ] || { echo "démarrer LLM-Service : copier .env.example en .env et y mettre la clé du service" >&2; exit 1; }
exec docker compose --env-file donnees/open-notebook/.env --env-file .env \
  -f outils/open-notebook/officiel/docker-compose.yml -f outils/open-notebook/compose.override.yml "$@"
