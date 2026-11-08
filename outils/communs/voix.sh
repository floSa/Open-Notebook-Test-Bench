#!/usr/bin/env bash
# Serveur de voix local compatible OpenAI (TTS et STT) : Speaches 0.8.3 sur CPU, conteneur rag-speaches.
# Relecture préalable : outils/resultats/open-notebook/relecture-speaches.md
# - image déjà présente (étiquette latest-cpu = 0.8.3-cpu, même empreinte) ;
# - STT : faster-whisper-small copié depuis le cache Hugging Face local (pas de téléchargement) ;
# - TTS : Kokoro-82M ONNX téléchargé à la demande (seul modèle de voix manquant) ;
# - port 127.0.0.1:8969 seulement ; interface Gradio désactivée ; joignable sous http://rag-speaches:8000/v1.
set -euo pipefail
cd "$(dirname "$0")/../.."
IMAGE="ghcr.io/speaches-ai/speaches:0.8.3-cpu@sha256:21e3df06d842fb7802ab470dd77c25f0e8c0d22950e8d8c6ae886e851af53ef8"
HF="donnees/socle/speaches-hf"
STT="models--Systran--faster-whisper-small"
TTS="speaches-ai/Kokoro-82M-v1.0-ONNX"
mkdir -p "$HF"
if [ ! -d "$HF/$STT" ] && [ -d "$HOME/.cache/huggingface/hub/$STT" ]; then
  cp -rL "$HOME/.cache/huggingface/hub/$STT" "$HF/" && echo "copie : $STT"
fi
docker network inspect rag-local >/dev/null 2>&1 || docker network create rag-local
if ! docker inspect rag-speaches >/dev/null 2>&1; then
  docker run -d --name rag-speaches --restart unless-stopped --network rag-local \
    -p 127.0.0.1:8969:8000 -v "$PWD/$HF:/home/ubuntu/.cache/huggingface/hub" \
    -e ENABLE_UI=false -e LOG_LEVEL=info "$IMAGE" >/dev/null
fi
docker start rag-speaches >/dev/null
for i in $(seq 90); do curl -sf http://127.0.0.1:8969/health >/dev/null && break; sleep 2; done
curl -s http://127.0.0.1:8969/v1/models | python3 -c "import json,sys;print('modèles :',[m['id'] for m in json.load(sys.stdin)['data']])"
curl -s http://127.0.0.1:8969/v1/models | grep -q "Kokoro" || { curl -s -X POST "http://127.0.0.1:8969/v1/models/$TTS"; echo; }
# le cache copié n'a pas la fiche du modèle : Speaches ne télécharge que les fichiers manquants (quelques Ko)
curl -s http://127.0.0.1:8969/v1/models | grep -q "faster-whisper-small" || { curl -s -X POST "http://127.0.0.1:8969/v1/models/Systran/faster-whisper-small"; echo; }
curl -s http://127.0.0.1:8969/v1/models | python3 -c "import json,sys;print('modèles :',[m['id'] for m in json.load(sys.stdin)['data']])"
