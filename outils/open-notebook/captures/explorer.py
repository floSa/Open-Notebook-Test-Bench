"""Exploration de l'interface (libellés, liens, boutons) avant les captures. Lancé par outils/communs/captures/lancer.sh."""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "http://rag-open-notebook:8502"
ENV = dict(l.split("=", 1) for l in Path("donnees/open-notebook/.env").read_text().splitlines() if "=" in l)
OUT = Path("donnees/exploration"); OUT.mkdir(parents=True, exist_ok=True)
chemins = sys.argv[1:] or ["/notebooks"]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900}, locale="fr-FR")
    pg.goto(URL + "/"); pg.wait_for_load_state("networkidle")
    pg.screenshot(path=str(OUT / "00-accueil.png"))
    champs = pg.locator("input[type=password]")
    if champs.count():
        champs.first.fill(ENV["OPEN_NOTEBOOK_PASSWORD"]); pg.keyboard.press("Enter"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(1500)
    rapport = {}
    for i, c in enumerate(chemins, 1):
        pg.goto(URL + c); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(1500)
        pg.screenshot(path=str(OUT / f"{i:02d}{c.replace('/', '_')}.png"), full_page=True)
        rapport[c] = {"url": pg.url, "titre": pg.title(),
                      "liens": pg.eval_on_selector_all("a", "e => e.map(x => [x.innerText.trim(), x.getAttribute('href')]).filter(x => x[0])"),
                      "boutons": pg.eval_on_selector_all("button", "e => e.map(x => x.innerText.trim() || x.getAttribute('aria-label')).filter(Boolean)"),
                      "titres": pg.eval_on_selector_all("h1,h2,h3", "e => e.map(x => x.innerText.trim())")}
    (OUT / "rapport.json").write_text(json.dumps(rapport, ensure_ascii=False, indent=1))
    print(json.dumps(rapport, ensure_ascii=False)[:6000])
    b.close()
