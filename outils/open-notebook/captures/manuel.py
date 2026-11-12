"""Scénarios Playwright du manuel utilisateur d'Open Notebook (partie 1) : chaque action se fait à la souris, comme un
utilisateur, et chaque étape produit une capture annotée (rectangle rouge, pastille numérotée).

Lancement : outils/communs/captures/lancer.sh outils/open-notebook/captures/manuel.py <chapitre> [...]
Chapitres : voir SCENARIOS en bas du fichier. Images : docs/open-notebook/img/<chapitre>/ ; texte des pages :
outils/resultats/open-notebook/captures/<chapitre>/. Aucun secret visible : mot de passe et clés masqués avant capture.
"""
import os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
from commun_on import Session, api, carnet

CLE = os.environ.get("LLM_CENTRAL_KEY", "")


def menu(s, libelle):
    """Lien du menu de gauche."""
    return s.pg.get_by_role("link", name=libelle, exact=True).first


def bouton(s, libelle, exact=False):
    return s.pg.get_by_role("button", name=libelle, exact=exact).first


# ---------------------------------------------------------------- 02. Installer
def installer(s):
    s.chapitre = "02-installer"
    s.aller("/login")
    mdp = s.pg.locator("input[type=password]")
    s.ecran("01-connexion", [(mdp, "Mot de passe"), (bouton(s, "Se connecter"), "Se connecter")])
    s.connexion()
    s.aller("/settings/models")
    bloc = s.pg.get_by_text("OpenAI Compatible", exact=True).first.locator("xpath=ancestor::div[contains(@class,'rounded')][1]")
    defauts = s.pg.get_by_text("Attributions des modèles par défaut").first.locator("xpath=ancestor::div[contains(@class,'rounded')][1]")
    s.ecran("02-modeles", [(menu(s, "Modèles"), "Modèles"), (defauts, "Attributions"), (bloc, "OpenAI Compatible")], plein=True)


SCENARIOS = {"02": installer}

if __name__ == "__main__":
    with sync_playwright() as p:
        for nom in sys.argv[1:]:
            s = Session(p)
            try:
                if nom != "02":
                    s.connexion()
                SCENARIOS[nom](s)
            finally:
                s.fermer()
