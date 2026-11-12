#!/usr/bin/env bash
# Vérifie que les ports publiés sont liés à 127.0.0.1 et injoignables par l'adresse réseau de WSL.
# Sortie : outils/resultats/open-notebook/ports-<date>.txt
cd "$(dirname "$0")/../.."
S="outils/resultats/open-notebook/ports-$(date +%F).txt"
{
  echo "== $(date -Iseconds)"
  echo "-- ports publiés (docker ps)"
  docker ps --format '{{.Names}}  {{.Ports}}' | grep -E 'rag-open-notebook|llm-central|rag-speaches'
  ip_wsl=$(ip -4 -o addr show eth0 | awk '{print $4}' | cut -d/ -f1)
  echo "-- adresse de WSL : $ip_wsl"
  for port in 8502 5055 8080 8969; do
    l=$(curl -s -m 3 -o /dev/null -w '%{http_code}' "http://127.0.0.1:$port/")
    e=$(curl -s -m 3 -o /dev/null -w '%{http_code}' "http://$ip_wsl:$port/" || true)
    echo "port $port : 127.0.0.1 -> HTTP $l ; $ip_wsl -> HTTP $e (000 = refusé)"
  done
  echo "-- écoute 0.0.0.0 côté hôte (doit être vide)"
  docker ps --format '{{.Names}} {{.Ports}}' | grep -E '^(rag-open-notebook|llm-central|rag-speaches)' | grep -E '0\.0\.0\.0|\[::\]' || echo "(aucune)"
} | tee "$S"
