#!/usr/bin/env bash
# Arrête Open Notebook (données conservées). Option --voix : arrête aussi le serveur de synthèse vocale.
# Le service LLM central n'est jamais arrêté ici : il est partagé avec d'autres applications.
set -euo pipefail
cd "$(dirname "$0")/../.."
outils/open-notebook/compose.sh stop
[ "${1:-}" = --voix ] && docker stop rag-speaches >/dev/null && echo "serveur de voix arrêté"
echo "Open Notebook arrêté."
