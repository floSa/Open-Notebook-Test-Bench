#!/usr/bin/env python3
"""Recherche plein texte contre recherche vectorielle (POST /api/search) sur le carnet « Banc ».

Pour chaque requête : document attendu, rang obtenu dans chaque mode, score, durée.
Sortie : outils/resultats/open-notebook/recherche-<date>.json
"""
import datetime, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from client import RACINE, OpenNotebook

REQUETES = [  # (requête, document attendu, nature)
    ("BAT-48V-14Ah", "stocks-octobre-2025.xlsx", "référence exacte"),
    ("Motodrive", "rapport-annuel-2025.pdf", "nom propre"),
    ("prime d'intéressement", "cse-2025-10-14.md", "mots exacts"),
    ("Combien de temps le cadre est-il couvert en cas de défaut ?", "faq-sav.html", "reformulation"),
    ("Où ranger les accumulateurs et à quelle température ?", "procedure-batteries.docx", "synonyme"),
    ("nouvelle usine près de l'estuaire de la Loire", "strategie-2026.pptx", "paraphrase"),
    ("battery supplier audit score", "supplier-audit-batterix-en.pdf", "anglais"),
    ("score de l'audit du fournisseur de batteries", "supplier-audit-batterix-en.pdf", "français vers anglais"),
    ("chiffre d'affaires par trimestre", "rapport-annuel-2025.pdf", "thème"),
    ("trottinette électrique", None, "absent du corpus"),
]

on = OpenNotebook()
nb = next(n for n in on.get("/api/notebooks") if n["name"] == "Banc")
res = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "carnet": nb["id"], "lignes": []}
for q, attendu, nature in REQUETES:
    ligne = {"requete": q, "attendu": attendu, "nature": nature}
    for mode in ("text", "vector"):
        t0 = time.time()
        r = on.post("/api/search", {"query": q, "type": mode, "limit": 10, "search_sources": True, "search_notes": False,
                                     "minimum_score": 0.2, "notebook_id": nb["id"]})
        duree = round(time.time() - t0, 2)
        titres = [x.get("title") for x in r["results"]]
        scores = [round(x.get("similarity") or x.get("relevance") or 0, 3) for x in r["results"]]
        rang = titres.index(attendu) + 1 if attendu in titres else None
        ligne[mode] = {"rang": rang, "resultats": len(titres), "premier": titres[0] if titres else None,
                       "scores": scores[:5], "titres": titres[:5], "duree_s": duree}
    res["lignes"].append(ligne)
    print(f"{nature:22} texte: rang {ligne['text']['rang']} ({ligne['text']['resultats']} rés.)  "
          f"vecteur: rang {ligne['vector']['rang']} ({ligne['vector']['resultats']} rés., {ligne['vector']['scores'][:3]})  {q}")
sortie = RACINE / f"outils/resultats/open-notebook/recherche-{datetime.date.today()}.json"
sortie.write_text(json.dumps(res, ensure_ascii=False, indent=2))
print("->", sortie.relative_to(RACINE))
