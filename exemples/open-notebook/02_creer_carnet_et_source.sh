#!/usr/bin/env bash
# Crée un carnet, y ajoute un fichier (multipart, embedding demandé, traitement en tâche de fond) et attend la fin.
set -euo pipefail
ON_MDP="${ON_MDP:-$(grep ^OPEN_NOTEBOOK_PASSWORD= "$(dirname "$0")/../../donnees/open-notebook/.env" | cut -d= -f2)}"
API=http://127.0.0.1:5055/api; H="Authorization: Bearer $ON_MDP"
FICHIER="${1:-$(dirname "$0")/../../corpus/documents/cse-2025-10-14.md}"
NB=$(curl -s -H "$H" -H 'Content-Type: application/json' -d '{"name":"Exemple API","description":"créé par 02_creer_carnet_et_source.sh"}' $API/notebooks | python3 -c 'import json,sys;print(json.load(sys.stdin)["id"])')
echo "carnet : $NB"
SRC=$(curl -s -H "$H" -F type=upload -F "file=@$FICHIER" -F "notebooks=[\"$NB\"]" -F embed=true -F async_processing=true $API/sources | python3 -c 'import json,sys;print(json.load(sys.stdin)["id"])')
echo "source : $SRC"
for i in $(seq 120); do  # extraction puis embedding (tâche séparée) : attendre embedded_chunks > 0
  n=$(curl -s -H "$H" $API/sources/$SRC | python3 -c 'import json,sys;print(json.load(sys.stdin).get("embedded_chunks") or 0)')
  [ "$n" -gt 0 ] && break; sleep 3
done
echo "statut : $(curl -s -H "$H" $API/sources/$SRC/status | python3 -c 'import json,sys;print(json.load(sys.stdin)["status"])'), passages : $n"
