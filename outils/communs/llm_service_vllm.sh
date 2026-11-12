#!/usr/bin/env bash
# HISTORIQUE : ancien service de modèles (Ollama/vLLM). Ce script démarre des conteneurs de LLM-Service, désormais géré à part : ne plus le lancer.
# Remplacé par outils/communs/llm_central_sante.sh (vérification en lecture seule du service LLM central).
# Service de modèles pour le banc GPU : LLM-Service (dépôt séparé, branche service-vllm).
# Deux conteneurs, un modèle chacun (vllm-central : chat, vllm-embed : embedding), réseau llm-net.
# Contrairement à Ollama, vLLM réserve sa VRAM au démarrage : un seul moteur à la fois sur le GPU
# (ce script refuse de démarrer si ollama-central tourne encore).
# Usage : outils/communs/llm_service_vllm.sh   (LLM_SERVICE_DIR pour un autre emplacement du dépôt)
set -euo pipefail
DIR="${LLM_SERVICE_DIR:-$HOME/mes_projets/Projet-IA/LLM-Service}"
if ! docker ps --format '{{.Names}}' | grep -qx vllm-central; then
  [ -f "$DIR/Makefile" ] || { echo "LLM-Service introuvable dans $DIR (branche service-vllm attendue)"; exit 1; }
  if docker ps --format '{{.Names}}' | grep -qx ollama-central; then
    echo "ollama-central tourne encore : un seul moteur à la fois sur le GPU, arrête-le d'abord (docker stop ollama-central)." >&2
    exit 1
  fi
  (cd "$DIR" && make up)
fi
for i in $(seq 120); do curl -sf "http://127.0.0.1:${VLLM_PORT:-8001}/health" >/dev/null && break; sleep 3; done
for i in $(seq 120); do curl -sf "http://127.0.0.1:${VLLM_EMBED_PORT:-8002}/health" >/dev/null && break; sleep 3; done
echo "LLM-Service (vLLM) : http://vllm-central:8000/v1 (chat), http://vllm-embed:8000/v1 (embedding) sur le réseau llm-net"
curl -s "http://127.0.0.1:${VLLM_PORT:-8001}/v1/models" | python3 -c "import json,sys; [print(' chat  ', m['id']) for m in json.load(sys.stdin)['data']]"
curl -s "http://127.0.0.1:${VLLM_EMBED_PORT:-8002}/v1/models" | python3 -c "import json,sys; [print(' embed ', m['id']) for m in json.load(sys.stdin)['data']]"
