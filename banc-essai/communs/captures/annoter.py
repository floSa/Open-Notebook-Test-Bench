"""Annotation des captures d'écran des manuels (kit/PROMPT.md, §6 bis).

annoter(page, [(locator, "libellé"), ...]) dessine dans la page un rectangle rouge autour de chaque élément et une
pastille numérotée (1, 2, 3...) à son coin supérieur gauche ; masquer(page, locator) recouvre un secret ;
retirer(page) efface tout. capture(...) enchaîne : attente des éléments, annotation, capture, retrait, et renvoie la
liste des libellés dans l'ordre des pastilles (pour écrire le tableau N° | Élément | Rôle).
Les éléments sont dessinés en position absolue dans le document : valables aussi en capture pleine page.
"""
from pathlib import Path

ROUGE = "#e10600"
_JS = """
([boites, classe]) => {
  for (const b of boites) {
    const r = document.createElement('div');
    r.className = classe;
    Object.assign(r.style, {position: 'absolute', left: (b.x - 4) + 'px', top: (b.y - 4) + 'px',
      width: (b.w + 8) + 'px', height: (b.h + 8) + 'px', border: '3px solid %(rouge)s', borderRadius: '6px',
      boxShadow: '0 0 0 2px rgba(255,255,255,.85)', zIndex: 2147483646, pointerEvents: 'none',
      background: b.masque ? '#222' : 'transparent'});
    document.body.appendChild(r);
    if (b.n) {
      const p = document.createElement('div');
      p.className = classe;
      p.textContent = b.n;
      Object.assign(p.style, {position: 'absolute', left: Math.max(0, b.x - 16) + 'px', top: Math.max(0, b.y - 16) + 'px',
        width: '26px', height: '26px', lineHeight: '26px', borderRadius: '50%%', background: '%(rouge)s',
        color: '#fff', font: 'bold 15px/26px sans-serif', textAlign: 'center', zIndex: 2147483647,
        pointerEvents: 'none', boxShadow: '0 0 0 2px #fff'});
      document.body.appendChild(p);
    }
  }
}
""" % {"rouge": ROUGE}
CLASSE = "rag-annotation-manuel"


def _boite(page, loc, n=None, masque=False):
    loc.wait_for(state="visible", timeout=15000)
    loc.scroll_into_view_if_needed(timeout=5000)
    b = loc.bounding_box()
    vw, vh = page.evaluate("[window.innerWidth, window.innerHeight]")
    # un élément sans taille ou hors de la fenêtre donnerait une pastille flottante sans rectangle : erreur explicite
    if not b or b["width"] < 2 or b["height"] < 2 or b["x"] + b["width"] < 0 or b["y"] + b["height"] < 0 \
            or b["x"] > vw or b["y"] > vh:
        raise ValueError(f"élément {n or 'masqué'} invisible ou hors de la fenêtre : {b} ; locator {loc}")
    sx, sy = page.evaluate("[window.scrollX, window.scrollY]")
    return {"x": b["x"] + sx, "y": b["y"] + sy, "w": b["width"], "h": b["height"], "n": n, "masque": masque}


def annoter(page, elements):
    """elements : liste de (locator, libellé). Renvoie les libellés numérotés."""
    boites = [_boite(page, loc, n=i) for i, (loc, _) in enumerate(elements, 1)]
    page.evaluate(_JS, [boites, CLASSE])
    return [(i, lib) for i, (_, lib) in enumerate(elements, 1)]


def masquer(page, locator):
    page.evaluate(_JS, [[_boite(page, locator, masque=True)], CLASSE])


def retirer(page):
    page.evaluate(f"() => document.querySelectorAll('.{CLASSE}').forEach(e => e.remove())")


def capture(page, chemin, elements=(), masques=(), plein=False, clip=None, texte=None):
    """Annote, capture dans `chemin` (PNG), retire. `texte` : fichier où enregistrer le texte de la page."""
    chemin = Path(chemin); chemin.parent.mkdir(parents=True, exist_ok=True)
    for m in masques:
        masquer(page, m)
    libelles = annoter(page, list(elements)) if elements else []
    page.wait_for_timeout(300)
    page.screenshot(path=str(chemin), full_page=plein, clip=clip)
    retirer(page)
    if texte:
        Path(texte).parent.mkdir(parents=True, exist_ok=True)
        Path(texte).write_text(page.inner_text("body"))
    print("capture", chemin, libelles, flush=True)
    return libelles
