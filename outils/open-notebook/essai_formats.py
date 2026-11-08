#!/usr/bin/env python3
"""Essai des formats : ce qu'Open Notebook a extrait de chaque document du corpus (carnet « Banc » ou autre).

Relève statut, caractères, passages (chunks), présence de valeurs témoins, et un extrait autour d'un tableau.
Sortie : outils/resultats/open-notebook/formats-<date>-<etiquette>.json
Usage : python3 outils/open-notebook/essai_formats.py [--carnet Banc] [--etiquette sans-docling]
"""
import argparse, datetime, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from client import RACINE, OpenNotebook

# valeurs témoins par document : présentes dans le texte extrait ?
TEMOINS = {
    "rapport-annuel-2025.pdf": ["48,6", "14,2", "15 400", "4 290", "97", "Motodrive", "Saint-Nazaire"],
    "contrat-batterix-scan.pdf": ["212", "21 jours", "40 000", "8 %"],
    "procedure-batteries.docx": ["Benali", "premier lundi", "classe D"],
    "strategie-2026.pptx": ["2 490", "25 000", "Utrecht"],
    "stocks-octobre-2025.xlsx": ["BAT-48V-14Ah", "1240", "1500", "Motodrive"],
    "faq-sav.html": ["7 ans", "02 40 00 12 34"],
    "cse-2025-10-14.md": ["1 150", "Le Gall"],
    "supplier-audit-batterix-en.pdf": ["87", "0.3", "Laura Fischer"],
    "message-vocal-production.mp3": ["Moreau", "ligne", "mars"],
}
EXTRAIT = {"rapport-annuel-2025.pdf": "T3 2025", "stocks-octobre-2025.xlsx": "BAT-48V", "procedure-batteries.docx": "Inspection",
           "strategie-2026.pptx": "Vilaine", "message-vocal-production.mp3": "ligne"}

p = argparse.ArgumentParser()
p.add_argument("--carnet", default="Banc")
p.add_argument("--etiquette", default="sans-docling")
a = p.parse_args()
on = OpenNotebook()
nb = next(n for n in on.get("/api/notebooks") if n["name"] == a.carnet)
res = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "carnet": a.carnet, "etiquette": a.etiquette, "documents": []}
for s in sorted(on.get(f"/api/sources?notebook_id={nb['id']}&limit=100"), key=lambda s: s["title"]):
    d = on.get(f"/api/sources/{s['id']}")
    st = on.get(f"/api/sources/{s['id']}/status")
    t = d.get("full_text") or ""
    tem = TEMOINS.get(d["title"], [])
    cle = EXTRAIT.get(d["title"])
    i = t.find(cle) if cle else -1
    ligne = {"document": d["title"], "statut": st["status"], "message": (st.get("processing_info") or {}).get("error"),
             "caracteres": len(t), "passages": d.get("embedded_chunks"),
             "temoins_trouves": [x for x in tem if x in t], "temoins_absents": [x for x in tem if x not in t],
             "extrait": t[max(0, i - 120): i + 280] if i >= 0 else t[:300]}
    res["documents"].append(ligne)
    print(f"{ligne['document']:34} {ligne['statut']:9} {ligne['caracteres']:6} car. {str(ligne['passages']):>3} passages  "
          f"absents : {ligne['temoins_absents']}")
sortie = RACINE / f"outils/resultats/open-notebook/formats-{datetime.date.today()}-{a.etiquette}.json"
sortie.write_text(json.dumps(res, ensure_ascii=False, indent=2))
print("->", sortie.relative_to(RACINE))
