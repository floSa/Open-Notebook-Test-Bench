#!/usr/bin/env python3
"""Tableau Markdown comparant les bancs d'une solution : python3 outils/communs/banc/tableau.py <dossier de résultats>"""
import json, sys
from pathlib import Path

lignes = ["| Banc | Mode | Modèle | Contexte | `num_ctx` | Docling | Exactes | Refus pièges | Bon document cité | p50 (s) | p95 (s) | Indexation (s) | Pic RAM application (Mo) |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for f in sorted(Path(sys.argv[1]).glob("banc-*.json")):
    d = json.loads(f.read_text()); s = d["synthese"]; c = d["config"]
    lignes.append(f"| [{d['etiquette']}]({f.name}) | {c['mode']} | {c['modele']} | {c.get('contexte_sources') or '-'} | {c['num_ctx']} | "
                  f"{c['docling']} | {s['exactes']}/{s['sur']} | {s['refus_corrects']}/{s['pieges']} | {s['citation_bon_document']} | "
                  f"{s['latence_p50_s']} | {s['latence_p95_s']} | {s.get('indexation_s') or '-'} | {s['pic_ram_application_mo']} |")
print("\n".join(lignes))
