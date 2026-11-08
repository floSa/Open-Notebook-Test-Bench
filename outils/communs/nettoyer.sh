#!/usr/bin/env bash
# Supprime une solution installée par ce dépôt : conteneurs, volumes et réseau du projet compose rag-<solution>,
# puis ses données dans donnees/<solution>/. Option --socle : supprime aussi le serveur de voix (rag-speaches), le réseau rag-local et donnees/socle/.
# LLM-Service (ollama-central, réseau llm-net) n'est jamais touché : c'est un service partagé, dans un autre dépôt.
# Ne vise que des noms explicites : les conteneurs rag-* d'autres projets (ex. rag-ollama de rag-agent-chat) ne sont pas touchés.
# Jamais lancé automatiquement.
# Usage : outils/communs/nettoyer.sh <solution> [--socle] [--oui]
set -euo pipefail
cd "$(dirname "$0")/../.."
sol="${1:?usage : nettoyer.sh <solution> [--socle] [--oui]}"
[[ "$sol" =~ ^[a-z0-9-]+$ ]] || { echo "nom de solution invalide"; exit 1; }
# image déjà présente (socle) utilisée comme conteneur jetable
OLLAMA_IMAGE="ollama/ollama@sha256:46399ef084d97b381955b5dc585c5d836dbe7ed3f79f170d1c04660fed511e3a"
socle=0; oui=0
for a in "${@:2}"; do case "$a" in --socle) socle=1;; --oui) oui=1;; esac; done

echo "À supprimer : projet compose rag-$sol (conteneurs, volumes, réseau), dossier donnees/$sol/"
[ $socle = 1 ] && echo "              socle : rag-speaches, réseau rag-local, dossier donnees/socle/ (LLM-Service non touché)"
if [ $oui = 0 ]; then read -r -p "Confirmer (oui/non) ? " r; [ "$r" = oui ] || exit 1; fi

# fichiers compose de la solution : compose officiel figé puis override du dépôt
fichiers=()
for f in "outils/$sol/officiel/docker-compose.yml" "outils/$sol/compose.override.yml"; do [ -f "$f" ] && fichiers+=(-f "$f"); done
envf="donnees/$sol/.env"
if [ ${#fichiers[@]} -gt 0 ] && [ -f "$envf" ]; then
  docker compose -p "rag-$sol" --env-file "$envf" "${fichiers[@]}" down -v --remove-orphans || true
fi
# Les fichiers créés par les conteneurs appartiennent parfois à root : suppression via un conteneur jetable.
[ -d "donnees/$sol" ] && docker run --rm --entrypoint rm -v "$PWD/donnees:/d" "$OLLAMA_IMAGE" -rf "/d/$sol"

if [ $socle = 1 ]; then
  docker rm -f rag-speaches 2>/dev/null || true
  docker network rm rag-local 2>/dev/null || echo "réseau rag-local encore utilisé : conservé"
  [ -d donnees/socle ] && docker run --rm --entrypoint rm -v "$PWD/donnees:/d" "$OLLAMA_IMAGE" -rf /d/socle
fi
echo "Terminé."
