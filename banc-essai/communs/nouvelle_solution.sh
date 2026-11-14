#!/usr/bin/env bash
# Prépare le dépôt d'une nouvelle solution à partir de ce banc (le dernier terminé) et de l'archive du kit :
# consignes (kit/, CLAUDE.md, .claude/) tirées de l'archive à jour, corpus (empreintes vérifiées), outils communs,
# mesures du socle, résultats des bancs précédents (comparatif), modèles de README et de présentation.
# Rend les scripts exécutables, crée le premier commit et déclare origin ; rien n'est poussé ici.
# Usage : banc-essai/communs/nouvelle_solution.sh <dossier du nouveau dépôt> [archive du kit]
#   ex. banc-essai/communs/nouvelle_solution.sh ~/mes_projets/Tutoriels/Kotaemon-Test-Bench ~/mes_projets/Tutoriels/kit-manuels-rag-local.zip
set -euo pipefail
SRC="$(cd "$(dirname "$0")/../.." && pwd)"
DEST="${1:?usage : nouvelle_solution.sh <dossier du nouveau dépôt> [archive du kit]}"
KIT="${2:-$SRC/kit-manuels-rag-local.zip}"
[ -e "$DEST/.git" ] && { echo "$DEST est déjà un dépôt git : rien n'est copié"; exit 1; }
mkdir -p "$DEST"
# consignes à jour : kit/, CLAUDE.md et .claude/ de l'archive (le corpus et les outils viennent du banc source)
if [ -f "$KIT" ]; then
  python3 -I -c "
import sys, zipfile
z = zipfile.ZipFile(sys.argv[1])
for n in z.namelist():
    if n.startswith(('kit/', '.claude/')) or n == 'CLAUDE.md':
        z.extract(n, sys.argv[2])" "$KIT" "$DEST"
  cp "$KIT" "$DEST/"
else
  echo "archive du kit introuvable ($KIT) : consignes copiées depuis $SRC"
  cp -r "$SRC"/{kit,CLAUDE.md,.claude} "$DEST"/
fi
R=(rsync -a --exclude __pycache__ --exclude '*.pyc')
"${R[@]}" "$SRC"/{.gitignore,LICENSE} "$DEST"/
mkdir -p "$DEST/service"
"${R[@]}" "$SRC/service/.env.example" "$DEST/service/"
mkdir -p "$DEST/banc-essai"
"${R[@]}" "$SRC/banc-essai/corpus" "$DEST/banc-essai/"
mkdir -p "$DEST/banc-essai/resultats"
"${R[@]}" "$SRC/banc-essai/communs" "$DEST/banc-essai/"
"${R[@]}" "$SRC/banc-essai/resultats/socle" "$SRC/banc-essai/resultats/machine" "$DEST/banc-essai/resultats/"
# résultats des solutions déjà passées au banc, pour le tableau comparatif de documentations/index-serie.md
for d in "$SRC"/banc-essai/resultats/*/; do
  s=$(basename "$d"); case "$s" in socle|machine) continue;; esac
  mkdir -p "$DEST/banc-essai/resultats/$s"
  cp "$d"banc-*.json "$d"banc-*.md "$d"identite-github-*.json "$d"versions-*.json "$DEST/banc-essai/resultats/$s/" 2>/dev/null || true
done
# droits d'exécution (perdus par une archive zip)
find "$DEST/service" "$DEST/banc-essai" -name '*.sh' -exec chmod +x {} +
# empreintes du corpus identiques au banc d'origine
(cd "$DEST" && python3 -I - <<'PY'
import hashlib, json, pathlib
m = json.loads(pathlib.Path("banc-essai/corpus/MANIFEST.json").read_text())
for d in m["documents"]:
    h = hashlib.sha256(pathlib.Path("banc-essai/corpus/documents", d["fichier"]).read_bytes()).hexdigest()
    assert h == d["sha256"], d["fichier"]
print("corpus : empreintes conformes")
PY
)
nom="$(basename "$DEST")"
cd "$DEST" && git init -q -b main && git add -A && git commit -qm "Dépôt : corpus, outils communs et résultats repris du banc précédent ($(basename "$SRC"))"
git remote add origin "git@github.com-perso:floSa/$nom.git"
echo "Dépôt prêt : $DEST ($(git ls-files | wc -l) fichiers suivis) ; origin = git@github.com-perso:floSa/$nom.git (dépôt GitHub à créer vide)"
