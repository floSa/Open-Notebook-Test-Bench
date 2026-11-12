"""Banc commun : interface d'adaptateur, notation, mesures, sorties JSON et Markdown.

Un adaptateur expose :
    nom : str
    indexer(fichiers: list[Path]) -> dict        # infos libres (durée mesurée ici)
    demander(question: str) -> {"reponse": str, "citations": [{"document": str, "page": int|None, "extrait": str}]}
    config() -> dict                              # réglages en vigueur, pour le rapport
Bibliothèque standard seulement.
"""
import datetime, json, re, statistics, subprocess, threading, time, unicodedata, urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parents[3]
QUESTIONS = RACINE / "corpus/questions.json"
DOCUMENTS = RACINE / "corpus/documents"

REFUS = re.compile(r"(ne (contien|mentionn|précis|fourni|donn|perm|figur|trouv)|n'(est|apparaît|indique|y a)|aucune? (information|mention|donnée)|"
                   r"pas (d'information|mentionn|précis|indiqu|disponible|trouv|dans)|introuvable|impossible de (répondre|trouver|déterminer)|"
                   r"not (mention|contain|provide|found|available)|no information|je ne (sais|dispose|trouve))", re.I)


def normaliser(t):
    t = unicodedata.normalize("NFKC", t or "").lower()
    t = re.sub(r"(?<=\d)[\s  .](?=\d{3}\b)", "", t)  # 40 000 / 40.000 -> 40000
    t = re.sub(r"(?<=\d)[.,](?=\d)", ",", t)                   # 0.3 -> 0,3
    return re.sub(r"\s+", " ", t)


def present(alt, r):
    """alt présent dans r, sans être collé à un chiffre ou une lettre (« 8 » ne doit pas valider « 87 »)."""
    return re.search(r"(?<![0-9a-z])" + re.escape(normaliser(alt)) + r"(?![0-9])", r) is not None


def exacte(reponse, attendu):
    r = normaliser(reponse)
    return all(any(present(alt, r) for alt in el.split("|")) for el in attendu)


def citation_correcte(citations, sources):
    if not sources:
        return None
    docs = {s["document"] for s in sources}
    pages = {(s["document"], s["page"]) for s in sources}
    bon_doc = any(any(d in (c.get("document") or "") for d in docs) for c in citations)
    pages_c = [(d, c.get("page")) for c in citations for d in docs if d in (c.get("document") or "") and c.get("page")]
    bonne_page = (any(p in pages for p in pages_c)) if pages_c else None
    return {"document": bon_doc, "page": bonne_page}


def _central():
    """Adresse et clé du service LLM central (.env du dépôt ; la clé n'est jamais affichée)."""
    env = dict(l.split("=", 1) for l in (RACINE / ".env").read_text().splitlines() if "=" in l and not l.lstrip().startswith("#"))
    return env.get("LLM_CENTRAL_URL_HOTE", "http://127.0.0.1:8080/v1").strip(), env["LLM_CENTRAL_KEY"].strip()


def juge_llm(question, attendu, reponse, modele="chat"):
    """Jugement complémentaire par LLM local (signalé comme tel dans les résultats) : modèle `chat` du service
    central, réflexion coupée, température 0."""
    consigne = (f"Question : {question}\nÉléments attendus : {', '.join(attendu) or 'aucune réponse dans les documents'}\n"
                f"Réponse à juger : {reponse}\n\nLa réponse est-elle correcte (contient les éléments attendus, ou signale "
                f"l'absence d'information si aucun élément n'est attendu) ? Réponds par un seul mot : OUI ou NON.")
    url, cle = _central()
    req = urllib.request.Request(url + "/chat/completions", json.dumps({
        "model": modele, "messages": [{"role": "user", "content": consigne}], "temperature": 0, "max_tokens": 5,
        "chat_template_kwargs": {"enable_thinking": False}}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {cle}"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"].strip().upper().startswith("OUI")
    except Exception as e:
        return f"erreur : {type(e).__name__}"


class Echantillonneur(threading.Thread):
    """Relève la mémoire des conteneurs (docker stats) pendant le banc."""

    def __init__(self, conteneurs, pas=5):
        super().__init__(daemon=True)
        self.conteneurs, self.pas, self.stop, self.pics = conteneurs, pas, threading.Event(), {}

    def run(self):
        while not self.stop.is_set():
            out = subprocess.run(["docker", "stats", "--no-stream", "--format", "{{.Name}};{{.MemUsage}}", *self.conteneurs],
                                 capture_output=True, text=True).stdout
            for l in out.strip().splitlines():
                nom, mem = l.split(";"); v = mem.split("/")[0].strip()
                mo = float(re.sub(r"[A-Za-z]+", "", v)) * {"GiB": 1024, "MiB": 1, "KiB": 1 / 1024, "B": 1 / 2**20}[re.sub(r"[\d.]+", "", v)]
                self.pics[nom] = max(self.pics.get(nom, 0), round(mo))
            self.stop.wait(self.pas)


def vram_nvidia():
    """VRAM GPU utilisée (nvidia-smi) : pertinent pour un socle vLLM, qui réserve sa VRAM au démarrage et la garde
    (une mesure en fin de banc suffit, contrairement à la RAM applicative qui varie)."""
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=5).stdout.strip().splitlines()[0]
        used, total = (int(x) for x in out.split(","))
        return f"{used} Mo / {total} Mo (nvidia-smi, mesuré en fin de banc)"
    except Exception:
        return "sans objet (aucun GPU NVIDIA, socle CPU)"


