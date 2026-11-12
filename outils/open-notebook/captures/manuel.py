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
import re
from commun_on import CLE_CENTRAL, Session, api, carnet


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


def nav(s, libelle):
    """Entrée du menu de gauche (premier élément de ce texte dans la page : le menu vient en premier)."""
    return s.pg.get_by_text(libelle, exact=True).first


def toast(s):
    return s.pg.locator("[data-sonner-toast]").first


def dialogue(s):
    return s.pg.get_by_role("dialog").last


# ---------------------------------------------------------------- 03. Premiers pas
def premiers_pas(s):
    s.chapitre = "03-premiers-pas"; pg = s.pg
    s.aller("/notebooks", attendre=bouton(s, "Nouveau Carnet"))
    s.ecran("01-menu", [(bouton(s, "Créer", exact=True), "Créer"), (nav(s, "Sources"), "Sources"), (nav(s, "Carnets"), "Carnets"),
                        (nav(s, "Demander et rechercher"), "Demander et rechercher"), (nav(s, "Podcasts"), "Podcasts"),
                        (nav(s, "Modèles"), "Modèles")])
    s.ecran("02-bas-du-menu", [(pg.get_by_text("Actions rapides").first, "Actions rapides"), (bouton(s, "Thème"), "Thème"),
                               (bouton(s, "Langue"), "Langue"), (bouton(s, "Se déconnecter"), "Se déconnecter")])
    s.ecran("03-page-carnets", [(bouton(s, "Vue en mosaïque"), "Vue en mosaïque"), (bouton(s, "Vue en liste"), "Vue en liste"),
                                (pg.get_by_placeholder("Rechercher des carnets..."), "Rechercher des carnets"),
                                (bouton(s, "Nouveau Carnet"), "Nouveau Carnet"), (pg.get_by_text("Consultés récemment").first, "Consultés récemment"),
                                (pg.get_by_text("Carnets actifs").first, "Carnets actifs")])
    bouton(s, "Langue").click()
    s.ecran("04-menu-langue", [(pg.get_by_role("menuitem", name="Français").or_(pg.get_by_role("menuitemradio", name="Français")).first, "Français")],
            attendre=pg.get_by_text("Français", exact=True).first)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    bouton(s, "Thème").click()
    s.ecran("05-menu-theme", [(pg.get_by_role("menuitem", name="Clair").first, "Clair"), (pg.get_by_role("menuitem", name="Sombre").first, "Sombre"),
                              (pg.get_by_role("menuitem", name="Système").first, "Système")], attendre=pg.get_by_text("Sombre", exact=True).first)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    pg.keyboard.press("Control+k")
    s.ecran("06-actions-rapides", [(pg.get_by_placeholder("Entrez votre recherche...").first, "Entrez votre recherche...")],
            attendre=pg.get_by_placeholder("Entrez votre recherche...").first)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    bouton(s, "Créer", exact=True).click()
    s.ecran("07-menu-creer", [(pg.get_by_role("menuitem", name="Source").first, "Source"), (pg.get_by_role("menuitem", name="Carnet").first, "Carnet"),
                              (pg.get_by_role("menuitem", name="Podcast").first, "Podcast")], attendre=pg.get_by_role("menuitem").first)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)

    # Déclarer les modèles : la configuration « llm-central » posée par l'installateur est retirée, puis refaite à la souris.
    for c in api("/api/credentials"):
        if c["name"] == "llm-central":
            api(f"/api/credentials/{c['id']}", "DELETE")
    s.aller("/settings/models", attendre=pg.get_by_text("Attributions des modèles par défaut").first)
    titre = pg.get_by_text("OpenAI Compatible", exact=True).first
    bloc = titre.locator("xpath=ancestor::div[.//button[contains(., 'Ajouter une configuration')]][1]")
    ajout = bloc.get_by_role("button", name="Ajouter une configuration").last
    ajout.scroll_into_view_if_needed()
    s.ecran("08-fournisseur", [(titre, "OpenAI Compatible"), (ajout, "Ajouter une configuration")])
    ajout.click()
    d = dialogue(s); d.wait_for(state="visible")
    champs = d.locator("input")
    nom, cle, url = champs.nth(0), champs.nth(1), champs.nth(2)
    nom.fill("llm-central"); cle.fill(CLE_CENTRAL); url.fill("http://llm-central:8080/v1")
    valider = d.get_by_role("button", name="Ajouter une configuration")
    s.ecran("09-fenetre-configuration", [(nom, "Nom de la configuration"), (cle, "Clé API"), (url, "URL de base"), (valider, "Ajouter une configuration")],
            masques=[cle])
    valider.click(); pg.wait_for_timeout(2500)
    carte = pg.get_by_text("llm-central", exact=True).first.locator("xpath=ancestor::div[.//button[normalize-space()='Test']][1]")
    carte.get_by_role("button", name="Test").click()
    t = toast(s); t.wait_for(state="visible", timeout=30000); pg.wait_for_timeout(800)
    print("toast :", t.inner_text(), flush=True)
    s.ecran("10-test", [(carte.get_by_role("button", name="Test"), "Test"), (t, "Résultat du test"), (carte.get_by_role("button", name="Models"), "Models")])
    pg.wait_for_timeout(4000)
    for typ, nom_modele, capture in (("Lang", "chat", True), ("Embed", "embed", False), ("STT|Speech|Transcri", "transcribe", False)):
        carte.get_by_role("button", name="Models").click()
        d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(1500)
        liste = d.get_by_role("combobox").first
        liste.click(); pg.wait_for_timeout(500)
        print("types :", [o.inner_text() for o in pg.get_by_role("option").all()], flush=True)
        pg.get_by_role("option").filter(has_text=re.compile(typ, re.I)).first.click(); pg.wait_for_timeout(800)
        case = d.get_by_text(nom_modele, exact=True).first
        case.click(); pg.wait_for_timeout(500)
        ajouter = d.get_by_role("button", name=re.compile(r"^Ajouter \(\d+\)"))
        if capture:
            s.ecran("11-decouverte", [(liste, "Type de modèle"), (case, nom_modele), (ajouter, "Ajouter (1)")])
        ajouter.click(); pg.wait_for_timeout(2000)
        if d.is_visible():
            pg.keyboard.press("Escape")
    s.aller("/settings/models", attendre=pg.get_by_text("Attributions des modèles par défaut").first)
    def liste_de(libelle):
        return pg.get_by_text(re.compile("^" + re.escape(libelle))).first.locator("xpath=following::*[@role='combobox'][1]")
    libelles = ["Modèle de Chat", "Modèle d'Embedding", "Modèle de Synthèse Vocale (TTS)", "Modèle de Transcription Vocale (STT)"]
    def choisir(l, choix):
        l.scroll_into_view_if_needed(); l.click(force=True); pg.wait_for_timeout(800)
        if not pg.get_by_role("option").count():  # liste à moitié hors de la fenêtre (1440 px) : ouverture au clavier
            pg.keyboard.press("Escape"); l.focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(800)
        pg.get_by_role("option").filter(has_text=re.compile("^" + choix)).first.click(); pg.wait_for_timeout(1500)
        print("choix", choix, "->", [t.inner_text().replace("\n", " ") for t in pg.locator("[data-sonner-toast]").all()],
              [d.inner_text()[:300] for d in pg.get_by_role("alertdialog").all()], flush=True)
    for libelle, choix in ((libelles[0], "chat"), (libelles[3], "transcribe")):
        choisir(liste_de(libelle), choix)
    pg.mouse.wheel(0, -2000); pg.wait_for_timeout(500)
    auto = bouton(s, "Attribution automatique des défauts")
    s.ecran("12-attribution-automatique", [(pg.get_by_text(re.compile("^Modèles requis manquants")).first, "Modèles requis manquants"),
                                          (auto, "Attribution automatique des défauts")])
    auto.click(); pg.wait_for_timeout(2500)
    for role in ("alertdialog", "dialog"):
        if pg.get_by_role(role).count():
            print(role, ":", pg.get_by_role(role).last.inner_text()[:500], flush=True)
    print("après attribution automatique :", [t.inner_text().replace("\n", " ") for t in pg.locator("[data-sonner-toast]").all()], flush=True)
    if not (liste_de(libelles[1]).inner_text() or "").strip():
        choisir(liste_de(libelles[1]), "embed")
        ad = pg.get_by_role("alertdialog").last
        if ad.count():
            boutons = [b for b in ad.get_by_role("button").all() if b.inner_text().strip()]
            print("boutons de confirmation :", [b.inner_text() for b in boutons], flush=True)
            ok = [b for b in boutons if b.inner_text().strip() != "Annuler"][-1]
            s.ecran("13-changement-embedding", [(ad.get_by_text("Changement de modèle d'embedding").first, "Changement de modèle d'embedding"),
                                                (ok, ok.inner_text().strip())])
            ok.click(); pg.wait_for_timeout(3000)
            print("après confirmation :", pg.url, [t.inner_text().replace("\n", " ") for t in pg.locator("[data-sonner-toast]").all()], flush=True)
            if "/settings/models" not in pg.url:  # « Changer & Aller à la reconstruction » ouvre la page Avancé (chapitre 10)
                s.aller("/settings/models", attendre=pg.get_by_text("Attributions des modèles par défaut").first)
    for libelle in ("Modèle de Transformation", "Modèle d'Outils", "Modèle à large contexte"):
        l = liste_de(libelle)
        if "chat" not in (l.inner_text() or ""):
            choisir(l, "chat")
    pg.mouse.wheel(0, -2000); pg.wait_for_timeout(500)
    listes = [liste_de(l) for l in libelles]
    s.ecran("15-attributions", [(listes[0], "Modèle de Chat"), (listes[1], "Modèle d'Embedding"),
                                (listes[2], "Modèle de Synthèse Vocale (TTS)"), (listes[3], "Modèle de Transcription Vocale (STT)")])


