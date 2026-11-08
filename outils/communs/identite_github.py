#!/usr/bin/env python3
"""Identité d'un dépôt GitHub (étoiles, forks, licence, activité, versions) par l'API publique, sans compte.

Usage : identite_github.py <propriétaire/dépôt> <solution>
Sortie : outils/resultats/<solution>/identite-github-<date>.json
"""
import datetime, json, re, sys, urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
depot, solution = sys.argv[1], sys.argv[2]


def api(chemin, entetes=False):
    req = urllib.request.Request(f"https://api.github.com/repos/{depot}{chemin}",
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "rag-local-manuels"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return (json.load(r), dict(r.headers)) if entetes else json.load(r)


def total(chemin):
    """Nombre total d'éléments d'une liste paginée (lu dans l'en-tête Link avec per_page=1)."""
    corps, h = api(chemin + ("&" if "?" in chemin else "?") + "per_page=1", entetes=True)
    m = re.search(r'[?&]page=(\d+)>; rel="last"', h.get("Link", ""))
    return int(m.group(1)) if m else len(corps)


d = api("")
aujourdhui = datetime.date.today()
il_y_a_90j = (aujourdhui - datetime.timedelta(days=90)).isoformat()
versions = api("/releases?per_page=10")
res = {
    "date": datetime.datetime.now().isoformat(timespec="seconds"),
    "depot": f"https://github.com/{depot}",
    "description": d["description"], "site": d["homepage"],
    "etoiles": d["stargazers_count"], "forks": d["forks_count"],
    "licence": (d.get("license") or {}).get("spdx_id"),
    "langage": d["language"], "cree_le": d["created_at"], "dernier_push": d["pushed_at"],
    "archive": d["archived"],
    "issues_et_pr_ouvertes": d["open_issues_count"],
    "commits_total_branche_defaut": total(f"/commits?sha={d['default_branch']}"),
    "commits_90_derniers_jours": total(f"/commits?sha={d['default_branch']}&since={il_y_a_90j}T00:00:00Z"),
    "contributeurs": total("/contributors?anon=1"),
    "versions_recentes": [{"tag": v["tag_name"], "date": v["published_at"][:10], "prerelease": v["prerelease"]} for v in versions],
}
out = RACINE / f"outils/resultats/{solution}/identite-github-{aujourdhui}.json"
out.write_text(json.dumps(res, ensure_ascii=False, indent=2))
print(json.dumps(res, ensure_ascii=False, indent=2))
