#!/usr/bin/env bash
# État de l'API et authentification. Mot de passe : variable ON_MDP (sinon lu dans donnees/open-notebook/.env).
ON_MDP="${ON_MDP:-$(grep ^OPEN_NOTEBOOK_PASSWORD= "$(dirname "$0")/../../donnees/open-notebook/.env" | cut -d= -f2)}"
curl -s http://127.0.0.1:5055/health; echo
curl -s http://127.0.0.1:5055/api/auth/status; echo
echo "sans mot de passe : HTTP $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:5055/api/notebooks)"
echo "avec mot de passe : HTTP $(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $ON_MDP" http://127.0.0.1:5055/api/notebooks)"
