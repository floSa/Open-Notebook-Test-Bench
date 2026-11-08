"""Captures des manuels Open Notebook (interface en français, langue du navigateur fr-FR).

Lancement : outils/communs/captures/lancer.sh outils/open-notebook/captures/captures.py <scénario> [...]
Scénarios : installation, prise-en-main, sources, recherche, transformations, podcasts, demo.
Images : docs/open-notebook/img/<manuel>/NN-nom.png. Aucun secret n'est saisi à l'écran avant capture.
"""
import json, sys, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "http://rag-open-notebook:8502"
API = "http://rag-open-notebook:5055"
ENV = dict(l.split("=", 1) for l in Path("donnees/open-notebook/.env").read_text().splitlines() if "=" in l)
IMG = Path("docs/open-notebook/img")


def api(chemin):
    req = urllib.request.Request(API + chemin, headers={"Authorization": f"Bearer {ENV['OPEN_NOTEBOOK_PASSWORD']}"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def carnet(nom):
    return next(n["id"] for n in api("/api/notebooks") if n["name"] == nom)


class Session:
    def __init__(self, p):
        self.b = p.chromium.launch()
        self.pg = self.b.new_page(viewport={"width": 1440, "height": 900}, locale="fr-FR")

    def shot(self, manuel, nom, plein=False):
        d = IMG / manuel; d.mkdir(parents=True, exist_ok=True)
        self.pg.wait_for_timeout(1200)
        self.pg.screenshot(path=str(d / f"{nom}.png"), full_page=plein)
        print("capture", d / f"{nom}.png", flush=True)

    def aller(self, chemin):
        self.pg.goto(URL + chemin); self.pg.wait_for_load_state("load"); self.pg.wait_for_timeout(3000)

    def connexion(self, manuel=None):
        self.aller("/")
        if manuel:
            self.shot(manuel, "01-connexion")
        self.pg.locator("input[type=password]").fill(ENV["OPEN_NOTEBOOK_PASSWORD"])
        self.pg.keyboard.press("Enter"); self.pg.wait_for_load_state("load"); self.pg.wait_for_timeout(3000)


def installation(s):
    s.connexion()
    s.aller("/settings/models"); s.shot("01-installation", "01-modeles", plein=True)
    s.aller("/settings"); s.shot("01-installation", "02-parametres", plein=True)


def prise_en_main(s):
    m = "02-prise-en-main"
    s.connexion(m)
    s.aller("/notebooks"); s.shot(m, "02-carnets")
    s.pg.get_by_role("button", name="Nouveau Carnet").click(); s.pg.wait_for_timeout(800)
    champ = s.pg.get_by_role("dialog").locator("input").first
    champ.fill("Démo prise en main"); s.shot(m, "03-nouveau-carnet")
    s.pg.keyboard.press("Escape")
    s.aller(f"/notebooks/{carnet('Essai installation')}"); s.shot(m, "04-carnet-chat-citation")
    s.pg.get_by_role("button", name="Ajouter la source").click(); s.pg.wait_for_timeout(800)
    s.shot(m, "05-ajouter-source")
    s.pg.keyboard.press("Escape")
    lien = s.pg.get_by_text("source:", exact=False).last
    if lien.count():
        lien.click(); s.pg.wait_for_timeout(1500); s.shot(m, "06-ouverture-citation")


def transformations(s):
    s.connexion()
    s.aller("/transformations"); s.shot("05-notes-et-transformations", "01-transformations", plein=True)
    s.aller(f"/notebooks/{carnet('Banc')}"); s.shot("05-notes-et-transformations", "02-carnet-notes")


def recherche(s):
    m = "06-recherche"
    s.connexion()
    s.aller("/search"); s.shot(m, "01-demander-et-rechercher")
    s.pg.get_by_role("tab", name="Recherche").click() if s.pg.get_by_role("tab", name="Recherche").count() else \
        s.pg.get_by_role("button", name="Recherche").first.click()
    s.pg.wait_for_timeout(800)
    champ = s.pg.locator("input[type=text], input:not([type])").last
    champ.fill("Où ranger les accumulateurs et à quelle température ?"); s.pg.keyboard.press("Enter")
    s.pg.wait_for_timeout(8000); s.shot(m, "02-resultats-recherche", plein=True)
    s.pg.get_by_text("Recherche vectorielle", exact=True).click(); s.pg.wait_for_timeout(500)
    s.pg.get_by_role("button", name="Recherche").last.click()
    s.pg.wait_for_timeout(10000); s.shot(m, "03-resultats-vectoriels", plein=True)


def chat(s):
    m = "04-chat-et-citations"
    s.connexion()
    s.aller(f"/notebooks/{carnet('Banc')}")
    carte = s.pg.get_by_text("rapport-annuel-2025.pdf").first.locator("xpath=ancestor::div[contains(@class,'border')][1]")
    boutons = carte.locator("button")
    print("boutons de la carte :", [b.get_attribute("aria-label") or b.get_attribute("title") or b.inner_text() for b in boutons.all()])
    boutons.first.hover(); s.pg.wait_for_timeout(800)
    s.shot(m, "01-contexte-par-source")


def podcasts(s):
    m = "07-podcasts"
    s.connexion()
    s.aller("/podcasts"); s.shot(m, "01-episodes", plein=True)
    print("onglets :", [o.inner_text() for o in s.pg.get_by_role("tab").all()])
    onglets = s.pg.get_by_role("tab")
    if onglets.count() > 1:
        onglets.nth(1).click(); s.pg.wait_for_timeout(1500); s.shot(m, "02-profils", plein=True)


def recettes(s):
    m = "09-recettes"
    s.connexion()
    s.aller(f"/notebooks/{carnet('Démo Vélanor')}"); s.shot(m, "01-carnet-demo")
    b = s.pg.get_by_role("button", name="Sessions")
    if b.count():
        b.first.click(); s.pg.wait_for_timeout(1200); s.shot(m, "02-sessions")


SCENARIOS = {"recettes": recettes, "podcasts": podcasts, "chat": chat, "installation": installation, "prise-en-main": prise_en_main, "transformations": transformations,
             "recherche": recherche}

if __name__ == "__main__":
    with sync_playwright() as p:
        for nom in sys.argv[1:]:
            s = Session(p)
            try:
                SCENARIOS[nom](s)
            finally:
                s.b.close()
