#!/usr/bin/env bash
# Supprime une solution installée par ce dépôt : conteneurs, volumes et réseau du projet compose rag-<solution>,
# puis ses données dans donnees/<solution>/. Option --socle : supprime aussi le socle (rag-socle-ollama, réseau rag-local,
# donnees/socle/, conteneur de voix rag-speaches s'il existe).
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
[ $socle = 1 ] && echo "              socle : rag-socle-ollama, rag-speaches, réseau rag-local, dossier donnees/socle/"
if [ $oui = 0 ]; then read -r -p "Confirmer (oui/non) ? " r; [ "$r" = oui ] || exit 1; fi

if [ -f "outils/$sol/compose.yml" ]; then
  docker compose -p "rag-$sol" -f "outils/$sol/compose.yml" down -v --remove-orphans || true
fi
# Les fichiers créés par les conteneurs appartiennent parfois à root : suppression via un conteneur jetable.
[ -d "donnees/$sol" ] && docker run --rm --entrypoint rm -v "$PWD/donnees:/d" "$OLLAMA_IMAGE" -rf "/d/$sol"

if [ $socle = 1 ]; then
  docker rm -f rag-socle-ollama rag-speaches 2>/dev/null || true
  docker network rm rag-local 2>/dev/null || echo "réseau rag-local encore utilisé : conservé"
  [ -d donnees/socle ] && docker run --rm --entrypoint rm -v "$PWD/donnees:/d" "$OLLAMA_IMAGE" -rf /d/socle
fi
echo "Terminé."
