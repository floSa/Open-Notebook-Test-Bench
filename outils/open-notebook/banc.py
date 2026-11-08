#!/usr/bin/env python3
"""Adaptateur du banc pour Open Notebook (API REST) et lancement.

Modes :
  chat : une session de chat par question dans le carnet « Banc », contexte = toutes les sources en MODE_CONTEXTE
         (« full content » par défaut) ; citations lues dans le texte ([source:id]).
  ask  : POST /api/search/ask/simple (recherche vectorielle, jusqu'à 5 recherches de 10 résultats).
Usage :
  python3 outils/open-notebook/banc.py --etiquette defaut-qwen [--mode chat|ask] [--modele qwen3:4b-instruct]
         [--contexte "full content"|insights] [--reindexer] [--limite N] [--sans-juge]
"""
import argparse, re, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "communs/banc"))
from client import RACINE, OpenNotebook
import commun

CARNET = "Banc"


class Adaptateur:
    nom = "open-notebook"

    def __init__(self, mode, modele, contexte):
        self.on, self.mode, self.contexte = OpenNotebook(), mode, contexte
        self.modeles = {m["name"]: m["id"] for m in self.on.get("/api/models") if m["type"] == "language"}
        self.modele_id = self.modeles[modele]
        self.modele = modele
        self.nb = next((n for n in self.on.get("/api/notebooks") if n["name"] == CARNET), None)
        self.titres = {}
        if self.nb:
            self._charger_sources()

    def _charger_sources(self):
        self.sources = self.on.get(f"/api/sources?notebook_id={self.nb['id']}&limit=100")
        self.titres = {s["id"]: s["title"] for s in self.sources}

    def config(self):
        env = dict(l.split("=", 1) for l in (RACINE / "donnees/open-notebook/.env").read_text().splitlines() if "=" in l)
        cred = next(c for c in self.on.get("/api/credentials") if c["name"] == "llm-service")
        return {"mode": self.mode, "modele": self.modele, "contexte_sources": self.contexte if self.mode == "chat" else None,
                "num_ctx": cred.get("num_ctx"), "chunk_size": env.get("OPEN_NOTEBOOK_CHUNK_SIZE", "400 (défaut)"),
                "docling": env.get("OPEN_NOTEBOOK_ENABLE_DOCLING", "false"), "version": "1.15.1"}

    def indexer(self, fichiers):
        if self.nb:  # carnet recréé pour une indexation propre
            self.on.delete(f"/api/notebooks/{self.nb['id']}?delete_exclusive_sources=true")
        self.nb = self.on.post("/api/notebooks", {"name": CARNET, "description": "Corpus Vélanor, banc automatique"})
        etats = {}
        for f in fichiers:
            t0 = time.time()
            s = self.on.ajouter_fichier(f, self.nb["id"])
            e = self.on.attendre_source(s["id"])
            e["duree_s"] = round(time.time() - t0, 1)
            etats[f.name] = e
            print(f"  {f.name:34} {e}", flush=True)
        self._charger_sources()
        return {"sources": etats}

    def _citations(self, texte):
        cits = []
        for sid in dict.fromkeys(re.findall(r"source:[a-z0-9]+", texte)):
            cits.append({"document": self.titres.get(sid, sid), "page": None, "extrait": sid})
        return cits

    def demander(self, question):
        if self.mode == "ask":
            m = self.modele_id
            r = self.on.post("/api/search/ask/simple", {"question": question, "strategy_model": m, "answer_model": m,
                                                        "final_answer_model": m, "notebook_id": self.nb["id"]})
            texte = r["answer"]
        else:
            ctx = {sid: self.contexte for sid in self.titres}
            texte, sid, jetons = self.on.demander(self.nb["id"], question, ctx)
            self.on.delete(f"/api/chat/sessions/{sid}")
        return {"reponse": texte, "citations": self._citations(texte)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--etiquette", required=True)
    p.add_argument("--mode", default="chat", choices=["chat", "ask"])
    p.add_argument("--modele", default="qwen3:4b-instruct")
    p.add_argument("--contexte", default="full content")
    p.add_argument("--reindexer", action="store_true")
    p.add_argument("--limite", type=int)
    p.add_argument("--sans-juge", action="store_true")
    p.add_argument("--ids", help="sous-ensemble de questions, ex. Q01,Q15,Q21")
    a = p.parse_args()
    ad = Adaptateur(a.mode, a.modele, a.contexte)
    res = commun.lancer(ad, a.etiquette, ["rag-open-notebook", "rag-open-notebook-surrealdb"], ["ollama-central"],
                        indexer=a.reindexer or not ad.nb, juge=not a.sans_juge, limite=a.limite,
                        ids=a.ids.split(",") if a.ids else None)
    commun.ecrire(res, RACINE / "outils/resultats/open-notebook")
    s = res["synthese"]
    print(f"exactes {s['exactes']}/{s['sur']}, refus {s['refus_corrects']}/{s['pieges']}, bon document cité "
          f"{s['citation_bon_document']}, p50 {s['latence_p50_s']} s, p95 {s['latence_p95_s']} s")


if __name__ == "__main__":
    main()
