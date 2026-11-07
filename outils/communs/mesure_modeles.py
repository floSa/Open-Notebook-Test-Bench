#!/usr/bin/env python3
"""Mesures du socle Ollama (CPU) : débit, premier jeton, RAM, contexte, dépassement.

Écrit outils/resultats/socle/mesures-<date>.json. Bibliothèque standard seulement.
Usage : python3 outils/communs/mesure_modeles.py [--rapide]
"""
import concurrent.futures as cf, datetime, json, subprocess, sys, time, urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
URL = "http://127.0.0.1:11434"
CONTENEUR = "rag-socle-ollama"
CHATS = ["qwen3:4b-instruct", "ministral-3:3b"]
EMBED = "bge-m3"
CONTEXTES = [4096, 8192, 16384, 32768]
PHRASE = "La société Vélanor fabrique des vélos électriques à Nantes et publie chaque année un rapport détaillé. "


def post(chemin, corps, timeout=900):
    req = urllib.request.Request(URL + chemin, json.dumps(corps).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def ram_conteneur():
    out = subprocess.run(["docker", "stats", "--no-stream", "--format", "{{.MemUsage}}", CONTENEUR],
                         capture_output=True, text=True).stdout.split("/")[0].strip()
    val = float(out[:-3]); unite = out[-3:]
    return round(val * {"GiB": 1024, "MiB": 1, "KiB": 1 / 1024}[unite])


def decharger():
    for m in CHATS + [EMBED]:
        try: post("/api/generate", {"model": m, "keep_alive": 0}) if m != EMBED else post("/api/embed", {"model": m, "input": "x", "keep_alive": 0})
        except Exception: pass
    time.sleep(2)


def generer(modele, ctx, prompt, n=128):
    t0 = time.time()
    r = post("/api/generate", {"model": modele, "prompt": prompt, "stream": False,
                               "options": {"num_ctx": ctx, "num_predict": n, "temperature": 0}})
    return {
        "duree_s": round(time.time() - t0, 2),
        "jetons_prompt": r.get("prompt_eval_count"),
        "jetons_generes": r.get("eval_count"),
        "debit_generation_jetons_s": round(r["eval_count"] / (r["eval_duration"] / 1e9), 2),
        "debit_prompt_jetons_s": round(r["prompt_eval_count"] / (r["prompt_eval_duration"] / 1e9), 1) if r.get("prompt_eval_duration") else None,
        "premier_jeton_s": round((r.get("load_duration", 0) + r.get("prompt_eval_duration", 0)) / 1e9, 2),
        "debut_reponse": r["response"][:80],
    }


def main():
    rapide = "--rapide" in sys.argv
    res = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "serveur": "ollama 0.30.7 (CPU)",
           "version": json.loads(urllib.request.urlopen(URL + "/api/version").read()), "mesures": []}
    court = "Explique en trois phrases ce qu'est la recherche augmentée par récupération (RAG)."
    decharger(); ram_vide = ram_conteneur(); res["ram_conteneur_vide_mo"] = ram_vide
    for modele in CHATS:
        for ctx in (CONTEXTES[:2] if rapide else CONTEXTES):
            decharger()
            froid = generer(modele, ctx, court, 64)  # inclut le chargement
            chaud = generer(modele, ctx, court, 128)
            # prompt long : remplit environ la moitié du contexte
            long_ = (PHRASE * (ctx // 2 // 22)) + "\nRésume ce texte en une phrase."
            plein = generer(modele, ctx, long_, 64)
            # deux requêtes simultanées
            t0 = time.time()
            with cf.ThreadPoolExecutor(2) as ex:
                deux = list(ex.map(lambda _: generer(modele, ctx, court, 96), range(2)))
            ram = ram_conteneur()
            ps = post("/api/ps", {}) if False else json.loads(urllib.request.urlopen(URL + "/api/ps").read())
            taille = next((m["size"] for m in ps["models"] if m["name"] == modele), None)
            ligne = {"modele": modele, "num_ctx": ctx, "froid": froid, "chaud": chaud, "prompt_demi_contexte": plein,
                     "deux_simultanees": deux, "deux_simultanees_duree_s": round(time.time() - t0, 2),
                     "ram_conteneur_mo": ram, "taille_modele_charge_mo": taille // 10**6 if taille else None}
            res["mesures"].append(ligne)
            print(f"{modele:20} ctx={ctx:6} chaud={chaud['debit_generation_jetons_s']} j/s "
                  f"prompt={plein['debit_prompt_jetons_s']} j/s 1er jeton (demi-ctx)={plein['premier_jeton_s']} s "
                  f"RAM={ram} Mo charge={ligne['taille_modele_charge_mo']} Mo", flush=True)
    # embedding
    decharger()
    textes = [PHRASE * 20] * 16
    t0 = time.time(); e = post("/api/embed", {"model": EMBED, "input": textes}); d = time.time() - t0
    res["embedding"] = {"modele": EMBED, "dimension": len(e["embeddings"][0]), "lot": 16,
                        "jetons_par_texte_approx": 20 * 22, "duree_lot_s": round(d, 2), "ram_conteneur_mo": ram_conteneur()}
    print("embedding", res["embedding"], flush=True)
    # dépassement volontaire : prompt plus long que num_ctx
    decharger()
    trop = (PHRASE * 400) + "\nQuelle ville est citée ?"
    t0 = time.time()
    r = post("/api/generate", {"model": CHATS[0], "prompt": trop, "stream": False,
                               "options": {"num_ctx": 2048, "num_predict": 32, "temperature": 0}})
    res["depassement"] = {"num_ctx": 2048, "jetons_envoyes_approx": 400 * 22, "prompt_eval_count": r.get("prompt_eval_count"),
                          "reponse": r["response"][:200], "duree_s": round(time.time() - t0, 2),
                          "logs": subprocess.run(["docker", "logs", "--since", "2m", CONTENEUR], capture_output=True, text=True).stderr[-3000:]}
    print("dépassement", {k: v for k, v in res["depassement"].items() if k != "logs"}, flush=True)
    sortie = RACINE / f"outils/resultats/socle/mesures-{datetime.date.today()}.json"
    sortie.write_text(json.dumps(res, ensure_ascii=False, indent=2))
    print("->", sortie.relative_to(RACINE))


if __name__ == "__main__":
    main()
