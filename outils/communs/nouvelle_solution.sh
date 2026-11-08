#!/usr/bin/env bash
# Prépare le dépôt d'une nouvelle solution à partir de ce banc : kit, corpus, outils communs, mesures du socle,
# résultats des bancs précédents (pour le comparatif), modèles de README et de présentation. Rien n'est poussé.
# Usage : outils/communs/nouvelle_solution.sh ~/Projets/Tutoriels/RAGFlow-Test-Bench
set -euo pipefail
SRC="$(cd "$(dirname "$0")/../.." && pwd)"
DEST="${1:?usage : nouvelle_solution.sh <dossier du nouveau dépôt>}"
[ -e "$DEST/.git" ] && { echo "$DEST est déjà un dépôt git : rien n'est copié"; exit 1; }
mkdir -p "$DEST"
R=(rsync -a --exclude __pycache__ --exclude '*.pyc')
"${R[@]}" "$SRC"/{kit,corpus,CLAUDE.md,.claude,.gitignore,LICENSE} "$DEST"/
mkdir -p "$DEST/outils/resultats"
"${R[@]}" "$SRC/outils/communs" "$DEST/outils/"
"${R[@]}" "$SRC/outils/resultats/socle" "$SRC/outils/resultats/machine" "$DEST/outils/resultats/"
# résultats des solutions déjà passées au banc, pour le tableau comparatif de docs/README.md
for d in "$SRC"/outils/resultats/*/; do
  s=$(basename "$d"); case "$s" in socle|machine) continue;; esac
  mkdir -p "$DEST/outils/resultats/$s"
  cp "$d"banc-*.json "$d"banc-*.md "$d"identite-github-*.json "$d"versions-*.json "$DEST/outils/resultats/$s/" 2>/dev/null || true
done
# empreintes du corpus identiques au banc d'origine
(cd "$DEST" && python3 - <<'PY'
import hashlib, json, pathlib
m = json.loads(pathlib.Path("corpus/MANIFEST.json").read_text())
for d in m["documents"]:
    h = hashlib.sha256(pathlib.Path("corpus/documents", d["fichier"]).read_bytes()).hexdigest()
    assert h == d["sha256"], d["fichier"]
print("corpus : empreintes conformes")
PY
)
cd "$DEST" && git init -q && git add -A && git commit -qm "Kit : prompt, fiches, outils communs, corpus et résultats repris du banc précédent"
echo "Dépôt prêt : $DEST ($(git -C "$DEST" ls-files | wc -l) fichiers suivis)"
