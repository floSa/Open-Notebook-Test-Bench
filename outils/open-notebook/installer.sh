#!/usr/bin/env bash
# Installation rejouable et idempotente d'Open Notebook 1.15.1, branché au socle Ollama.
# Journal : outils/resultats/open-notebook/installation-<date>.log
set -euo pipefail
cd "$(dirname "$0")/../.."
VERSION=v1.15.1
D="$PWD/donnees/open-notebook"
LOG="outils/resultats/open-notebook/installation-$(date +%F).log"
mkdir -p "$D/surreal_data" "$D/notebook_data" "$(dirname "$LOG")"
exec > >(tee -a "$LOG") 2>&1
echo "=== installation $(date -Iseconds)"
t0=$(date +%s)

# 1. compose officiel à la version figée (copie gardée dans le dépôt, empreinte vérifiée)
OFF=outils/open-notebook/officiel/docker-compose.yml
[ -f "$OFF" ] || curl -sfL "https://raw.githubusercontent.com/lfnovo/open-notebook/$VERSION/docker-compose.yml" -o "$OFF"
echo "8ef83d69d06a1b42ef8dc9598010e93a2147090031c57cef6b7f7f7d59e17034  $OFF" | sha256sum -c -

# 2. secrets générés localement, une seule fois
if [ ! -f "$D/.env" ]; then
  umask 077
  cat > "$D/.env" <<EOF
DONNEES=$D
OPEN_NOTEBOOK_ENCRYPTION_KEY=$(openssl rand -hex 32)
OPEN_NOTEBOOK_PASSWORD=$(openssl rand -hex 12)
SURREAL_USER=rag
SURREAL_PASSWORD=$(openssl rand -hex 16)
EOF
  echo "secrets générés dans donnees/open-notebook/.env"
fi
. "$D/.env"
ID=donnees/IDENTIFIANTS-LOCAUX.txt
if ! grep -q "Open Notebook" "$ID" 2>/dev/null; then
  cat >> "$ID" <<EOF
== Open Notebook (identifiants fictifs locaux, générés le $(date +%F)) ==
Interface : http://127.0.0.1:8502   API : http://127.0.0.1:5055   (OpenAPI : http://127.0.0.1:5055/docs)
Mot de passe (interface et en-tête Authorization: Bearer) : $OPEN_NOTEBOOK_PASSWORD
Clé de chiffrement (OPEN_NOTEBOOK_ENCRYPTION_KEY) : voir donnees/open-notebook/.env
SurrealDB (non publié) : utilisateur $SURREAL_USER, mot de passe dans donnees/open-notebook/.env
EOF
  chmod 600 "$ID"
fi

# 3. socle (Ollama, Speaches) puis démarrage
outils/communs/socle.sh >/dev/null
outils/communs/voix.sh >/dev/null   # Speaches : TTS et STT locaux (podcasts, sources audio)
docker compose --env-file "$D/.env" -f "$OFF" -f outils/open-notebook/compose.override.yml up -d
for i in $(seq 120); do curl -sf http://127.0.0.1:5055/health >/dev/null && break; sleep 2; done
curl -s http://127.0.0.1:5055/health; echo
for i in $(seq 60); do curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8502/ | grep -qE "200|307" && break; sleep 2; done
echo "interface : HTTP $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8502/)"

# 4. branchement au socle
python3 outils/open-notebook/configurer.py --voix "${@}"

# ports : uniquement 127.0.0.1
docker ps --filter name=rag-open-notebook --format '{{.Names}} {{.Ports}}'
echo "durée : $(( $(date +%s) - t0 )) s"
