#!/usr/bin/env python3
"""Notes et transformations : intégrées (prompts en anglais) et personnalisée (en français).

1. liste des transformations fournies ; 2. « Simple Summary » appliquée à la FAQ (insight asynchrone) ;
3. création d'une transformation personnalisée en français, exécutée sur le rapport annuel ;
4. note manuelle, puis insight enregistré comme note.
Sortie : outils/resultats/open-notebook/transformations-<date>.json
"""
import datetime, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from client import RACINE, OpenNotebook

on = OpenNotebook()
res = {"date": datetime.datetime.now().isoformat(timespec="seconds")}
nb = next(n for n in on.get("/api/notebooks") if n["name"] == "Banc")
src = {s["title"]: s["id"] for s in on.get(f"/api/sources?notebook_id={nb['id']}&limit=100")}
trs = on.get("/api/transformations")
res["fournies"] = [{"name": t["name"], "title": t.get("title"), "apply_default": t.get("apply_default")} for t in trs]
print("fournies :", [t["name"] for t in trs])

# 2. transformation fournie sur une source (insight, tâche de fond)
simple = next(t for t in trs if t["name"] == "Simple Summary")
t0 = time.time()
r = on.post(f"/api/sources/{src['faq-sav.html']}/insights", {"transformation_id": simple["id"]})
ins = []
while time.time() - t0 < 900 and not ins:
    time.sleep(5)
    ins = on.get(f"/api/sources/{src['faq-sav.html']}/insights")
res["simple_summary_faq"] = {"reponse_api": r, "duree_s": round(time.time() - t0, 1), "insights": ins}
print("Simple Summary :", round(time.time() - t0, 1), "s ->", (ins[0]["content"][:300] if ins else "rien"))

# 3. transformation personnalisée en français (idempotent : réutilisée si elle existe)
perso = next((t for t in trs if t["name"] == "fiche-chiffres-fr"), None) or on.post("/api/transformations", {
    "name": "fiche-chiffres-fr", "title": "Fiche chiffres clés",
    "description": "Liste en français les chiffres clés d'un document, avec leur unité",
    "prompt": ("Réponds en français. À partir du document, dresse une liste à puces des chiffres clés "
               "(au plus 8), chacun avec son unité et ce qu'il mesure. N'invente aucun chiffre."),
    "apply_default": False})
rapport = on.get(f"/api/sources/{src['rapport-annuel-2025.pdf']}")["full_text"]
t0 = time.time()
r = on.post("/api/transformations/execute", {"transformation_id": perso["id"], "input_text": rapport})
res["perso_rapport"] = {"transformation": perso["id"], "duree_s": round(time.time() - t0, 1), "sortie": r.get("output")}
print("personnalisée :", res["perso_rapport"]["duree_s"], "s ->", (r.get("output") or "")[:400])

# 4. notes
n = on.post("/api/notes", {"title": "Points à vérifier", "content": "Comparer le délai contractuel Batterix (21 jours) "
                           "au délai constaté dans le classeur des stocks.", "note_type": "human", "notebook_id": nb["id"]})
res["note_manuelle"] = n
if ins:
    res["insight_vers_note"] = on.post(f"/api/insights/{ins[0]['id']}/save-as-note", {"notebook_id": nb["id"]})
res["notes_du_carnet"] = [{"title": x["title"], "note_type": x.get("note_type")} for x in on.get(f"/api/notes?notebook_id={nb['id']}")]
print("notes :", res["notes_du_carnet"])
sortie = RACINE / f"outils/resultats/open-notebook/transformations-{datetime.date.today()}.json"
sortie.write_text(json.dumps(res, ensure_ascii=False, indent=2))
print("->", sortie.relative_to(RACINE))
