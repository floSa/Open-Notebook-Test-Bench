"""Sonde de l'interface : ouvre menus et fenêtres et relève leur contenu (menuitem, option, dialog), pour écrire la carte
de l'interface et les scénarios. Sortie : outils/resultats/open-notebook/captures/carte/sonde.json."""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
from commun_on import Session, carnet

OUT = Path("outils/resultats/open-notebook/captures/carte/sonde.json")
JS = """() => { const v = e => !!(e.offsetWidth || e.offsetHeight);
  const t = s => [...document.querySelectorAll(s)].filter(v).map(e => (e.innerText || e.getAttribute('aria-label') || '').trim().replace(/\\s+/g,' ')).filter(Boolean);
  return {menu: t('[role=menuitem],[role=menuitemradio],[role=option]'), dialogue: t('[role=dialog]').map(x => x.slice(0, 1500))}; }"""
res = {}
def sonde(s, nom, action):
    try:
        action(); s.pg.wait_for_timeout(1200); res[nom] = s.pg.evaluate(JS)
    except Exception as e:
        res[nom] = {"erreur": str(e).splitlines()[0][:200]}
    print(nom, json.dumps(res[nom], ensure_ascii=False)[:700], flush=True)
    s.pg.keyboard.press("Escape"); s.pg.wait_for_timeout(500)

with sync_playwright() as p:
    s = Session(p); s.connexion(); B = lambda n, **k: s.pg.get_by_role("button", name=n, **k).first
    s.aller("/notebooks")
    for nom, b in [("creer", "Créer"), ("langue", "Langue"), ("theme", "Thème")]:
        sonde(s, nom, lambda b=b: B(b).click())
    nb = carnet("Banc"); s.aller(f"/notebooks/{nb}")
    sonde(s, "ajouter-source", lambda: s.pg.locator("button:has-text('Ajouter la source')").first.click())
    sonde(s, "ajouter-source-fleche", lambda: s.pg.locator("button:has-text('Ajouter la source') + button, button:has-text('Ajouter la source') ~ button").first.click())
    sonde(s, "contexte", lambda: B("Contexte").click())
    sonde(s, "sessions", lambda: B("Sessions").click())
    sonde(s, "modele-chat", lambda: B("chat").click())
    sonde(s, "selection-sources", lambda: s.pg.locator("text=SOURCES").locator("xpath=following::button[1]").click())
    sonde(s, "icone-source", lambda: s.pg.locator("text=rapport-annuel-2025.pdf").first.locator("xpath=ancestor::div[contains(@class,'border')][1]//button").first.click())
    s.aller("/podcasts")
    sonde(s, "generer-podcast", lambda: B("Générer un podcast").click())
    s.pg.get_by_role("tab", name="Profils").click(); s.pg.wait_for_timeout(800)
    sonde(s, "creer-intervenant", lambda: B("Créer un intervenant").click())
    sonde(s, "creer-profil", lambda: B("Créer un profil").click())
    s.aller("/transformations")
    sonde(s, "creer-transformation", lambda: B("Créer une nouvelle").click())
    sonde(s, "playground", lambda: s.pg.get_by_role("tab", name="Bac à sable (Playground)").click())
    s.aller("/settings/models")
    sonde(s, "models-decouverte", lambda: B("Models").click())
    sonde(s, "modifier-config", lambda: B("Modifier").click())
    s.aller("/search")
    sonde(s, "carnets-portee", lambda: s.pg.get_by_role("combobox").first.click())
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    s.fermer()
