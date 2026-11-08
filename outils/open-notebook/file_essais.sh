#!/usr/bin/env bash
# File d'essais séquentielle (un seul appel au modèle à la fois : sur CPU, des essais parallèles fausseraient les latences).
# Chaque étape écrit son journal dans outils/resultats/open-notebook/. Usage : file_essais.sh etape1 etape2 ...
cd "$(dirname "$0")/../.."
R=outils/resultats/open-notebook; J=$(date +%F)
D=donnees/open-notebook/.env
compose() { docker compose --env-file "$D" -f outils/open-notebook/officiel/docker-compose.yml -f outils/open-notebook/compose.override.yml "$@"; }
attendre() { for i in $(seq 600); do curl -sf http://127.0.0.1:5055/health >/dev/null && return 0; sleep 2; done; return 1; }
ctx() { python3 outils/open-notebook/configurer.py --voix --num-ctx "$1" >/dev/null; }

for e in "$@"; do
  echo "##### $e — début $(date +%T)"
  case "$e" in
    docling)  # active Docling (OCR, images) : installation au démarrage, mesurée
      grep -q '^OPEN_NOTEBOOK_ENABLE_DOCLING=' "$D" || echo 'OPEN_NOTEBOOK_ENABLE_DOCLING=true' >> "$D"
      t0=$(date +%s); compose up -d 2>&1; attendre
      echo "API disponible après $(( $(date +%s) - t0 )) s"
      docker logs rag-open-notebook 2>&1 | grep -iE 'docling|install|uv pip|Downloading|Installed' | tail -20
      curl -s -H "Authorization: Bearer $(grep ^OPEN_NOTEBOOK_PASSWORD= $D | cut -d= -f2)" http://127.0.0.1:5055/api/capabilities; echo
      du -sh donnees/open-notebook/notebook_data
      docker stats --no-stream --format '{{.Name}} {{.MemUsage}}' rag-open-notebook ;;
    banc-docling)   python3 outils/open-notebook/banc.py --etiquette docling-qwen-fullcontent --reindexer ;;
    formats)        python3 outils/open-notebook/essai_formats.py --etiquette docling ;;
    recherche)      python3 outils/open-notebook/essai_recherche.py ;;
    transformations) python3 outils/open-notebook/essai_transformations.py ;;
    banc-ministral) python3 outils/open-notebook/banc.py --etiquette docling-ministral-fullcontent --modele ministral-3:3b ;;
    banc-ctx4096)   ctx 4096; python3 outils/open-notebook/banc.py --etiquette docling-qwen-fullcontent-ctx4096; ctx 16384 ;;
    banc-ask)       python3 outils/open-notebook/banc.py --etiquette docling-qwen-ask --mode ask ;;
    exemples)       bash exemples/open-notebook/lancer_tous.sh 01_etat_api.sh 02_creer_carnet_et_source.sh 03_poser_question.py 04_rechercher.sh 05_supprimer_carnet.sh ;;
    *) echo "étape inconnue : $e" ;;
  esac > >(tee "$R/essai-$J-$e.log") 2>&1
  echo "##### $e — fin $(date +%T)"
done
