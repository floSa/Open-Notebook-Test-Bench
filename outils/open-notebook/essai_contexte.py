#!/usr/bin/env python3
"""Essai de taille de contexte avec le service LLM central (chat : 16 384 jetons par requête, réflexion comprise).

Carnet « Essai contexte » : une source texte de taille croissante (texte du corpus répété, chaque copie numérotée),
en « full content », une question dont la réponse est dans la dernière copie. Relève le nombre de jetons annoncé par
Open Notebook (compteur « Context »), la durée, la réponse ou l'erreur. Le dépassement est provoqué exprès.
Sortie : outils/resultats/open-notebook/contexte-<date>.json ; le carnet est supprimé à la fin.
"""
import datetime, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from client import RACINE, OpenNotebook

TAILLES = [int(x) for x in (sys.argv[1:] or ["12000", "30000", "45000", "60000"])]
BASE = (RACINE / "corpus/documents/cse-2025-10-14.md").read_text() + "\n" + (RACINE / "corpus/documents/faq-sav.html").read_text()

on = OpenNotebook()
res = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "modele": "chat (service LLM central, 16 384 jetons)", "essais": []}
nb = on.post("/api/notebooks", {"name": "Essai contexte", "description": "essai de dépassement de contexte, supprimé à la fin"})
try:
    for taille in TAILLES:
        blocs, i = [], 1
        while sum(map(len, blocs)) < taille:
            blocs.append(f"\n\n### Copie {i}\n\n{BASE}"); i += 1
        code = f"VEL-{taille}-{i - 1}"
        texte = "".join(blocs) + f"\n\nCode de contrôle de la dernière copie : {code}.\n"
        src = on.post("/api/sources/json", {"type": "text", "content": texte, "notebooks": [nb["id"]], "title": f"texte-{taille}",
                                             "embed": False, "async_processing": False})
        ctx = on.post("/api/chat/context", {"notebook_id": nb["id"], "context_config": {"sources": {src["id"]: "full content"}}})
        s = on.post("/api/chat/sessions", {"notebook_id": nb["id"], "title": f"contexte {taille}"})
        t0 = time.time()
        try:
            r = on.post("/api/chat/execute", {"session_id": s["id"], "message": "Quel est le code de contrôle de la dernière copie ?",
                                              "context": ctx["context"]})
            rep = next((m["content"] for m in reversed(r["messages"]) if m["type"] == "ai"), "")
            err = None
        except Exception as e:
            rep, err = "", str(e)[:600]
        ligne = {"caracteres": len(texte), "jetons_annonces": ctx.get("token_count"), "duree_s": round(time.time() - t0, 1),
                 "code_attendu": code, "code_retrouve": code in rep, "reponse": rep[:400], "erreur": err}
        res["essais"].append(ligne)
        print(json.dumps(ligne, ensure_ascii=False)[:400], flush=True)
        on.delete(f"/api/sources/{src['id']}")
finally:
    on.delete(f"/api/notebooks/{nb['id']}?delete_exclusive_sources=true")
sortie = RACINE / f"outils/resultats/open-notebook/contexte-{datetime.date.today()}.json"
sortie.write_text(json.dumps(res, ensure_ascii=False, indent=2))
print("->", sortie.relative_to(RACINE))
