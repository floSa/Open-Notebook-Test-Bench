#!/usr/bin/env bash
# Restaure une sauvegarde faite par sauvegarder.sh. Les données actuelles sont d'abord mises de côté
# dans donnees/open-notebook.avant-restauration-<date> (jamais supprimées par ce script).
set -euo pipefail
cd "$(dirname "$0")/../.."
A="${1:?usage : restaurer.sh donnees/sauvegardes/open-notebook-....tar.gz}"
[ -f "$A" ] || { echo "archive introuvable : $A"; exit 1; }
IMG="ollama/ollama@sha256:46399ef084d97b381955b5dc585c5d836dbe7ed3f79f170d1c04660fed511e3a"
outils/open-notebook/arreter.sh >/dev/null
COTE="open-notebook.avant-restauration-$(date +%Y%m%d-%H%M%S)"
docker run --rm --entrypoint mv -v "$PWD/donnees:/d" "$IMG" /d/open-notebook "/d/$COTE"
docker run --rm --entrypoint tar -v "$PWD/donnees:/d" "$IMG" -xzf "/d/${A#donnees/}" -C /d
# le cache Docling n'est pas dans l'archive : reprise de celui des données mises de côté (évite 6 Go de téléchargement)
docker run --rm --entrypoint sh -v "$PWD/donnees:/d" "$IMG" -c "[ -d /d/$COTE/notebook_data/.cache ] && [ ! -e /d/open-notebook/notebook_data/.cache ] && mv /d/$COTE/notebook_data/.cache /d/open-notebook/notebook_data/ || true"
outils/open-notebook/demarrer.sh >/dev/null
echo "restauré depuis $A ; anciennes données : donnees/$COTE"