def pct(vals, q):
    vals = sorted(vals)
    return round(vals[min(len(vals) - 1, int(round(q / 100 * (len(vals) - 1))))], 2) if vals else None


def lancer(adaptateur, etiquette, conteneurs_app, conteneurs_modeles, indexer=True, juge=True, limite=None, ids=None):
    qs = json.loads(QUESTIONS.read_text())["questions"][:limite]
    if ids:
        qs = [q for q in qs if q["id"] in ids]
    ech = Echantillonneur(conteneurs_app + conteneurs_modeles); ech.start()
    res = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "solution": adaptateur.nom, "etiquette": etiquette,
           "config": adaptateur.config(), "questions": []}
    if indexer:
        t0 = time.time()
        res["indexation"] = adaptateur.indexer(sorted(f for f in DOCUMENTS.iterdir() if f.is_file()))
        res["indexation"]["duree_s"] = round(time.time() - t0, 1)
        print(f"indexation : {res['indexation']['duree_s']} s", flush=True)
    for q in qs:
        t0 = time.time()
        try:
            r = adaptateur.demander(q["question"]); err = None
        except Exception as e:
            r, err = {"reponse": "", "citations": []}, repr(e)[:500]
        lat = round(time.time() - t0, 2)
        piege = q["type"] == "piège"
        ligne = {**{k: q[k] for k in ("id", "type", "question", "attendu")}, "latence_s": lat, "erreur": err,
                 "reponse": r["reponse"], "citations": r["citations"],
                 "exacte": bool(REFUS.search(r["reponse"])) if piege else exacte(r["reponse"], q["attendu"]),
                 "citation": citation_correcte(r["citations"], q["sources"])}
        if juge:
            ligne["juge_llm"] = juge_llm(q["question"], q["attendu"], r["reponse"])
        res["questions"].append(ligne)
        print(f"{q['id']} {q['type']:15} {'OK ' if ligne['exacte'] else 'NON'} {lat:6.1f}s  {r['reponse'][:90]!r}", flush=True)
    ech.stop.set(); ech.join(timeout=30)
    res["synthese"] = synthese(res["questions"], ech.pics, conteneurs_app)
    res["synthese"]["indexation_s"] = res.get("indexation", {}).get("duree_s")
    return res


def renoter(res):
    """Recalcule exactitude et synthèse à partir des réponses enregistrées (pics de RAM conservés)."""
    pics = res["synthese"]["pic_ram_mo"]; idx = res["synthese"].get("indexation_s")
    qs = {q["id"]: q for q in json.loads(QUESTIONS.read_text())["questions"]}
    for l in res["questions"]:
        l["exacte"] = bool(REFUS.search(l["reponse"])) if l["type"] == "piège" else exacte(l["reponse"], qs[l["id"]]["attendu"])
    app = [k for k in pics if k.startswith("rag-open-notebook")]
    res["synthese"] = synthese(res["questions"], pics, app); res["synthese"]["indexation_s"] = idx
    return res


def synthese(lignes, pics, conteneurs_app):
    normales = [l for l in lignes if l["type"] != "piège"]
    pieges = [l for l in lignes if l["type"] == "piège"]
    cit = [l["citation"] for l in normales if l["citation"]]
    lat = [l["latence_s"] for l in lignes if not l["erreur"]]
    jug = [l.get("juge_llm") for l in lignes if isinstance(l.get("juge_llm"), bool)]
    par_type = {}
    for l in lignes:
        t = par_type.setdefault(l["type"], [0, 0]); t[0] += bool(l["exacte"]); t[1] += 1
    return {
        "questions": len(lignes), "exactes": sum(bool(l["exacte"]) for l in normales), "sur": len(normales),
        "refus_corrects": sum(bool(l["exacte"]) for l in pieges), "pieges": len(pieges),
        "citation_bon_document": sum(c["document"] for c in cit), "citation_bonne_page": sum(bool(c["page"]) for c in cit),
        "citations_avec_page": sum(c["page"] is not None for c in cit),
        "juge_llm_oui": sum(jug), "juge_llm_sur": len(jug),
        "erreurs": sum(bool(l["erreur"]) for l in lignes),
        "latence_p50_s": pct(lat, 50), "latence_p95_s": pct(lat, 95),
        "par_type": {k: f"{a}/{b}" for k, (a, b) in par_type.items()},
        "pic_ram_mo": pics, "pic_ram_application_mo": sum(v for k, v in pics.items() if k in conteneurs_app),
        "vram": vram_nvidia(),
    }


def ecrire(res, dossier):
    dossier = Path(dossier); dossier.mkdir(parents=True, exist_ok=True)
    base = dossier / f"banc-{res['date'][:10]}-{res['etiquette']}"
    base.with_suffix(".json").write_text(json.dumps(res, ensure_ascii=False, indent=2))
    s = res["synthese"]
    md = [f"# Banc {res['solution']} — {res['etiquette']} — {res['date']}", "",
          "| Mesure | Valeur |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in s.items()]
    md += ["", "| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |", "|---|---|---|---|---|---|---|"]
    for l in res["questions"]:
        c = l["citation"]["document"] if l["citation"] else "-"
        rep = l["reponse"][:80].replace("|", "/").replace("\n", " ")
        md.append(f"| {l['id']} | {l['type']} | {'oui' if l['exacte'] else 'non'} | {l.get('juge_llm', '-')} | {c} | {l['latence_s']} | {rep} |")
    base.with_suffix(".md").write_text("\n".join(md) + "\n")
    print("->", base.with_suffix(".json").relative_to(RACINE))
    return base
