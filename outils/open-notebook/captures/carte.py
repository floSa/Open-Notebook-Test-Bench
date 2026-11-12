"""Carte de l'interface d'Open Notebook (kit/PROMPT.md, phase C) : parcours de chaque page et des menus principaux.

Pour chaque page : capture de repérage pleine page dans docs/open-notebook/img/carte/, texte de la page et inventaire
des éléments (titres, onglets, boutons, champs, listes, interrupteurs, liens) dans
outils/resultats/open-notebook/captures/carte/. Interface en français (langue du navigateur fr-FR).
Lancement : outils/communs/captures/lancer.sh outils/open-notebook/captures/carte.py
"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
from commun_on import URL, Session, carnet, api

IMG = Path("docs/open-notebook/img/carte")
RES = Path("outils/resultats/open-notebook/captures/carte")
INVENTAIRE = """() => {
  const vis = e => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length);
  const txt = e => (e.innerText || e.getAttribute('aria-label') || e.getAttribute('title') || e.getAttribute('placeholder') || '').trim().replace(/\\s+/g, ' ');
  const pick = sel => [...document.querySelectorAll(sel)].filter(vis).map(txt).filter(Boolean);
  return {
    titres: pick('h1,h2,h3,h4'),
    onglets: pick('[role=tab]'),
    boutons: [...new Set(pick('button,[role=button]'))],
    champs: [...document.querySelectorAll('input,textarea')].filter(vis).map(e => e.getAttribute('placeholder') || e.getAttribute('aria-label') || e.name || e.type),
    listes: pick('[role=combobox],select'),
    interrupteurs: [...document.querySelectorAll('[role=switch],[role=checkbox],input[type=checkbox]')].filter(vis).map(e => (e.closest('label,div')?.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 80)),
    liens: [...new Set(pick('a'))],
  };
}"""


def relever(s, n, nom, plein=True, dialogue=False):
    IMG.mkdir(parents=True, exist_ok=True); RES.mkdir(parents=True, exist_ok=True)
    s.pg.wait_for_timeout(1500)
    s.pg.screenshot(path=str(IMG / f"{n:02d}-{nom}.png"), full_page=plein)
    zone = s.pg.get_by_role("dialog").last if dialogue and s.pg.get_by_role("dialog").count() else s.pg.locator("body")
    inv = s.pg.evaluate(INVENTAIRE)
    (RES / f"{n:02d}-{nom}.txt").write_text(zone.inner_text())
    (RES / f"{n:02d}-{nom}.json").write_text(json.dumps({"url": s.pg.url, **inv}, ensure_ascii=False, indent=1))
    print(f"{n:02d}-{nom}", s.pg.url, "| onglets", inv["onglets"][:12], "| boutons", inv["boutons"][:40], flush=True)


def essayer(f):
    try:
        f()
    except Exception as e:
        print("  (échec :", str(e).splitlines()[0][:160], ")", flush=True)


def main():
    with sync_playwright() as p:
        s = Session(p)
        s.aller("/login"); relever(s, 1, "connexion", plein=False)
        s.connexion()
        nb = carnet("Banc")
        src = api(f"/api/sources?notebook_id={nb}&limit=5")[0]["id"]
        pages = [("/notebooks", "carnets"), (f"/notebooks/{nb}", "carnet"), ("/sources", "sources"), (f"/sources/{src}", "source"),
                 ("/search", "demander-et-rechercher"), ("/podcasts", "podcasts"), ("/settings/models", "modeles"),
                 ("/transformations", "transformations"), ("/settings", "parametres"), ("/advanced", "avance")]
        n = 2
        for chemin, nom in pages:
            s.aller(chemin); relever(s, n, nom); n += 1
            if nom == "podcasts":
                for o in s.pg.get_by_role("tab").all()[1:]:
                    t = o.inner_text().strip()
                    o.click(); relever(s, n, "podcasts-" + t.lower().replace(" ", "-")[:20]); n += 1
            if nom == "demander-et-rechercher":
                for o in s.pg.get_by_role("tab").all()[1:]:
                    t = o.inner_text().strip()
                    o.click(); relever(s, n, "recherche-" + t.lower().replace(" ", "-")[:20]); n += 1
            if nom == "source":
                for o in s.pg.get_by_role("tab").all()[1:]:
                    t = o.inner_text().strip()
                    o.click(); relever(s, n, "source-" + t.lower().replace(" ", "-")[:20]); n += 1
        # menus et fenêtres
        s.aller("/notebooks")
        def creer():
            s.pg.get_by_role("button", name="Créer").first.click(); relever(s, n, "menu-creer", plein=False)
        essayer(creer); n += 1; s.pg.keyboard.press("Escape")
        def nouveau():
            s.pg.get_by_role("button", name="Nouveau Carnet").click(); relever(s, n, "fenetre-nouveau-carnet", plein=False)
        essayer(nouveau); n += 1; s.pg.keyboard.press("Escape")
        def langue():
            s.pg.get_by_role("button", name="Langue").click(); relever(s, n, "menu-langue", plein=False)
        essayer(langue); n += 1; s.pg.keyboard.press("Escape")
        def theme():
            s.pg.get_by_role("button", name="Thème").click(); relever(s, n, "menu-theme", plein=False)
        essayer(theme); n += 1; s.pg.keyboard.press("Escape")
        def actions():
            s.pg.keyboard.press("Control+k"); relever(s, n, "actions-rapides", plein=False)
        essayer(actions); n += 1; s.pg.keyboard.press("Escape")
        s.aller(f"/notebooks/{nb}")
        def ajout_source():
            s.pg.get_by_role("button", name="Ajouter la source").first.click(); relever(s, n, "fenetre-ajouter-source", plein=False)
        essayer(ajout_source); n += 1; s.pg.keyboard.press("Escape")
        s.aller(f"/notebooks/{nb}")
        def note():
            s.pg.get_by_role("button", name="Écrire une note").first.click(); relever(s, n, "fenetre-note", plein=False)
        essayer(note); n += 1; s.pg.keyboard.press("Escape")
        s.aller("/settings/models")
        def fournisseur():
            b = s.pg.get_by_role("button").filter(has_text="Ajouter").first
            b.click(); relever(s, n, "fenetre-ajout-fournisseur", plein=False)
        essayer(fournisseur); n += 1; s.pg.keyboard.press("Escape")
        s.b.close()


if __name__ == "__main__":
    main()