def attendre_sources(nb_id, n=1, delai=600):
    """Attend que n sources du carnet soient traitées (ou en échec) : l'interface l'affiche sur la carte de la source."""
    import time
    fin = time.time() + delai
    while time.time() < fin:
        srcs = api(f"/api/sources?notebook_id={nb_id}&limit=100")
        etats = [api(f"/api/sources/{x['id']}/status")["status"] for x in srcs]
        if len(etats) >= n and all(e in ("completed", "failed") for e in etats):
            return etats
        time.sleep(4)
    return etats


def attendre_reponse(s, avant, delai=300):
    """Attend une nouvelle réponse du modèle dans la colonne de discussion (le nombre de blocs « Références » ou de messages
    augmente, puis le texte se stabilise)."""
    pg = s.pg
    import time
    fin = time.time() + delai
    while time.time() < fin:
        if pg.get_by_text("source:", exact=False).count() > avant or pg.locator("text=/Références|References/").count() > avant:
            break
        pg.wait_for_timeout(2000)
    pg.wait_for_timeout(4000)


def icone_contexte(s, titre):
    """Icône de mode de contexte d'une carte de source (aperçus, contenu complet, exclu)."""
    return s.pg.get_by_text(titre, exact=True).first.locator("xpath=ancestor::div[.//button][1]").locator("button").first


