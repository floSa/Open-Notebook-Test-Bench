#!/usr/bin/env bash
# Socle de modèles en repli CPU : Ollama (pas de GPU NVIDIA sur la machine, voir JOURNAL D1).
# Idempotent. Copie (sans téléchargement) les modèles déjà présents dans ~/.ollama,
# télécharge seulement ceux qui manquent (bge-m3), démarre rag-socle-ollama sur 127.0.0.1:11434.
set -euo pipefail
cd "$(dirname "$0")/../.."

IMAGE="ollama/ollama@sha256:46399ef084d97b381955b5dc585c5d836dbe7ed3f79f170d1c04660fed511e3a"  # 0.30.7
SOURCE="${OLLAMA_SOURCE:-$HOME/.ollama/models}"
DEST="donnees/socle/ollama/models"
COPIER=(qwen3/4b-instruct ministral-3/3b)
TELECHARGER=(bge-m3)
CONTEXTE="${OLLAMA_CONTEXT_LENGTH:-8192}"

mkdir -p "$DEST/manifests/registry.ollama.ai/library" "$DEST/blobs"
for m in "${COPIER[@]}"; do
  man="$SOURCE/manifests/registry.ollama.ai/library/$m"
  [ -f "$man" ] || { echo "absent : $m"; continue; }
  mkdir -p "$DEST/manifests/registry.ollama.ai/library/$(dirname "$m")"
  cp --update=none "$man" "$DEST/manifests/registry.ollama.ai/library/$m"
  for dg in $(python3 -c "import json,sys;d=json.load(open(sys.argv[1]));print(' '.join([d['config']['digest']]+[l['digest'] for l in d['layers']]))" "$man"); do
    f="${dg/:/-}"
    [ -f "$DEST/blobs/$f" ] || { echo "copie $m $f"; cp "$SOURCE/blobs/$f" "$DEST/blobs/$f"; }
  done
done

docker network inspect rag-local >/dev/null 2>&1 || docker network create rag-local

if ! docker inspect rag-socle-ollama >/dev/null 2>&1; then
  docker run -d --name rag-socle-ollama --restart unless-stopped \
    --network rag-local --network-alias rag-ollama \
    -p 127.0.0.1:11434:11434 \
    -v "$PWD/$DEST:/root/.ollama/models" \
    -e OLLAMA_CONTEXT_LENGTH="$CONTEXTE" \
    -e OLLAMA_NUM_PARALLEL=2 \
    -e OLLAMA_MAX_LOADED_MODELS=2 \
    -e OLLAMA_KEEP_ALIVE=30m \
    "$IMAGE" >/dev/null
fi
docker start rag-socle-ollama >/dev/null
for i in $(seq 60); do curl -sf http://127.0.0.1:11434/api/version >/dev/null && break; sleep 1; done
curl -s http://127.0.0.1:11434/api/version; echo
for m in "${TELECHARGER[@]}"; do
  docker exec rag-socle-ollama ollama list | grep -q "^$m" || { docker exec rag-socle-ollama ollama pull "$m" >/dev/null 2>&1 && echo "téléchargé : $m"; }
done
docker exec rag-socle-ollama ollama list
