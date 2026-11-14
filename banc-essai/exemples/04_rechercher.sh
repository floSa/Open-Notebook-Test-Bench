#!/usr/bin/env bash
# Recherche plein texte puis vectorielle dans tous les carnets ; affiche titre et score des 3 premiers résultats.
ON_MDP="${ON_MDP:-$(grep ^OPEN_NOTEBOOK_PASSWORD= "$(dirname "$0")/../../donnees/open-notebook/.env" | cut -d= -f2)}"
Q="${1:-}"; [ -n "$Q" ] || Q="prime d'intéressement"  # apostrophe hors de ${…} : bash la prendrait pour un guillemet
for mode in text vector; do
  echo "== $mode : $Q"
  python3 -c 'import json,sys;print(json.dumps({"query":sys.argv[1],"type":sys.argv[2],"limit":3,"search_sources":True,"search_notes":False}))' "$Q" "$mode" |
  curl -s -H "Authorization: Bearer $ON_MDP" -H 'Content-Type: application/json' -d @- http://127.0.0.1:5055/api/search |
  python3 -c 'import json,sys;[print(" ", r.get("title"), round(r.get("similarity") or r.get("relevance") or 0, 3)) for r in json.load(sys.stdin)["results"]]'
done