def citation(s):
    """Dernier lien de citation d'une réponse (source:… ou source_insight:…)."""
    return s.pg.locator("a, button").filter(has_text=re.compile(r"^\s*source(_insight)?:")).last


def assistant_source(s, chemin=None, url=None, texte=None, titre=None, captures=None, carnets=None):
    """Assistant « Ajouter une nouvelle source » (trois étapes). captures : préfixes de noms d'images, ou None."""
    pg = s.pg; d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    if chemin:
        onglet = d.get_by_role("tab", name="Télécharger un fichier"); onglet.click(); pg.wait_for_timeout(600)
        d.locator("input[type=file]").set_input_files(chemin if isinstance(chemin, list) else [chemin]); pg.wait_for_timeout(1200)
        zone = d.locator("input[type=file]").locator("xpath=ancestor::div[1]")
    elif url:
        onglet = d.get_by_role("tab", name="Ajouter une URL"); onglet.click(); pg.wait_for_timeout(600)
        zone = d.locator("textarea").first; zone.fill(url)
    else:
        onglet = d.get_by_role("tab", name="Saisir du texte"); onglet.click(); pg.wait_for_timeout(600)
        zone = d.locator("textarea").first; zone.fill(texte)
    if titre:
        d.get_by_placeholder("Donnez un titre descriptif à votre source").fill(titre)
    suivant = d.get_by_role("button", name="Suivant")
    print("étape 1 :", d.inner_text()[:600].replace("\n", "|"), flush=True)
    if captures:
        s.ecran(f"{captures[0]}", [(onglet, onglet.inner_text().strip()), (zone, "contenu"), (suivant, "Suivant")])
    suivant.click(); pg.wait_for_timeout(1200)
    print("étape 2 :", d.inner_text()[:900].replace("\n", "|"), flush=True)
    if carnets:
        for c in carnets:
            d.get_by_text(c, exact=True).first.click(); pg.wait_for_timeout(300)
    if captures and len(captures) > 1:
        s.ecran(f"{captures[1]}", [(d.get_by_text("Carnets", exact=True).first, "Carnets"), (suivant, "Suivant")])
    suivant.click(); pg.wait_for_timeout(1200)
    print("étape 3 :", d.inner_text()[:1200].replace("\n", "|"), flush=True)
    fin = d.get_by_role("button", name="Terminé")
    if captures and len(captures) > 2:
        s.ecran(f"{captures[2]}", [(d.get_by_text("Dense Summary", exact=True).first, "Dense Summary"),
                                   (d.get_by_text("Activer l'indexation pour la recherche").first, "Activer l'indexation pour la recherche"), (fin, "Terminé")])
    fin.click(); pg.wait_for_timeout(2500)


