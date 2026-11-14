#!/usr/bin/env bash
# Supprime le carnet « Exemple API » et ses sources exclusives (nettoyage des exemples 02 et 03).
ON_MDP="${ON_MDP:-$(grep ^OPEN_NOTEBOOK_PASSWORD= "$(dirname "$0")/../../donnees/open-notebook/.env" | cut -d= -f2)}"
H="Authorization: Bearer $ON_MDP"; API=http://127.0.0.1:5055/api
NB=$(curl -s -H "$H" $API/notebooks | python3 -c 'import json,sys;print(next((n["id"] for n in json.load(sys.stdin) if n["name"]=="Exemple API"),""))')
[ -n "$NB" ] && curl -s -X DELETE -H "$H" "$API/notebooks/$NB?delete_exclusive_sources=true"; echo
