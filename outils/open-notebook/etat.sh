#!/usr/bin/env bash
# État : conteneurs, ports, santé de l'API, de l'interface et du service LLM central, mémoire de l'application.
cd "$(dirname "$0")/../.."
docker ps -a --filter name=rag-open-notebook --filter name=rag-speaches --filter name=llm-central --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
echo "API /health : $(curl -s -m 5 http://127.0.0.1:5055/health || echo injoignable)"
echo "Interface   : HTTP $(curl -s -m 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:8502/)"
echo "Service central : $(outils/communs/llm_central_sante.sh >/dev/null 2>&1 && echo joignable || echo injoignable)"
docker stats --no-stream --format 'table {{.Name}}\t{{.MemUsage}}\t{{.CPUPerc}}' rag-open-notebook rag-open-notebook-surrealdb rag-speaches 2>/dev/null