# ---------------------------------------------------------------- 04. Première question
def premiere_question(s):
    s.chapitre = "04-premiere-question"; pg = s.pg
    ancien = carnet("Premier essai")
    if ancien:
        api(f"/api/notebooks/{ancien}?delete_exclusive_sources=true", "DELETE")
    s.aller("/notebooks", attendre=bouton(s, "Nouveau Carnet"))
    bouton(s, "Nouveau Carnet").click()
    d = dialogue(s); d.wait_for(state="visible")
    champs = d.locator("input, textarea")
    champs.nth(0).fill("Premier essai"); champs.nth(1).fill("Une page de la FAQ du service après-vente")
    creer = d.get_by_role("button", name="Créer un nouveau carnet")
    s.ecran("01-nouveau-carnet", [(champs.nth(0), "Nom"), (champs.nth(1), "Description"), (creer, "Créer un nouveau carnet")])
    creer.click(); pg.wait_for_timeout(2500)
    if "/notebooks/" not in pg.url:
        pg.get_by_text("Premier essai", exact=True).first.click(); pg.wait_for_timeout(2500)
    ajout = pg.locator("button:has-text('Ajouter la source')").first
    s.ecran("02-carnet-vide", [(ajout, "Ajouter la source"), (bouton(s, "Écrire une note"), "Écrire une note"),
                               (pg.get_by_text("Commencer une conversation sur ce Carnet").first, "Commencer une conversation")])
    ajout.click(); pg.wait_for_timeout(600)
    item = pg.get_by_role("menuitem", name="Ajouter la source")
    s.ecran("03-menu-ajouter", [(item, "Ajouter la source"), (pg.get_by_role("menuitem", name="Ajouter des sources existantes"), "Ajouter des sources existantes")])
    item.click()
    assistant_source(s, chemin="corpus/documents/faq-sav.html", captures=["04-assistant-fichier", "05-assistant-carnets", "06-assistant-traiter"])
    nb = carnet("Premier essai")
    print("traitement :", attendre_sources(nb, 1), flush=True)
    s.aller(f"/notebooks/{nb}", attendre=pg.get_by_text("faq-sav.html").first)
    bouton(s, "Écrire une note").locator("xpath=following::button[1]").click(); pg.wait_for_timeout(800)  # replie la colonne NOTES
    icone = icone_contexte(s, "faq-sav.html")
    avant_ctx = pg.get_by_text("Context:").first.locator("xpath=ancestor::div[1]").inner_text()
    icone.click(); pg.wait_for_timeout(1500)
    print("contexte :", avant_ctx.replace("\n", " "), "->", pg.get_by_text("Context:").first.locator("xpath=ancestor::div[1]").inner_text().replace("\n", " "), flush=True)
    question = pg.get_by_placeholder(re.compile("Posez n'importe quelle question"))
    question.fill("Quelle est la durée de garantie du cadre ?")
    envoyer = question.locator("xpath=following::button[1]")
    s.ecran("07-question", [(icone, "Mode de contexte"), (pg.get_by_text("Context:").first.locator("xpath=ancestor::div[1]"), "Context"),
                            (question, "Question"), (envoyer, "Envoyer")])
    avant = pg.get_by_text("source:", exact=False).count()
    envoyer.click()
    attendre_reponse(s, avant)
    cit = citation(s)
    bulle = cit.locator("xpath=ancestor::div[contains(@class,'rounded')][1]")
    bulle.scroll_into_view_if_needed()
    s.ecran("08-reponse", [(bulle, "Réponse"), (cit, "Citation"), (pg.get_by_text("Context:").first, "Context")])
    cit.click(); pg.wait_for_timeout(3000)
    print("après clic citation :", pg.url, [d.inner_text()[:200] for d in pg.get_by_role("dialog").all()], flush=True)
    d = dialogue(s)
    s.ecran("09-source-citee", [(d.get_by_role("tab", name="Contenu"), "Contenu"), (d.get_by_role("tab", name=re.compile("^Analyses")), "Analyses"),
                                (d.get_by_role("tab", name="Détails"), "Détails"), (d.get_by_role("button", name="Discuter avec Sources"), "Discuter avec Sources")])


SCENARIOS = {"02": installer, "03": premiers_pas, "04": premiere_question}

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
