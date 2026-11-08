#!/usr/bin/env bash
# Essai de sauvegarde puis de restauration : un carnet témoin créé après la sauvegarde doit disparaître,
# les carnets et sources d'avant doivent revenir. Sortie : outils/resultats/open-notebook/sauvegarde-restauration-<date>.txt
set -euo pipefail
cd "$(dirname "$0")/../.."
OUT="outils/resultats/open-notebook/sauvegarde-restauration-$(date +%F).txt"
etat() { .venv/bin/python - <<'PY'
import sys; sys.path.insert(0, "outils/open-notebook")
from client import OpenNotebook
on = OpenNotebook(); on.attendre_sante()
for n in sorted(on.get("/api/notebooks"), key=lambda n: n["name"]):
    print(f"  {n['name']} : {len(on.get('/api/sources?notebook_id=' + n['id'] + '&limit=100'))} sources")
PY
}
{
echo "# Essai de sauvegarde et de restauration, $(date -Iseconds)"
echo "## Avant sauvegarde"; etat
t0=$(date +%s); A=$(outils/open-notebook/sauvegarder.sh | awk '{print $1}'); t1=$(date +%s)
echo "## Sauvegarde : $A, $(du -h "$A" | cut -f1), $((t1-t0)) s (arrêt et redémarrage compris)"
.venv/bin/python -c "
import sys; sys.path.insert(0, 'outils/open-notebook')
from client import OpenNotebook
on = OpenNotebook(); on.attendre_sante(); on.post('/api/notebooks', {'name': 'Témoin après sauvegarde', 'description': 'doit disparaître'})"
echo "## Après création du carnet témoin"; etat
t0=$(date +%s); outils/open-notebook/restaurer.sh "$A"; t1=$(date +%s)
echo "## Restauration : $((t1-t0)) s"
echo "## Après restauration"; etat
echo "## Question de contrôle sur le carnet « Démo Vélanor »"
.venv/bin/python -c "
import sys, re; sys.path.insert(0, 'outils/open-notebook')
from client import OpenNotebook
on = OpenNotebook(); nb = next(n for n in on.get('/api/notebooks') if n['name'] == 'Démo Vélanor')
srcs = {s['id']: 'full content' for s in on.get('/api/sources?notebook_id=' + nb['id'] + '&limit=100')}
rep, sid, _ = on.demander(nb['id'], 'Quel est le prix public du modèle Erdre Cargo ?', srcs, titre='contrôle restauration')
print('  ', rep.replace(chr(10), ' ')); on.delete('/api/chat/sessions/' + sid)" 2>&1 | cut -c1-400
} 2>&1 | tee "$OUT"
