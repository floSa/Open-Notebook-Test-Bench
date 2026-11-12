#!/usr/bin/env python3
"""Tableau Markdown des bancs d'une ou plusieurs solutions.

Usage : python3 outils/communs/banc/tableau.py <dossier de résultats ou fichier banc-*.json> [...] [--relatif-a <dossier>]
Les liens pointent vers chaque fichier JSON, relativement au dossier donné par --relatif-a (par défaut : le dossier
de chaque fichier). La colonne « Réglages » résume les clés de configuration connues présentes dans le JSON
(Open Notebook : mode, contexte des sources, num_ctx, Docling ; RAGFlow : gabarit, top_n, poids des vecteurs,
contexte déclaré, mode agentique).
"""
import json, os, sys
from pathlib import Path

CLES = [("mode", "mode"), ("contexte_sources", "sources"), ("num_ctx", "num_ctx"), ("docling", "Docling"),
        ("gabarit", "gabarit"), ("top_n", "top_n"), ("vector_similarity_weight", "poids vecteurs"),
        ("contexte_declare", "contexte"), ("extra_question", "options")]


def reglages(c):
    morceaux = []
    for cle, nom in CLES:
        v = c.get(cle)
        if v not in (None, "", {}, []):
            morceaux.append(f"{nom} {json.dumps(v, ensure_ascii=False) if isinstance(v, dict) else v}")
    return ", ".join(morceaux) or "-"


def fichiers(args):
    for a in args:
        p = Path(a)
        yield from (sorted(p.glob("banc-*.json")) if p.is_dir() else [p])


def main(argv):
    rel = None
    if "--relatif-a" in argv:
        i = argv.index("--relatif-a"); rel = Path(argv[i + 1]); argv = argv[:i] + argv[i + 2:]
    lignes = ["| Solution | Banc | Modèle | Réglages | Exactes | Refus pièges | Bon document cité | Bonne page | p50 (s) | p95 (s) | Indexation (s) | Pic RAM application (Mo) |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for f in fichiers(argv):
        d = json.loads(f.read_text()); s = d["synthese"]; c = d.get("config", {})
        lien = os.path.relpath(f, rel) if rel else f.name
        page = f"{s.get('citation_bonne_page', 0)}/{s['citations_avec_page']}" if s.get("citations_avec_page") else "non exposée"
        lignes.append(f"| {d['solution']} | [{d['etiquette']}]({lien}) | {c.get('modele', '-')} | {reglages(c)} | "
                      f"{s['exactes']}/{s['sur']} | {s['refus_corrects']}/{s['pieges']} | {s['citation_bon_document']} | {page} | "
                      f"{s['latence_p50_s']} | {s['latence_p95_s']} | {s.get('indexation_s') or '-'} | {s['pic_ram_application_mo']} |")
    print("\n".join(lignes))


if __name__ == "__main__":
    main(sys.argv[1:])
