#!/usr/bin/env bash
# Suite de la file d'essais (lancée après file_essais.sh) : chat, échantillon « Demander », podcast, démonstration.
cd "$(dirname "$0")/../.."
R=outils/resultats/open-notebook; J=$(date +%F)
etape() { echo "##### $1 — début $(date +%T)"; shift; "$@" > >(tee "$R/essai-$J-$E.log") 2>&1; echo "##### fin $(date +%T)"; }
E=chat;      etape chat python3 outils/open-notebook/essai_chat.py
# échantillon d'une question par type (D4 : banc « Demander » complet trop long sur CPU)
E=banc-ask;  etape banc-ask python3 outils/open-notebook/banc.py --etiquette docling-qwen-ask-echantillon --mode ask --ids Q01,Q02,Q15,Q21,Q28,Q30,Q33,Q35
E=podcast;   etape podcast python3 outils/open-notebook/essai_podcast.py "Essai installation"
E=demo;      etape demo python3 outils/open-notebook/demo.py
