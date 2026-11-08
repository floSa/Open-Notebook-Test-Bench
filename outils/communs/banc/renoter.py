#!/usr/bin/env python3
"""Renote un ou plusieurs résultats de banc (après correction de la notation), sans relancer les questions.
Usage : python3 outils/communs/banc/renoter.py outils/resultats/<solution>/banc-*.json"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import commun

for f in sys.argv[1:]:
    res = commun.renoter(json.loads(Path(f).read_text()))
    res["renote"] = "notation corrigée (bornes des nombres) après coup ; réponses inchangées"
    commun.ecrire(res, Path(f).resolve().parent)
    s = res["synthese"]; print(f, f"exactes {s['exactes']}/{s['sur']}", s["par_type"])
