#!/usr/bin/env bash
# docker compose pour Open Notebook : compose officiel figé + override du dépôt.
# Variables : donnees/open-notebook/.env (secrets locaux) puis service/.env du dépôt (clé LLM_CENTRAL_KEY du service central,
# jamais recopiée ailleurs). Usage : service/compose.sh up -d | stop | ps | logs …
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f service/.env ] || { echo "démarrer LLM-Service : copier service/.env.example en service/.env et y mettre la clé du service" >&2; exit 1; }
exec docker compose --env-file donnees/open-notebook/.env --env-file service/.env \
  -f service/officiel/docker-compose.yml -f service/compose.override.yml "$@"
