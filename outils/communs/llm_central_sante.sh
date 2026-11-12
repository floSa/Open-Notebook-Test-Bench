#!/usr/bin/env bash
# Vérification (lecture seule) du service LLM central : liste les modèles puis, avec --essai, fait une requête par usage
# (chat, embed, rerank, transcribe). Ne démarre ni n'arrête rien : LLM-Service est géré à part.
# La clé est lue dans le .env du projet (LLM_CENTRAL_KEY), jamais affichée.
# Usage : outils/communs/llm_central_sante.sh [--essai] [fichier_audio]
set -euo pipefail
cd "$(dirname "$0")/../.."
[ -f .env ] || { echo ".env absent : copier .env.example en .env et renseigner LLM_CENTRAL_KEY" >&2; exit 1; }
set -a; . ./.env; set +a
URL="${LLM_CENTRAL_URL_HOTE:-http://127.0.0.1:8080/v1}"
[ -n "${LLM_CENTRAL_KEY:-}" ] || { echo "LLM_CENTRAL_KEY vide dans .env" >&2; exit 1; }
H="Authorization: Bearer $LLM_CENTRAL_KEY"
echo "== $URL/models"
curl -sf -m 10 -H "$H" "$URL/models" | python3 -c "import json,sys; [print(' ', m['id'], '(' + m.get('mode', '?') + ')') for m in json.load(sys.stdin)['data']]" \
  || { echo "service injoignable ou clé refusée" >&2; exit 1; }
[ "${1:-}" = "--essai" ] || exit 0
J='Content-Type: application/json'
echo "== chat (réflexion coupée pour l'essai)"
curl -s -m 120 -H "$H" -H "$J" "$URL/chat/completions" -d '{"model":"'"${LLM_CENTRAL_CHAT:-chat}"'","max_tokens":300,"chat_template_kwargs":{"enable_thinking":false},"messages":[{"role":"user","content":"Dis bonjour en un mot."}]}' \
  | python3 -c "import json,sys; print(' ', json.load(sys.stdin)['choices'][0]['message']['content'])"
echo "== embed"
curl -s -m 60 -H "$H" -H "$J" "$URL/embeddings" -d '{"model":"'"${LLM_CENTRAL_EMBED:-embed}"'","input":"bonjour"}' \
  | python3 -c "import json,sys; print('  dimensions :', len(json.load(sys.stdin)['data'][0]['embedding']))"
echo "== rerank"
curl -s -m 60 -H "$H" -H "$J" "$URL/rerank" -d '{"model":"'"${LLM_CENTRAL_RERANK:-rerank}"'","query":"capitale de la France","documents":["Paris est la capitale de la France.","Le chat dort."]}' \
  | python3 -c "import json,sys; [print('  doc', r['index'], 'score', round(r['relevance_score'], 2)) for r in json.load(sys.stdin)['results']]"
AUDIO="${2:-corpus/documents/message-vocal-production.mp3}"
if [ -f "$AUDIO" ]; then
  echo "== transcribe ($AUDIO)"
  curl -s -m 180 -H "$H" "$URL/audio/transcriptions" -F model="${LLM_CENTRAL_TRANSCRIBE:-transcribe}" -F file=@"$AUDIO" \
    | python3 -c "import json,sys; print(' ', json.load(sys.stdin)['text'][:200])"
fi
