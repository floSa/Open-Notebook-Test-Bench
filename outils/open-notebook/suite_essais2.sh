#!/usr/bin/env bash
# Profil le plus serré : à 4096, le corpus entier en « full content » dépasse le contexte (erreur 502, banc ctx4096).
# Banc complet à 6144 : plus petit contexte où le corpus entier tient en « full content ».
cd "$(dirname "$0")/../.."
ctx() { python3 outils/open-notebook/configurer.py --voix --num-ctx "$1" >/dev/null; }
R=outils/resultats/open-notebook; J=$(date +%F)
echo "##### banc-ctx6144 — début $(date +%T)"
ctx 6144; python3 outils/open-notebook/banc.py --etiquette docling-qwen-fullcontent-ctx6144 > "$R/essai-$J-banc-ctx6144.log" 2>&1
# « Demander » à 4096 retiré : à 16384 déjà, une question dure 400 à 1 100 s et la sortie de stratégie peut atteindre
# 8192 jetons (coupée par ESPERANTO_LLM_TIMEOUT) ; elle ne tiendrait pas dans 4096 (journal, 2026-11-08 15:30).
ctx 16384
echo "##### fin $(date +%T)"
