#!/usr/bin/env python3
"""Dernière version stable de chaque composant, relevée sur GitHub (API publique, sans compte).

Usage : versions.py <solution> <propriétaire/dépôt>[=version utilisée] ...
  ex. versions.py open-notebook lfnovo/open-notebook=v1.15.1 ollama/ollama=v0.40.15 surrealdb/surrealdb=v2.7.0
Sortie : outils/resultats/<solution>/versions-<date>.json ; code de sortie 1 si une version utilisée n'est pas
la dernière stable (préversions, rc, beta, alpha, nightly exclues). Une version plus ancienne imposée par
l'application (ex. SurrealDB 2 pour Open Notebook) se justifie dans le JSON par un argument « --raison dépôt=texte ».
"""
import datetime, json, re, sys, urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
INSTABLE = re.compile(r"(rc|beta|alpha|nightly|dev|preview|pre)", re.I)


def releases(depot):
    req = urllib.request.Request(f"https://api.github.com/repos/{depot}/releases?per_page=50",
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "rag-local-manuels"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def derniere_stable(depot):
    for r in releases(depot):
        if not r["draft"] and not r["prerelease"] and not INSTABLE.search(r["tag_name"]):
            return r["tag_name"], r["published_at"][:10]
    return None, None


def norm(v):
    return (v or "").lstrip("v")


if __name__ == "__main__":
    assert norm("v1.2") == "1.2" and INSTABLE.search("v0.9.0-rc.3") and not INSTABLE.search("v1.0.0")
    solution, args = sys.argv[1], sys.argv[2:]
    raisons = dict(a[len("--raison"):].strip(" =").split("=", 1) for a in args if a.startswith("--raison"))
    res, retard = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "composants": []}, False
    for a in (a for a in args if not a.startswith("--raison")):
        depot, _, utilisee = a.partition("=")
        tag, date = derniere_stable(depot)
        a_jour = not utilisee or norm(utilisee) == norm(tag)
        ligne = {"depot": depot, "derniere_stable": tag, "publiee_le": date, "utilisee": utilisee or None,
                 "a_jour": a_jour, "raison": raisons.get(depot)}
        res["composants"].append(ligne)
        retard |= not a_jour and not ligne["raison"]
        print(f"{depot:30s} stable {tag} ({date})  utilisée {utilisee or '-':12s} {'à jour' if a_jour else 'EN RETARD'}"
              + (f" — {ligne['raison']}" if ligne["raison"] else ""))
    out = RACINE / f"outils/resultats/{solution}/versions-{datetime.date.today()}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(1 if retard else 0)
