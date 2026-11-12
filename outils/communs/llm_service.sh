#!/usr/bin/env bash
# HISTORIQUE : ancien service de modèles (Ollama/vLLM). Ce script démarre des conteneurs de LLM-Service, désormais géré à part : ne plus le lancer.
# Remplacé par outils/communs/llm_central_sante.sh (vérification en lecture seule du service LLM central).
# Service de modèles commun à toutes les solutions : LLM-Service (dépôt séparé, branche service-ollama).
# Un seul Ollama (conteneur ollama-central, réseau llm-net, 127.0.0.1:11434) sert le chat et l'embedding
# à toutes les applications ; aucune solution n'embarque son propre serveur de modèles.
# Ce script démarre le service s'il est arrêté et vérifie que les modèles du banc sont présents.
# Usage : outils/communs/llm_service.sh   (LLM_SERVICE_DIR pour un autre emplacement du dépôt)
set -euo pipefail
DIR="${LLM_SERVICE_DIR:-$HOME/mes_projets/Projet-IA/LLM-Service}"
MODELES=(qwen3:4b-instruct bge-m3)
if ! docker ps --format '{{.Names}}' | grep -qx ollama-central; then
  [ -f "$DIR/docker-compose.yml" ] || { echo "LLM-Service introuvable dans $DIR (branche service-ollama attendue)"; exit 1; }
  (cd "$DIR" && docker network inspect llm-net >/dev/null 2>&1 || docker network create llm-net >/dev/null
   docker compose up -d)
fi
for i in $(seq 60); do curl -sf http://127.0.0.1:11434/api/version >/dev/null && break; sleep 3; done
present=$(docker exec ollama-central ollama list)
for m in "${MODELES[@]}"; do
  grep -q "^$m" <<<"$present" || { echo "téléchargement de $m dans LLM-Service"; docker exec ollama-central ollama pull "$m" >/dev/null; }
done
echo "LLM-Service : $(curl -s http://127.0.0.1:11434/api/version), http://ollama-central:11434 sur le réseau llm-net"
docker exec ollama-central ollama list
