#!/usr/bin/env python3
"""Vérification fonctionnelle minimale après installation, avec mesure de la RAM de l'application.

1. mot de passe exigé (401 sans en-tête) ; 2. RAM au repos ; 3. carnet + import d'un document avec embedding,
RAM échantillonnée pendant l'indexation ; 4. une question, citation [source:…] attendue.
Sortie : outils/resultats/open-notebook/verif-minimale-<date>.json
"""
import datetime, json, sys, time, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "communs/banc"))
from client import RACINE, OpenNotebook
from commun import Echantillonneur

APP = ["rag-open-notebook", "rag-open-notebook-surrealdb"]
res = {"date": datetime.datetime.now().isoformat(timespec="seconds")}
try:
    urllib.request.urlopen("http://127.0.0.1:5055/api/notebooks", timeout=10)
    res["sans_mot_de_passe"] = "200 (accès ouvert !)"
except urllib.error.HTTPError as e:
    res["sans_mot_de_passe"] = f"{e.code} {e.read().decode()[:80]}"
print("sans mot de passe :", res["sans_mot_de_passe"])

repos = Echantillonneur(APP + ["rag-socle-ollama"], pas=2); repos.start(); time.sleep(6); repos.stop.set(); repos.join()
res["ram_repos_mo"] = repos.pics
print("RAM au repos :", repos.pics)

on = OpenNotebook()
nb = on.post("/api/notebooks", {"name": "Essai installation", "description": "vérification minimale"})
doc = RACINE / "corpus/documents/faq-sav.html"
ech = Echantillonneur(APP + ["rag-socle-ollama"], pas=2); ech.start()
t0 = time.time()
src = on.ajouter_fichier(doc, nb["id"])
etat = on.attendre_source(src["id"])
res["indexation"] = {**etat, "duree_s": round(time.time() - t0, 1)}
ech.stop.set(); ech.join()
res["ram_pic_indexation_mo"] = ech.pics
print("indexation :", res["indexation"], "pic RAM :", ech.pics)

t0 = time.time()
q = "Quelle est la durée de garantie du cadre ?"
rep, sid, jetons = on.demander(nb["id"], q, {src["id"]: "full content"}, titre="vérification")
res["question"] = {"question": q, "reponse": rep, "duree_s": round(time.time() - t0, 1), "jetons_contexte": jetons,
                   "citation_presente": src["id"] in rep, "source_id": src["id"]}
print("réponse :", rep[:300], "\ncitation présente :", src["id"] in rep, f"({res['question']['duree_s']} s)")
res["carnet"] = nb["id"]
s = RACINE / f"outils/resultats/open-notebook/verif-minimale-{datetime.date.today()}.json"
s.write_text(json.dumps(res, ensure_ascii=False, indent=2))
print("->", s.relative_to(RACINE))
