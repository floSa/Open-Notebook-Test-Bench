#!/usr/bin/env bash
# Démarre le service de modèles (LLM-Service), le serveur de voix, puis Open Notebook.
set -euo pipefail
cd "$(dirname "$0")/../.."
outils/communs/llm_service.sh >/dev/null
docker start rag-speaches >/dev/null
docker compose --env-file donnees/open-notebook/.env -f outils/open-notebook/officiel/docker-compose.yml \
  -f outils/open-notebook/compose.override.yml up -d
for i in $(seq 90); do curl -sf http://127.0.0.1:5055/health >/dev/null && break; sleep 2; done
echo "Interface : http://127.0.0.1:8502  (mot de passe : donnees/IDENTIFIANTS-LOCAUX.txt)"
