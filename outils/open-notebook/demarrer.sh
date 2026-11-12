#!/usr/bin/env bash
# Démarre Open Notebook et le serveur de synthèse vocale. Le service LLM central (LLM-Service) est vérifié, pas démarré :
# s'il ne répond pas, le lancer par ~/mes_projets/Projet-IA/LLM-Service/scripts/demarrer.sh.
set -euo pipefail
cd "$(dirname "$0")/../.."
outils/communs/llm_central_sante.sh >/dev/null || echo "attention : service LLM central injoignable (démarrer LLM-Service)" >&2
docker start rag-speaches >/dev/null
outils/open-notebook/compose.sh up -d
for i in $(seq 90); do curl -sf http://127.0.0.1:5055/health >/dev/null && break; sleep 2; done
echo "Interface : http://127.0.0.1:8502  (mot de passe : donnees/IDENTIFIANTS-LOCAUX.txt)"
