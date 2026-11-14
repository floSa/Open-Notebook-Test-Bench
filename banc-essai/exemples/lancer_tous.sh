#!/usr/bin/env bash
# Exécute chaque exemple et ajoute sa sortie réelle à sorties_verifiees.txt (le mot de passe n'est jamais affiché).
cd "$(dirname "$0")"
S=sorties_verifiees.txt
for f in "$@"; do
  { echo "===== $f — $(date -Iseconds)"; case "$f" in *.py) "${PYTHON:-python3}" "$f";; *) bash "$f";; esac 2>&1; echo "(code de sortie : $?)"; echo; } | tee -a "$S"
done
