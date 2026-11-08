#!/usr/bin/env bash
# État : conteneurs, ports, santé de l'API et de l'interface, mémoire, modèles chargés.
cd "$(dirname "$0")/../.."
docker ps -a --filter name=rag-open-notebook --filter name=ollama-central --filter name=rag-speaches --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
echo "API /health : $(curl -s -m 5 http://127.0.0.1:5055/health || echo injoignable)"
echo "Interface   : HTTP $(curl -s -m 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:8502/)"
echo "Ollama      : $(curl -s -m 5 http://127.0.0.1:11434/api/version || echo injoignable)"
docker stats --no-stream --format 'table {{.Name}}\t{{.MemUsage}}\t{{.CPUPerc}}' rag-open-notebook rag-open-notebook-surrealdb ollama-central rag-speaches 2>/dev/null
curl -s -m 5 http://127.0.0.1:11434/api/ps | python3 -c "import json,sys;[print('chargé :',m['name'],m['size']//10**6,'Mo') for m in json.load(sys.stdin)['models']]" 2>/dev/null
