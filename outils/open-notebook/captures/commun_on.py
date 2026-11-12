"""Outils communs aux scénarios Playwright d'Open Notebook (exécutés dans le conteneur Playwright, réseau rag-local).

Session : navigateur 1440 × 900, langue fr-FR, connexion par le mot de passe local (jamais visible : champ masqué
et masque noir posé avant toute capture de la page de connexion). ecran(...) : capture annotée (rectangle rouge,
pastille numérotée, outils/communs/captures/annoter.py) dans docs/open-notebook/img/<chapitre>/, texte de la page
dans outils/resultats/open-notebook/captures/<chapitre>/.
"""
import json, urllib.request
from pathlib import Path

from annoter import capture

URL = "http://rag-open-notebook:8502"
API = "http://rag-open-notebook:5055"
ENV = dict(l.split("=", 1) for l in Path("donnees/open-notebook/.env").read_text().splitlines() if "=" in l)
IMG = Path("docs/open-notebook/img")
TXT = Path("outils/resultats/open-notebook/captures")


def api(chemin, methode="GET", corps=None):
    h = {"Authorization": f"Bearer {ENV['OPEN_NOTEBOOK_PASSWORD']}"}
    data = None
    if corps is not None:
        data, h["Content-Type"] = json.dumps(corps).encode(), "application/json"
    req = urllib.request.Request(API + chemin, data=data, headers=h, method=methode)
    t = urllib.request.urlopen(req, timeout=120).read()
    return json.loads(t) if t else None


def carnet(nom):
    return next((n["id"] for n in api("/api/notebooks") if n["name"] == nom), None)


class Session:
    def __init__(self, p, chapitre=None):
        self.b = p.chromium.launch()
        self.ctx = self.b.new_context(viewport={"width": 1440, "height": 900}, locale="fr-FR")
        self.pg = self.ctx.new_page()
        self.chapitre = chapitre

    def aller(self, chemin, attendre=None):
        self.pg.goto(URL + chemin); self.pg.wait_for_load_state("networkidle")
        if attendre is not None:
            attendre.wait_for(state="visible", timeout=30000)
        self.pg.wait_for_timeout(800)

    def connexion(self):
        self.aller("/login")
        champ = self.pg.locator("input[type=password]")
        if champ.count():
            champ.fill(ENV["OPEN_NOTEBOOK_PASSWORD"]); self.pg.keyboard.press("Enter")
            self.pg.wait_for_url(lambda u: "/login" not in u, timeout=30000)
            self.pg.wait_for_load_state("networkidle"); self.pg.wait_for_timeout(800)

    def ecran(self, nom, elements=(), masques=(), plein=False, clip=None, attendre=None, chapitre=None):
        ch = chapitre or self.chapitre
        if attendre is not None:
            attendre.wait_for(state="visible", timeout=60000)
        self.pg.wait_for_timeout(500)
        return capture(self.pg, IMG / ch / f"{nom}.png", elements, masques, plein, clip, texte=TXT / ch / f"{nom}.txt")

    def fermer(self):
        self.b.close()
