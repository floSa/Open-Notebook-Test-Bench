#!/usr/bin/env python3
"""Chat et citations : coût des modes de contexte, effet sur une question, modèle de raisonnement.

1. jetons envoyés selon le mode des sources du carnet « Banc » : not in / insights / full content ;
2. une même question posée avec « insights » puis « full content » ;
3. la même question avec un modèle de raisonnement (qwen3:4b, mode « thinking ») passé en model_override.
Sortie : outils/resultats/open-notebook/chat-<date>.json
"""
import datetime, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from client import RACINE, OpenNotebook

on = OpenNotebook()
nb = next(n for n in on.get("/api/notebooks") if n["name"] == "Banc")
srcs = on.get(f"/api/sources?notebook_id={nb['id']}&limit=100")
res = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "modes": {}}
for mode in ("not in", "insights", "full content"):
    c = on.post("/api/chat/context", {"notebook_id": nb["id"], "context_config": {"sources": {s["id"]: mode for s in srcs}}})
    res["modes"][mode] = {"jetons": c.get("token_count"), "caracteres": c.get("char_count")}
print("modes :", res["modes"])

Q = "Quel est le délai de livraison prévu par le contrat avec Batterix, et quel délai moyen est réellement constaté ?"


def poser(ctx_mode, modele=None):
    s = on.post("/api/chat/sessions", {"notebook_id": nb["id"], "title": f"essai {ctx_mode} {modele}", "model_override": modele})
    c = on.post("/api/chat/context", {"notebook_id": nb["id"], "context_config": {"sources": {x["id"]: ctx_mode for x in srcs}}})
    t0 = time.time()
    r = on.post("/api/chat/execute", {"session_id": s["id"], "message": Q, "context": c["context"], "model_override": modele})
    rep = [m for m in r["messages"] if m["type"] == "ai"][-1]["content"]
    on.delete(f"/api/chat/sessions/{s['id']}")
    return {"mode": ctx_mode, "modele": modele, "duree_s": round(time.time() - t0, 1), "jetons_contexte": c.get("token_count"), "reponse": rep}


res["question"] = Q
res["essais"] = [poser("insights"), poser("full content")]
mods = {m["name"]: m["id"] for m in on.get("/api/models")}
if "qwen3:4b" not in mods:  # modèle de raisonnement déjà présent dans ~/.ollama, copié dans le socle
    cred = next(c for c in on.get("/api/credentials") if c["name"] == "llm-service")
    mods["qwen3:4b"] = on.post("/api/models", {"name": "qwen3:4b", "provider": "ollama", "type": "language", "credential": cred["id"]})["id"]
try:
    res["essais"].append(poser("full content", mods["qwen3:4b"]))
except Exception as e:
    res["essais"].append({"modele": "qwen3:4b", "erreur": repr(e)[:500]})
for e in res["essais"]:
    print(json.dumps(e, ensure_ascii=False)[:700])
sortie = RACINE / f"outils/resultats/open-notebook/chat-{datetime.date.today()}.json"
sortie.write_text(json.dumps(res, ensure_ascii=False, indent=2))
print("->", sortie.relative_to(RACINE))
