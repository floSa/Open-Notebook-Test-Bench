#!/usr/bin/env python3
"""Pose une question dans un carnet (session de chat, contexte « full content ») et affiche réponse et citations.
Usage : python3 03_poser_question.py "Exemple API" "Quel est le montant de la prime d'intéressement ?"
Mot de passe : variable ON_MDP, sinon donnees/open-notebook/.env. Bibliothèque standard seulement."""
import json, os, re, sys, urllib.request
from pathlib import Path

API = "http://127.0.0.1:5055/api"
env = Path(__file__).resolve().parents[2] / "donnees/open-notebook/.env"
MDP = os.environ.get("ON_MDP") or next(l.split("=", 1)[1] for l in env.read_text().splitlines() if l.startswith("OPEN_NOTEBOOK_PASSWORD="))


def appel(methode, chemin, corps=None):
    req = urllib.request.Request(API + chemin, json.dumps(corps).encode() if corps is not None else None,
                                 {"Authorization": f"Bearer {MDP}", "Content-Type": "application/json"}, method=methode)
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read() or b"null")


nom, question = (sys.argv[1:3] + ["Exemple API", "Quel est le montant de la prime d'intéressement ?"][len(sys.argv[1:3]):])
nb = next(n for n in appel("GET", "/notebooks") if n["name"] == nom)
sources = appel("GET", f"/sources?notebook_id={nb['id']}")
session = appel("POST", "/chat/sessions", {"notebook_id": nb["id"], "title": "exemple 03"})
ctx = appel("POST", "/chat/context", {"notebook_id": nb["id"],
                                      "context_config": {"sources": {s["id"]: "full content" for s in sources}}})
rep = appel("POST", "/chat/execute", {"session_id": session["id"], "message": question, "context": ctx["context"]})
texte = [m for m in rep["messages"] if m["type"] == "ai"][-1]["content"]
titres = {s["id"]: s["title"] for s in sources}
print("contexte :", ctx["token_count"], "jetons")
print("réponse :", texte)
for sid in dict.fromkeys(re.findall(r"source:[a-z0-9]+", texte)):
    print("citation :", sid, "->", titres.get(sid))
