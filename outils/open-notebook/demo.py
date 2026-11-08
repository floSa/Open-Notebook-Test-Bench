#!/usr/bin/env python3
"""Jeu de démonstration et recettes de bout en bout : carnet « Démo Vélanor ».

Recette 1 : analyser le rapport annuel (questions sur les tableaux, fiche des chiffres clés enregistrée en note).
Recette 2 : confronter le contrat scanné, le classeur des stocks et l'audit (question multi-documents).
Recette 3 : préparer une synthèse pour la direction (question ouverte, note).
Les trois conversations sont conservées (sessions nommées) pour la démonstration. Idempotent : le carnet est recréé.
Sortie : outils/resultats/open-notebook/demo-<date>.json
"""
import datetime, json, re, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from client import RACINE, OpenNotebook

NOM = "Démo Vélanor"
CONVERSATIONS = [
    ("Recette 1 - rapport annuel", ["Quel est le chiffre d'affaires 2025 et quel trimestre a été le plus élevé ?",
                                     "Quel modèle est le plus vendu et quel est le plus cher ?"]),
    ("Recette 2 - contrat et audit", ["Le délai de livraison réellement constaté chez Batterix respecte-t-il le délai prévu par le contrat ?",
                                       "Quelles non-conformités l'audit de Batterix a-t-il relevées ?"]),
    ("Recette 3 - synthèse direction", ["Rédige en cinq puces les points d'attention pour la direction en 2026, avec les chiffres."]),
]

on = OpenNotebook()
res = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "carnet": NOM}
ancien = next((n for n in on.get("/api/notebooks") if n["name"] == NOM), None)
if ancien:
    on.delete(f"/api/notebooks/{ancien['id']}?delete_exclusive_sources=true")
nb = on.post("/api/notebooks", {"name": NOM, "description": "Corpus fictif Vélanor indexé, trois conversations exemples avec citations"})
res["sources"] = {}
t0 = time.time()
for f in sorted((RACINE / "corpus/documents").iterdir()):
    s = on.ajouter_fichier(f, nb["id"])
    res["sources"][f.name] = on.attendre_source(s["id"])
    print(f.name, res["sources"][f.name], flush=True)
res["indexation_s"] = round(time.time() - t0, 1)
srcs = on.get(f"/api/sources?notebook_id={nb['id']}&limit=100")
titres = {s["id"]: s["title"] for s in srcs}
ctx_cfg = {s["id"]: "full content" for s in srcs}
res["conversations"] = []
for titre, questions in CONVERSATIONS:
    sess = on.post("/api/chat/sessions", {"notebook_id": nb["id"], "title": titre})
    for q in questions:
        c = on.post("/api/chat/context", {"notebook_id": nb["id"], "context_config": {"sources": ctx_cfg}})
        t1 = time.time()
        r = on.post("/api/chat/execute", {"session_id": sess["id"], "message": q, "context": c["context"]})
        rep = [m for m in r["messages"] if m["type"] == "ai"][-1]["content"]
        cites = [titres.get(x, x) for x in dict.fromkeys(re.findall(r"source:[a-z0-9]+", rep))]
        res["conversations"].append({"session": titre, "question": q, "reponse": rep, "citations": cites,
                                     "duree_s": round(time.time() - t1, 1)})
        print(f"[{titre}] {q}\n  -> {rep[:300]}\n  citations : {cites}", flush=True)
# note issue de la transformation personnalisée (recette 1) et note manuelle (recette 3)
tr = next((t for t in on.get("/api/transformations") if t["name"] == "fiche-chiffres-fr"), None)
if tr:
    rapport = next(s for s in srcs if s["title"] == "rapport-annuel-2025.pdf")
    sortie = on.post("/api/transformations/execute", {"transformation_id": tr["id"],
                                                      "input_text": on.get(f"/api/sources/{rapport['id']}")["full_text"]})["output"]
    res["note_chiffres"] = on.post("/api/notes", {"title": "Chiffres clés 2025 (transformation)", "content": sortie,
                                                  "note_type": "ai", "notebook_id": nb["id"]})["id"]
syn = [c for c in res["conversations"] if c["session"].startswith("Recette 3")][-1]["reponse"]
res["note_synthese"] = on.post("/api/notes", {"title": "Points d'attention 2026", "content": syn, "note_type": "human",
                                              "notebook_id": nb["id"]})["id"]
s = RACINE / f"outils/resultats/open-notebook/demo-{datetime.date.today()}.json"
s.write_text(json.dumps(res, ensure_ascii=False, indent=2))
print("->", s.relative_to(RACINE))
