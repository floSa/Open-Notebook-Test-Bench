#!/usr/bin/env bash
# Arrête Open Notebook (données conservées). Option --socle : arrête aussi Ollama.
set -euo pipefail
cd "$(dirname "$0")/../.."
docker compose --env-file donnees/open-notebook/.env -f outils/open-notebook/officiel/docker-compose.yml \
  -f outils/open-notebook/compose.override.yml stop
[ "${1:-}" = --socle ] && docker stop rag-socle-ollama >/dev/null && echo "socle arrêté"
echo "Open Notebook arrêté."
