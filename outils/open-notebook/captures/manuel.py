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
    return s.pg.get_by_text(titre if isinstance(titre, re.Pattern) else re.compile("^" + re.escape(titre) + "$")).first.locator("xpath=ancestor::div[.//button][1]").locator("button").first


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
    faq = re.compile(r"^faq-sav( \(\d\))?\.html$")  # suffixe « (1) » si le fichier existe déjà dans un autre carnet
    s.aller(f"/notebooks/{nb}", attendre=pg.get_by_text(faq).first)
    bouton(s, "Écrire une note").locator("xpath=following::button[1]").click(); pg.wait_for_timeout(800)  # replie la colonne NOTES
    icone = icone_contexte(s, faq)
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


DEMO = "Démo Vélanor"
CORPUS = sorted(str(f) for f in Path("corpus/documents").iterdir() if f.is_file())


def creer_carnet(s, nom, description):
    """Crée un carnet par le menu « Créer » › « Carnet » (même fenêtre qu'au chapitre 04)."""
    pg = s.pg
    bouton(s, "Créer", exact=True).click(); pg.get_by_role("menuitem", name="Carnet").click()
    d = dialogue(s); d.wait_for(state="visible")
    champs = d.locator("input, textarea"); champs.nth(0).fill(nom); champs.nth(1).fill(description)
    d.get_by_role("button", name="Créer un nouveau carnet").click(); pg.wait_for_timeout(2500)
    nb = carnet(nom)
    if "/notebooks/" not in pg.url:
        s.aller(f"/notebooks/{nb}")
    return nb


# ---------------------------------------------------------------- 05. Sources
def sources(s):
    s.chapitre = "05-sources"; pg = s.pg
    ancien = carnet(DEMO)
    if ancien and len(api(f"/api/sources?notebook_id={ancien}&limit=100")) >= 9:  # carnet déjà construit : reprise sans retraiter les documents
        return sources_apres_ajout(s, ancien)
    if ancien:
        api(f"/api/notebooks/{ancien}?delete_exclusive_sources=true", "DELETE")
    s.aller("/notebooks", attendre=bouton(s, "Nouveau Carnet"))
    nb = creer_carnet(s, DEMO, "Dossier de démonstration : documents fictifs de l'entreprise Vélanor")
    pg.locator("button:has-text('Ajouter la source')").first.click(); pg.get_by_role("menuitem", name="Ajouter la source").click()
    d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(600)
    onglet = d.get_by_role("tab", name="Télécharger un fichier"); onglet.click(); pg.wait_for_timeout(500)
    d.locator("input[type=file]").set_input_files(CORPUS); pg.wait_for_timeout(1200)
    s.ecran("01-plusieurs-fichiers", [(onglet, "Télécharger un fichier"), (d.get_by_text(re.compile(r"^\d+ fichier\(s\)")).first, "9 fichier(s)"),
                                      (d.get_by_text(re.compile("^Sélectionnez plusieurs fichiers")).first, "Formats acceptés")])
    d.get_by_role("button", name="Suivant").click(); pg.wait_for_timeout(800)
    d.get_by_role("button", name="Suivant").click(); pg.wait_for_timeout(800)
    d.get_by_role("button", name="Terminé").click(); pg.wait_for_timeout(3000)
    if d.is_visible():
        print("fenêtre après Terminé :", d.inner_text()[:800].replace("\n", "|"), flush=True)
        pg.screenshot(path="donnees/exploration/apres-termine.png")
        d.wait_for(state="hidden", timeout=120000)
    pg.wait_for_timeout(1500)
    pg.screenshot(path="donnees/exploration/traitement.png")
    s.ecran("02-traitement-en-cours", [(pg.get_by_text("Traitement", exact=True).first, "Traitement"),
                                       (pg.get_by_text(re.compile("^Processing")).first, "Processing..."),
                                       (pg.get_by_text(re.compile(r"source\(s\) créée\(s\)")).first, "9 source(s) créée(s) avec succès")])
    print("traitement :", attendre_sources(nb, 9, 900), flush=True)
    sources_apres_ajout(s, nb)


def sources_apres_ajout(s, nb):
    pg = s.pg
    s.aller(f"/notebooks/{nb}", attendre=pg.get_by_text("faq-sav.html").first)
    # la source en échec garde le titre provisoire « Processing... » : repérée par son badge « Échec »
    echec = pg.get_by_text("Échec", exact=True).first.locator("xpath=ancestor::div[.//button][1]")
    echec.scroll_into_view_if_needed()
    s.ecran("03-source-en-echec", [(pg.get_by_text("Échec", exact=True).first, "Échec"), (bouton(s, "Réessayer le traitement"), "Réessayer le traitement")])
    # lien web : formulaire montré, puis annulé (pas d'accès à un site extérieur pendant les essais)
    pg.locator("button:has-text('Ajouter la source')").first.click(); pg.get_by_role("menuitem", name="Ajouter la source").click()
    d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(600)
    onglet = d.get_by_role("tab", name="Ajouter une URL"); onglet.click()
    zone = d.locator("textarea").first; zone.fill("https://exemple.com/article1")
    s.ecran("04-ajouter-url", [(onglet, "Ajouter une URL"), (zone, "URL(s)"), (d.get_by_placeholder("Donnez un titre descriptif à votre source"), "Titre (Optionnel)")])
    d.get_by_role("button", name="Annuler").click(); pg.wait_for_timeout(800)
    # texte saisi
    pg.locator("button:has-text('Ajouter la source')").first.click(); pg.get_by_role("menuitem", name="Ajouter la source").click()
    d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(600)
    onglet = d.get_by_role("tab", name="Saisir du texte"); onglet.click(); pg.wait_for_timeout(500)
    zone = d.locator("textarea").first
    zone.fill("Compte rendu d'appel du 5 novembre 2025 avec le transporteur Loire Fret : les livraisons vers Nantes passent "
              "au mardi et au vendredi à partir de janvier 2026. Contact : Claire Martin.")
    titre = d.get_by_placeholder("Donnez un titre descriptif à votre source"); titre.fill("Appel transporteur Loire Fret")
    s.ecran("05-saisir-texte", [(onglet, "Saisir du texte"), (zone, "Texte"), (titre, "Titre")])
    d.get_by_role("button", name="Suivant").click(); pg.wait_for_timeout(800)
    d.get_by_role("button", name="Suivant").click(); pg.wait_for_timeout(800)
    d.get_by_role("button", name="Terminé").click(); pg.wait_for_timeout(3000)
    print("texte :", attendre_sources(nb, 10, 300), flush=True)
    # page Sources
    s.aller("/sources", attendre=pg.get_by_text("Toutes les sources").first)
    ligne = pg.get_by_text("rapport-annuel-2025.pdf").first
    s.ecran("06-page-sources", [(pg.get_by_text("Type", exact=True).first, "Type"), (pg.get_by_text("Aperçus", exact=True).first, "Aperçus"),
                                (pg.get_by_text("Indexé (Embedded)").first, "Indexé (Embedded)"), (ligne, "Ligne d'une source")])
    ligne.click(); pg.wait_for_timeout(3000)
    pg.get_by_role("tab", name="Détails").click(); pg.wait_for_timeout(1500)
    s.ecran("07-source-details", [(bouton(s, "Back to Sources"), "Back to Sources"), (pg.get_by_role("tab", name="Détails"), "Détails"),
                                  (bouton(s, "Télécharger"), "Télécharger"), (pg.get_by_placeholder(re.compile("Posez n'importe quelle question")), "Question sur ce document")])


def sources_suite(s):
    """Suite du chapitre 05, jouée après le chapitre 04 (carnet « Premier essai ») : le carnet de démonstration est créé
    d'abord, pour que ses documents gardent leur nom (un fichier déjà téléversé sous le même nom reçoit un suffixe « (1) »)."""
    s.chapitre = "05-sources"; pg = s.pg
    # ajouter une source existante au carnet « Premier essai »
    pe = carnet("Premier essai")
    if pe:
        s.aller(f"/notebooks/{pe}", attendre=pg.locator("button:has-text('Ajouter la source')").first)
        pg.locator("button:has-text('Ajouter la source')").first.click(); pg.get_by_role("menuitem", name="Ajouter des sources existantes").click()
        d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(1500)
        print("existantes :", d.inner_text()[:500].replace("\n", "|"), flush=True)
        champ = d.locator("input").first; champ.fill("cse"); pg.wait_for_timeout(1500)
        choix = d.get_by_text("cse-2025-10-14.md").first
        case = d.get_by_role("checkbox").first if d.get_by_role("checkbox").count() else choix
        print("cases :", d.get_by_role("checkbox").count(), flush=True)
        case.click(); pg.wait_for_timeout(500)
        valider = d.get_by_role("button").filter(has_text=re.compile("Ajouter")).last
        s.ecran("08-sources-existantes", [(champ, "Recherche"), (choix, "cse-2025-10-14.md"), (valider, valider.inner_text().strip())])
        valider.click(); pg.wait_for_timeout(2000)
        carte = pg.get_by_text("cse-2025-10-14.md").first.locator("xpath=ancestor::div[.//button][1]")
        carte.hover(); pg.wait_for_timeout(400); carte.locator("button").last.click(); pg.wait_for_timeout(600)
        s.ecran("09-menu-source", [(pg.get_by_role("menuitem", name="Retirer du carnet"), "Retirer du carnet"),
                                   (pg.get_by_role("menuitem", name="Supprimer la source"), "Supprimer la source")])
        pg.get_by_role("menuitem", name="Retirer du carnet").click(); pg.wait_for_timeout(1500)
        for r in ("alertdialog", "dialog"):
            if pg.get_by_role(r).count():
                print("retirer :", pg.get_by_role(r).last.inner_text()[:300], flush=True)
                pg.get_by_role(r).last.get_by_role("button").filter(has_text=re.compile("Retirer|Confirmer|Supprimer")).last.click(); pg.wait_for_timeout(1500)
        bouton(s, "Archiver").click(); pg.wait_for_timeout(2000)
        print("après archivage :", pg.url, flush=True)
        s.aller("/notebooks", attendre=bouton(s, "Nouveau Carnet"))
        print("carnets :", pg.locator("main").inner_text()[:800].replace("\n", "|"), flush=True)
        arch = pg.get_by_text(re.compile("archivés", re.I)).first
        if arch.count():
            arch.scroll_into_view_if_needed()
            s.ecran("10-carnets-archives", [(arch, "Carnets archivés")])
        s.aller(f"/notebooks/{pe}", attendre=bouton(s, "Supprimer"))
        bouton(s, "Supprimer").click(); pg.wait_for_timeout(1200)
        d = pg.get_by_role("alertdialog").last if pg.get_by_role("alertdialog").count() else dialogue(s)
        s.ecran("11-supprimer-carnet", [(d.get_by_text("Supprimer les sources exclusives").first, "Supprimer les sources exclusives"),
                                        (d.get_by_text("Délier et les conserver").first, "Délier et les conserver"),
                                        (d.get_by_role("button", name="Supprimer").last, "Supprimer")])
        d.get_by_text("Supprimer les sources exclusives").first.click(); pg.wait_for_timeout(300)
        d.get_by_role("button", name="Supprimer").last.click(); pg.wait_for_timeout(2500)
        print("supprimé :", carnet("Premier essai") is None, flush=True)


def contexte_chat(s):
    """Ligne « Context: » du bas de la colonne de discussion."""
    return s.pg.get_by_text("Context:").first.locator("xpath=ancestor::div[1]")


def poser(s, question):
    pg = s.pg
    champ = pg.get_by_placeholder(re.compile("Posez n'importe quelle question"))
    champ.fill(question)
    avant = pg.locator("a, button").filter(has_text=re.compile(r"^\s*source(_insight)?:")).count()
    champ.locator("xpath=following::button[1]").click()
    import time
    fin = time.time() + 300
    while time.time() < fin:
        if pg.locator("a, button").filter(has_text=re.compile(r"^\s*source(_insight)?:")).count() > avant:
            break
        pg.wait_for_timeout(2000)
    pg.wait_for_timeout(3000)


def nouvelle_session(s, titre):
    pg = s.pg
    bouton(s, "Sessions").click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    print("sessions :", d.inner_text()[:400].replace("\n", "|"), [b.inner_text() for b in d.get_by_role("button").all()], flush=True)
    return d


# ---------------------------------------------------------------- 06. Discuter
def discuter(s):
    s.chapitre = "06-discuter"; pg = s.pg
    nb = carnet(DEMO)
    s.aller(f"/notebooks/{nb}", attendre=pg.get_by_text("faq-sav.html").first)
    bouton(s, "Écrire une note").locator("xpath=following::button[1]").click(); pg.wait_for_timeout(800)
    bouton(s, "Contexte").click(); pg.wait_for_timeout(600)
    s.ecran("01-menu-contexte", [(pg.get_by_role("menuitem", name="Tout inclure (aperçus uniquement)"), "Tout inclure (aperçus uniquement)"),
                                 (pg.get_by_role("menuitem", name="Tout inclure (contenu complet)"), "Tout inclure (contenu complet)"),
                                 (pg.get_by_role("menuitem", name="Tout exclure du contexte"), "Tout exclure du contexte")])
    pg.get_by_role("menuitem", name="Tout inclure (contenu complet)").click(); pg.wait_for_timeout(2000)
    print("contexte complet :", contexte_chat(s).inner_text().replace("\n", " "), flush=True)
    icone = icone_contexte(s, "procedure-batteries.docx")
    icone.click(); pg.wait_for_timeout(1200); icone.click(); pg.wait_for_timeout(1500)
    print("après deux clics :", contexte_chat(s).inner_text().replace("\n", " "), flush=True)
    icone.hover(); pg.wait_for_timeout(800)
    s.ecran("02-modes-de-contexte", [(icone_contexte(s, "faq-sav.html"), "Contenu complet"), (icone, "Aperçus"),
                                     (contexte_chat(s), "Context")])
    icone.click(); pg.wait_for_timeout(1200)  # revient au premier mode du cycle
    while "procedure" and contexte_chat(s).inner_text().count("8") and False:
        break
    print("retour :", contexte_chat(s).inner_text().replace("\n", " "), flush=True)
    d = nouvelle_session(s, "Découverte")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    poser(s, "Combien de salariés compte Vélanor fin 2025, et où se trouve son siège ?")
    cit = citation(s); bulle = cit.locator("xpath=ancestor::div[contains(@class,'rounded')][1]")
    icones = bulle.locator("xpath=following::button[position()<=2]")
    # éléments tous visibles sans défilement : la zone de discussion défile seule et décalerait les cadres
    rep = bulle.get_by_text(re.compile("412 salariés")).first
    s.ecran("03-reponse-citee", [(rep, "Réponse"), (cit, "Citation"), (icones.nth(0), "Enregistrer en note"), (icones.nth(1), "Copier")])
    bouton(s, "chat", exact=True).click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    s.ecran("04-modele-de-session", [(d.get_by_role("combobox").first, "Modèle"), (d.get_by_role("button", name="Réinitialiser"), "Réinitialiser"),
                                     (d.get_by_role("button", name="Enregistrer les modifications"), "Enregistrer les modifications")])
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    d = nouvelle_session(s, "x")
    b = d.get_by_role("button")
    s.ecran("05-sessions", [(b.nth(0), "Nouvelle session"), (d.get_by_text(re.compile("^Combien de salariés")).first, "Session"),
                            (b.nth(1), "Renommer"), (b.nth(2), "Supprimer")])
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)


def boutons_de(d):
    return [b.inner_text().strip() or (b.get_attribute("aria-label") or "") for b in d.get_by_role("button").all()]


# ---------------------------------------------------------------- 07. Notes et transformations
def notes(s):
    s.chapitre = "07-notes"; pg = s.pg
    nb = carnet(DEMO)
    deja = any(n.get("title") == "Points à vérifier" for n in api(f"/api/notes?notebook_id={nb}"))
    if not deja:
        notes_creation(s, nb)
    transformations_suite(s, nb)


def notes_creation(s, nb):
    pg = s.pg
    s.aller(f"/notebooks/{nb}", attendre=pg.get_by_text("faq-sav.html").first)
    bouton(s, "Écrire une note").click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    print("note :", d.inner_text()[:300].replace("\n", "|"), boutons_de(d), flush=True)
    d.get_by_role("button", name="Note sans titre").click(); pg.wait_for_timeout(500)
    titre = d.locator("input").first; titre.fill("Points à vérifier"); pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
    titre = d.get_by_text("Points à vérifier").first
    zone = d.locator("textarea, [contenteditable=true]").first; zone.click()
    pg.keyboard.type("Comparer le délai de livraison du contrat Batterix au délai constaté dans le classeur des stocks.")
    enreg = d.get_by_role("button").filter(has_text=re.compile("Enregistrer|Créer|Sauvegarder")).last
    s.ecran("01-ecrire-note", [(titre, "Titre"), (zone, "Texte de la note"), (enreg, enreg.inner_text().strip())])
    enreg.click(); pg.wait_for_timeout(2000)
    carte = pg.get_by_text("Points à vérifier").first
    s.ecran("02-note-dans-le-carnet", [(carte, "Carte de la note"), (contexte_chat(s), "Context")])


def transformations_suite(s, nb):
    pg = s.pg
    if any(t["name"] == "fiche-chiffres-fr" for t in api("/api/transformations")):
        return transformations_essai(s, nb)
    s.aller("/transformations", attendre=bouton(s, "Créer une nouvelle"))
    s.ecran("03-transformations", [(pg.get_by_role("tab", name="Transformations"), "Transformations"),
                                   (pg.get_by_role("tab", name="Bac à sable (Playground)"), "Bac à sable (Playground)"),
                                   (pg.get_by_text("Prompt de transformation par défaut").first, "Prompt de transformation par défaut"),
                                   (bouton(s, "Créer une nouvelle"), "Créer une nouvelle"), (pg.get_by_text("Dense Summary", exact=True).first, "Dense Summary")])
    bouton(s, "Créer une nouvelle").click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    print("transformation :", boutons_de(d), [(i.get_attribute("placeholder"), i.get_attribute("name")) for i in d.locator("input, textarea").all()], flush=True)
    champs = d.locator("input")
    champs.nth(0).fill("fiche-chiffres-fr"); champs.nth(1).fill("Chiffres clés")
    prompt = d.locator("textarea, [contenteditable=true], .cm-content").last; prompt.click()
    pg.keyboard.type("Réponds en français. À partir du document, dresse une liste à puces des chiffres clés (au plus 8), "
                     "chacun avec son unité et ce qu'il mesure. N'invente aucun chiffre.")
    creer = d.get_by_role("button", name="Créer une nouvelle").last
    s.ecran("04-nouvelle-transformation", [(champs.nth(0), "Nom"), (champs.nth(1), "Titre"), (prompt, "Prompt Système"), (creer, "Créer une nouvelle")])
    creer.click(); pg.wait_for_timeout(2500)
    if d.is_visible():
        print("toujours ouvert :", d.inner_text()[:300], flush=True); pg.keyboard.press("Escape")
    transformations_essai(s, nb)


def transformations_essai(s, nb):
    pg = s.pg
    s.aller("/transformations", attendre=bouton(s, "Créer une nouvelle"))
    pg.get_by_role("tab", name="Bac à sable (Playground)").click(); pg.wait_for_timeout(1500)
    print("playground :", pg.locator("main").inner_text()[:600].replace("\n", "|"), boutons_de(pg.locator("main")), flush=True)
    listes = pg.locator("main").get_by_role("combobox")
    listes.nth(0).click(); pg.wait_for_timeout(500); pg.get_by_role("option", name=re.compile("Chiffres clés|fiche-chiffres-fr")).first.click(); pg.wait_for_timeout(500)
    choisir_option(s, listes.nth(1), "^chat")
    texte = pg.locator("main textarea").first
    texte.fill(Path("corpus/documents/cse-2025-10-14.md").read_text())
    lancer = bouton(s, "Exécuter la transformation")
    lancer.click()
    pg.wait_for_timeout(5000)
    for _ in range(60):
        if "%" in pg.locator("main").inner_text() or "€" in pg.locator("main").inner_text():
            break
        pg.wait_for_timeout(2000)
    pg.wait_for_timeout(2000)
    s.ecran("05-bac-a-sable", [(listes.nth(0), "Transformation"), (listes.nth(1), "Modèle"), (texte, "Texte d'entrée"), (lancer, "Exécuter la transformation")], plein=True)
    src = next(x["id"] for x in api(f"/api/sources?notebook_id={nb}&limit=100") if x["title"].startswith("rapport-annuel"))
    s.aller(f"/sources/{src}", attendre=pg.get_by_role("tab", name=re.compile("^Analyses")))
    pg.get_by_role("tab", name=re.compile("^Analyses")).click(); pg.wait_for_timeout(1200)
    choix = pg.get_by_role("combobox").first
    if not choix.count():
        choix = bouton(s, "Sélectionner une transformation...")
    choix.click(); pg.wait_for_timeout(500)
    pg.get_by_role("option", name=re.compile("Chiffres clés|fiche-chiffres-fr")).first.click(); pg.wait_for_timeout(500)
    creer = bouton(s, "Créer", exact=True)
    s.ecran("06-appliquer-transformation", [(choix, "Sélectionner une transformation"), (creer, "Créer")])
    creer.click()
    for _ in range(90):
        pg.wait_for_timeout(2000)
        if pg.get_by_text(re.compile("Chiffres clés", re.I)).count() > 1 or pg.get_by_text("48,6").count():
            break
    pg.wait_for_timeout(2000)
    s.ecran("07-analyse-produite", [(pg.get_by_text(re.compile("Chiffres clés", re.I)).last, "Analyse « Chiffres clés »")])


# ---------------------------------------------------------------- 08. Rechercher et demander
def rechercher(s):
    s.chapitre = "08-rechercher"; pg = s.pg
    s.aller("/search", attendre=pg.get_by_role("tab", name="Recherche"))
    pg.get_by_role("tab", name="Recherche").click(); pg.wait_for_timeout(800)
    champ = pg.get_by_placeholder("Entrez votre recherche...").last
    champ.fill("Où ranger les accumulateurs et à quelle température ?"); pg.keyboard.press("Enter"); pg.wait_for_timeout(4000)
    s.ecran("01-recherche-textuelle", [(champ, "Recherche"), (pg.get_by_text("Recherche textuelle", exact=True).first, "Recherche textuelle"),
                                       (pg.get_by_text("Rechercher dans les Sources").first, "Rechercher dans les Sources"),
                                       (pg.get_by_text(re.compile("Aucun résultat")).first, "Aucun résultat")])
    pg.get_by_text("Recherche vectorielle", exact=True).first.click(); pg.wait_for_timeout(500)
    champ.click(); pg.keyboard.press("Enter")
    for _ in range(30):
        pg.wait_for_timeout(1500)
        if pg.get_by_text(re.compile("Correspondances")).count():
            break
    pg.wait_for_timeout(1500)
    print("vectoriel :", pg.locator("main").inner_text()[:800].replace("\n", "|"), flush=True)
    s.ecran("02-recherche-vectorielle", [(pg.get_by_text("Recherche vectorielle", exact=True).first, "Recherche vectorielle"),
                                         (pg.get_by_text(re.compile("Correspondances")).first.locator("xpath=ancestor::div[contains(@class,'rounded') or contains(@class,'border')][1]"), "Premier résultat")])
    pg.get_by_role("tab", name="Demander (bêta)").click(); pg.wait_for_timeout(800)
    q = pg.get_by_placeholder("Entrez votre question...").first
    q.fill("Quel score l'audit du fournisseur Batterix a-t-il obtenu, et quelles non-conformités a-t-il relevées ?")
    dem = bouton(s, "Demander", exact=True)
    s.ecran("03-demander", [(q, "Question"), (pg.get_by_text("Tous les carnets").first, "Carnets"), (pg.get_by_text(re.compile("Stratégie")).first, "Modèles utilisés"), (dem, "Demander")])
    dem.click()
    for _ in range(120):
        pg.wait_for_timeout(2500)
        t = pg.locator("main").inner_text()
        if "87" in t and ("Réponse finale" in t or "Final" in t or len(t) > 1500):
            break
    pg.wait_for_timeout(4000)
    print("demander :", pg.locator("main").inner_text()[-1200:].replace("\n", "|"), flush=True)
    s.ecran("04-reponse-demander", [(pg.get_by_text(re.compile("87")).last, "Réponse")], plein=True)


# ---------------------------------------------------------------- 10. Régler
def regler(s):
    s.chapitre = "10-regler"; pg = s.pg
    s.aller("/settings", attendre=pg.get_by_text("Traitement du contenu").first)
    s.ecran("01-traitement-du-contenu", [(pg.get_by_text("Moteur de traitement de documents").first.locator("xpath=following::*[@role='combobox'][1]"), "Moteur de traitement de documents"),
                                         (pg.get_by_text("Activer l'OCR").first, "Activer l'OCR"), (pg.get_by_text("Extraire les formules").first, "Extraire les formules"),
                                         (pg.get_by_text("Décrire les images et les graphiques").first, "Décrire les images et les graphiques"),
                                         (pg.get_by_text("Moteur de traitement d'URL").first.locator("xpath=following::*[@role='combobox'][1]"), "Moteur de traitement d'URL")])
    ind = pg.get_by_text("Option d'indexation par défaut").first; ind.scroll_into_view_if_needed()
    s.ecran("02-indexation-et-fichiers", [(ind.locator("xpath=following::*[@role='combobox'][1]"), "Option d'indexation par défaut"),
                                          (pg.get_by_text("Suppression automatique des fichiers").first.locator("xpath=following::*[@role='combobox'][1]"), "Suppression automatique des fichiers"),
                                          (bouton(s, "Enregistrer"), "Enregistrer")])
    s.aller("/advanced", attendre=pg.get_by_text("Infos Système").first)
    lancer = bouton(s, "Lancer la reconstruction")
    s.ecran("03-avance", [(pg.get_by_text("Infos Système").first.locator("xpath=ancestor::div[1]"), "Infos Système"),
                          (pg.get_by_text("Mode de reconstruction").first.locator("xpath=following::*[@role='combobox'][1]"), "Mode de reconstruction"),
                          (pg.get_by_text("Inclure dans la reconstruction").first, "Inclure dans la reconstruction"), (lancer, "Lancer la reconstruction")])
    lancer.click(); pg.wait_for_timeout(3000)
    for r in ("alertdialog", "dialog"):
        if pg.get_by_role(r).count():
            print("reconstruction :", pg.get_by_role(r).last.inner_text()[:300], flush=True)
            pg.get_by_role(r).last.get_by_role("button").last.click(); pg.wait_for_timeout(2000)
    for _ in range(90):
        t = pg.locator("main").inner_text()
        if re.search("terminé|Terminé|complété|Complete|succès", t):
            break
        pg.wait_for_timeout(2000)
    print("état reconstruction :", pg.locator("main").inner_text()[-600:].replace("\n", "|"), flush=True)
    s.ecran("04-reconstruction", [(pg.get_by_text(re.compile("terminé|Terminé|complété|Complete|succès|cours")).last, "État de la reconstruction")], plein=True)


def champ(d, libelle, n=0):
    """Champ d'une fenêtre repéré par son libellé (texte du label, puis premier champ qui le suit)."""
    l = d.get_by_label(re.compile("^" + re.escape(libelle)))
    if l.count():
        return l.nth(n)
    return d.get_by_text(re.compile("^" + re.escape(libelle))).nth(n).locator("xpath=following::*[self::input or self::textarea or @role='combobox'][1]")


def choisir_option(s, liste, motif):
    liste.click(); s.pg.wait_for_timeout(600)
    opts = s.pg.get_by_role("option")
    print("  options :", [o.inner_text().replace("\n", " ") for o in opts.all()][:12], flush=True)
    opts.filter(has_text=re.compile(motif)).first.click(); s.pg.wait_for_timeout(500)


# ---------------------------------------------------------------- 09. Podcast
def podcast(s):
    s.chapitre = "09-podcast"; pg = s.pg
    for e in api("/api/episode-profiles"):
        if e["name"] == "court-fr":
            api(f"/api/episode-profiles/{e['id']}", "DELETE")
    for e in api("/api/speaker-profiles"):
        if e["name"] == "duo-fr":
            api(f"/api/speaker-profiles/{e['id']}", "DELETE")
    s.aller("/podcasts", attendre=pg.get_by_role("tab", name="Profils"))
    s.ecran("01-episodes-vide", [(pg.get_by_role("tab", name="Épisodes"), "Épisodes"), (pg.get_by_role("tab", name="Profils"), "Profils"),
                                 (bouton(s, "Générer un podcast"), "Générer un podcast"), (bouton(s, "Rafraîchir"), "Rafraîchir")])
    pg.get_by_role("tab", name="Profils").click(); pg.wait_for_timeout(1200)
    bouton(s, "Créer un intervenant").click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    champ(d, "Nom du profil").fill("duo-fr")
    champ(d, "Description").fill("Deux voix : une animatrice française et un analyste")
    d.get_by_role("button", name="Ajouter un intervenant").click(); pg.wait_for_timeout(600)
    voix = [("Camille", "ff_siwis", "Animatrice d'une émission d'entreprise, curieuse et claire.", "Pose des questions simples et reformule."),
            ("Hugo", "am_michael", "Analyste financier de l'entreprise.", "Précis, cite les chiffres.")]
    for i, (nom, vid, histoire, perso) in enumerate(voix):
        champ(d, "Nom", i + 1 if d.get_by_label(re.compile("^Nom du profil")).count() == 0 else i).fill(nom) if False else None
    noms = d.get_by_label(re.compile("^Nom( \\*)?$"))
    print("champs Nom :", noms.count(), [i.get_attribute("placeholder") for i in d.locator("input, textarea").all()], flush=True)
    for i, (nom, vid, histoire, perso) in enumerate(voix):
        d.get_by_label(re.compile("^Nom( \\*)?$")).nth(i).fill(nom)
        d.get_by_label(re.compile("^ID de la voix")).nth(i).fill(vid)
        d.get_by_label(re.compile("^Histoire")).nth(i).fill(histoire)
        d.get_by_label(re.compile("^Personnalité")).nth(i).fill(perso)
    vm = d.get_by_role("combobox").first
    if "Kokoro" not in (vm.inner_text() or ""):
        choisir_option(s, vm, "Kokoro")
    creer = d.get_by_role("button", name="Créer un profil")
    d.get_by_label(re.compile("^ID de la voix")).nth(0).scroll_into_view_if_needed()
    s.ecran("02-profil-intervenants", [(vm, "Modèle vocal"), (champ(d, "Nom du profil"), "Nom du profil"), (d.get_by_label(re.compile("^Nom( \\*)?$")).nth(0), "Nom"),
                                       (d.get_by_label(re.compile("^ID de la voix")).nth(0), "ID de la voix"), (creer, "Créer un profil")])
    creer.click(); pg.wait_for_timeout(2000)
    if d.is_visible():
        print("intervenant encore ouvert :", d.inner_text()[-400:], flush=True); pg.keyboard.press("Escape")
    bouton(s, "Créer un profil").click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    print("profil épisode :", d.inner_text()[:1500].replace("\n", "|"), flush=True)
    champ(d, "Nom du profil").fill("court-fr")
    seg = champ(d, "Segments"); seg.fill("3")
    champ(d, "Description").fill("Épisode court et factuel, en français")
    listes = d.get_by_role("combobox")
    print("listes épisode :", [l.inner_text().replace("\n", " ") for l in listes.all()], flush=True)
    choisir_option(s, listes.nth(0), "duo-fr")
    for i in range(1, listes.count()):
        t = listes.nth(i).inner_text()
        if not t.strip() or "Sélectionn" in t:
            try:
                choisir_option(s, listes.nth(i), r"^chat|\(fr-FR\)")
            except Exception as e:
                print("  liste", i, "non remplie :", str(e)[:100], flush=True); pg.keyboard.press("Escape")
    brief = d.locator("textarea").last
    brief.fill("Épisode court et factuel, en français, qui présente les informations principales des sources.")
    creer = d.get_by_role("button", name=re.compile("^Créer")).last
    s.ecran("03-profil-episode", [(champ(d, "Nom du profil"), "Nom du profil"), (seg, "Segments"), (listes.nth(0), "Profil de l'intervenant"), (brief, "Briefing"), (creer, creer.inner_text().strip())])
    creer.click(); pg.wait_for_timeout(2000)
    if d.is_visible():
        print("épisode encore ouvert :", d.inner_text()[-500:], flush=True); pg.keyboard.press("Escape")
    pg.get_by_role("tab", name="Épisodes").click(); pg.wait_for_timeout(800)
    bouton(s, "Générer un podcast").click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(1500)
    print("générer :", d.inner_text()[:800].replace("\n", "|"), flush=True)
    cases = d.get_by_role("checkbox")
    print("cases :", cases.count(), flush=True)
    cases.first.click(); pg.wait_for_timeout(800)  # case du carnet « Démo Vélanor » : toutes ses sources et notes
    print("sélection :", d.get_by_text(re.compile("éléments sélectionnés")).first.inner_text(), flush=True)
    profil = d.get_by_text(re.compile("^Profil de l'épisode")).first.locator("xpath=following::*[@role='combobox'][1]")
    choisir_option(s, profil, "court-fr")
    nom = champ(d, "Nom de l'épisode"); nom.fill("Vélanor en bref")
    gen = d.get_by_role("button", name="Générer")
    s.ecran("04-generer", [(cases.first, "Démo Vélanor"), (profil, "Profil de l'épisode"), (nom, "Nom de l'épisode"), (gen, "Générer")])
    print("contenu choisi :", d.inner_text()[:600].replace("\n", "|"), flush=True)
    gen.click(); pg.wait_for_timeout(4000)
    s.ecran("05-episode-en-cours", [(pg.get_by_text("Vélanor en bref").first, "Épisode en cours")])
    import time
    fin = time.time() + 1800
    while time.time() < fin:
        eps = [e for e in api("/api/podcasts/episodes") if e.get("name") == "Vélanor en bref"]
        if eps and eps[0].get("job_status") in ("completed", "failed", "error"):
            print("épisode :", {k: eps[0].get(k) for k in ("job_status", "error_message", "audio_file")}, flush=True); break
        time.sleep(15)
    s.aller("/podcasts", attendre=pg.get_by_text("Vélanor en bref").first)
    s.ecran("06-episode-pret", [(pg.get_by_text("Vélanor en bref").first.locator("xpath=ancestor::div[contains(@class,'rounded')][1]"), "Épisode"),
                                (pg.locator("audio").first if pg.locator("audio").count() else pg.get_by_text("Vélanor en bref").first, "Lecteur audio")], plein=True)


# ---------------------------------------------------------------- 12. En cas de problème
def problemes(s):
    s.chapitre = "12-problemes"; pg = s.pg
    # 1. mot de passe refusé (navigateur sans session)
    ctx = s.b.new_context(viewport={"width": 1440, "height": 900}, locale="fr-FR"); p2 = ctx.new_page()
    from commun_on import URL
    p2.goto(URL + "/login"); p2.wait_for_load_state("load"); p2.wait_for_timeout(1500)
    p2.locator("input[type=password]").fill("mauvais-mot-de-passe"); p2.keyboard.press("Enter"); p2.wait_for_timeout(2500)
    print("connexion refusée :", p2.locator("body").inner_text()[:300].replace("\n", "|"), flush=True)
    from annoter import capture
    from commun_on import IMG, TXT
    err = p2.get_by_text(re.compile("incorrect|invalide|Invalid|échec|Échec|erreur", re.I)).first
    capture(p2, IMG / s.chapitre / "01-mot-de-passe-refuse.png", [(p2.locator("input[type=password]"), "Mot de passe"), (err, "Message d'erreur")],
            masques=[], texte=TXT / s.chapitre / "01-mot-de-passe-refuse.txt")
    ctx.close()
    # 2. test de connexion en échec : configuration volontairement fausse, supprimée ensuite
    s.aller("/settings/models", attendre=pg.get_by_text("Attributions des modèles par défaut").first)
    titre = pg.get_by_text("OpenAI Compatible", exact=True).first
    ajout = titre.locator("xpath=ancestor::div[.//button[contains(., 'Ajouter une configuration')]][1]").get_by_role("button", name="Ajouter une configuration").last
    ajout.scroll_into_view_if_needed(); ajout.click()
    d = dialogue(s); d.wait_for(state="visible"); ch = d.locator("input")
    ch.nth(0).fill("essai-erreur"); ch.nth(1).fill("cle-fausse"); ch.nth(2).fill("http://llm-central:9999/v1")
    d.get_by_role("button", name="Ajouter une configuration").click(); pg.wait_for_timeout(2500)
    carte = pg.get_by_text("essai-erreur", exact=True).first.locator("xpath=ancestor::div[.//button[normalize-space()='Test']][1]")
    carte.scroll_into_view_if_needed(); carte.get_by_role("button", name="Test").click()
    t = toast(s); t.wait_for(state="visible", timeout=60000); pg.wait_for_timeout(1500)
    print("test en échec :", t.inner_text(), flush=True)
    s.ecran("02-test-en-echec", [(pg.get_by_text("essai-erreur", exact=True).first, "essai-erreur"), (t, "Message d'échec")])
    carte.get_by_role("button", name="Supprimer").first.click(); pg.wait_for_timeout(1000)
    for r in ("alertdialog", "dialog"):
        if pg.get_by_role(r).count():
            pg.get_by_role(r).last.get_by_role("button").filter(has_text=re.compile("Supprimer|Confirmer|Delete")).last.click(); pg.wait_for_timeout(1500); break
    print("configurations :", [c["name"] for c in api("/api/credentials")], flush=True)
    # 3. dépassement du contexte de 16 384 jetons : un texte d'environ 80 000 caractères, en contenu complet
    ancien = carnet("Essai contexte")
    if ancien:
        api(f"/api/notebooks/{ancien}?delete_exclusive_sources=true", "DELETE")
    s.aller("/notebooks", attendre=bouton(s, "Nouveau Carnet"))
    nb = creer_carnet(s, "Essai contexte", "Dépassement volontaire du contexte, supprimé après l'essai")
    base = Path("corpus/documents/cse-2025-10-14.md").read_text() + "\n" + Path("corpus/documents/faq-sav.html").read_text()
    texte = "".join(f"\n\n### Copie {i}\n\n{base}" for i in range(1, 60))[:80000]
    pg.locator("button:has-text('Ajouter la source')").first.click(); pg.get_by_role("menuitem", name="Ajouter la source").click()
    d = dialogue(s); d.wait_for(state="visible"); d.get_by_role("tab", name="Saisir du texte").click(); pg.wait_for_timeout(500)
    d.locator("textarea").first.fill(texte); d.get_by_placeholder("Donnez un titre descriptif à votre source").fill("Texte trop long")
    d.get_by_role("button", name="Suivant").click(); pg.wait_for_timeout(600); d.get_by_role("button", name="Suivant").click(); pg.wait_for_timeout(600)
    for c in d.get_by_role("checkbox").all():  # ni résumé ni indexation : seule la conversation compte ici
        if c.get_attribute("aria-checked") == "true" or c.get_attribute("data-state") == "checked":
            c.click()
    d.get_by_role("button", name="Terminé").click(); pg.wait_for_timeout(3000)
    print("source longue :", attendre_sources(nb, 1, 300), flush=True)
    s.aller(f"/notebooks/{nb}", attendre=pg.get_by_text("Texte trop long").first)
    print("boutons Contexte :", [b.inner_text() for b in pg.get_by_role("button", name=re.compile("^Contexte")).all()], flush=True)
    for _ in range(3):  # icône de la carte jusqu'au contenu complet (le compteur dépasse alors 10 000 jetons)
        if re.search(r"\d+(\.\d)?K tokens", contexte_chat(s).locator("xpath=..").inner_text()) and "K chars" in contexte_chat(s).locator("xpath=..").inner_text() \
                and float(re.search(r"([\d.]+)K tokens", contexte_chat(s).locator("xpath=..").inner_text()).group(1)) > 10:
            break
        icone_contexte(s, "Texte trop long").click(); pg.wait_for_timeout(1500)
    print("contexte long :", contexte_chat(s).inner_text().replace("\n", " "), flush=True)
    champ_q = pg.get_by_placeholder(re.compile("Posez n'importe quelle question")); champ_q.fill("Quel est le dernier numéro de copie ?")
    champ_q.locator("xpath=following::button[1]").click()
    for _ in range(60):
        pg.wait_for_timeout(2000)
        if pg.locator("[data-sonner-toast]").count() or pg.get_by_text(re.compile("error|erreur|exceeds|dépasse", re.I)).count():
            break
    pg.wait_for_timeout(1500)
    msgs = [t.inner_text().replace("\n", " ") for t in pg.locator("[data-sonner-toast]").all()]
    print("dépassement :", msgs, pg.locator("main").inner_text()[-500:].replace("\n", "|"), flush=True)
    err = pg.locator("[data-sonner-toast]").first if pg.locator("[data-sonner-toast]").count() else pg.get_by_text(re.compile("error|erreur|exceeds", re.I)).last
    s.ecran("03-contexte-depasse", [(contexte_chat(s), "Context"), (err, "Message d'erreur")])
    api(f"/api/notebooks/{nb}?delete_exclusive_sources=true", "DELETE")
    # 4. bandeau des podcasts
    s.aller("/podcasts", attendre=bouton(s, "Générer un podcast"))
    ban = pg.get_by_text(re.compile("Configuration requise|requise", re.I)).first
    if ban.count():
        s.ecran("04-podcast-configuration-requise", [(ban, "Configuration requise")])


def creer_session(s, titre, capture=None):
    """Fenêtre « Sessions » : bouton de création (icône sans libellé), titre, validation."""
    pg = s.pg
    bouton(s, "Sessions").click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    nouveau = [b for b in d.get_by_role("button").all() if not b.inner_text().strip() and (b.get_attribute("aria-label") or "") != "Close"][0]
    nouveau.click(); pg.wait_for_timeout(1200)
    print("après création :", d.inner_text()[:300].replace("\n", "|"), [i.get_attribute("placeholder") for i in d.locator("input").all()], flush=True)
    if d.locator("input").count():
        champ_t = d.locator("input").first; champ_t.fill(titre)
        if capture:
            s.ecran(capture, [(nouveau, "Nouvelle session"), (champ_t, "Titre de la session")])
        pg.keyboard.press("Enter"); pg.wait_for_timeout(1500)
    if d.is_visible():
        pg.keyboard.press("Escape"); pg.wait_for_timeout(500)


RECETTES = [
    ("Recette 1 - rapport annuel", ["Quel est le chiffre d'affaires 2025 et quel trimestre a été le plus élevé ?",
                                    "Quel modèle est le plus vendu et quel est le plus cher ?"]),
    ("Recette 2 - contrat et audit", ["Le délai de livraison réellement constaté chez Batterix respecte-t-il le délai prévu par le contrat ?",
                                      "Quelles non-conformités l'audit de Batterix a-t-il relevées ?"]),
    ("Recette 3 - synthèse direction", ["Rédige une synthèse en cinq puces pour la direction : chiffre d'affaires 2025, objectif 2026, "
                                        "nouvelle usine, risque fournisseur batteries, arrêt de la ligne 3. Cite les sources."]),
]


# ---------------------------------------------------------------- 11. Cas pratiques
def cas_pratiques(s):
    s.chapitre = "11-cas-pratiques"; pg = s.pg
    nb = carnet(DEMO)
    for sess in api(f"/api/chat/sessions?notebook_id={nb}"):
        if sess.get("title", "").startswith("Recette"):
            api(f"/api/chat/sessions/{sess['id']}", "DELETE")
    s.aller(f"/notebooks/{nb}", attendre=pg.get_by_text("faq-sav.html").first)
    bouton(s, "Écrire une note").locator("xpath=following::button[1]").click(); pg.wait_for_timeout(800)
    print("contexte à l'ouverture :", contexte_chat(s).locator("xpath=..").inner_text().replace("\n", " "), flush=True)
    bouton(s, "Contexte").click(); pg.get_by_role("menuitem", name="Tout inclure (contenu complet)").click(); pg.wait_for_timeout(2000)
    print("contexte complet :", contexte_chat(s).locator("xpath=..").inner_text().replace("\n", " "), flush=True)
    import time
    for i, (titre, questions) in enumerate(RECETTES, 1):
        creer_session(s, titre, capture="01-nouvelle-session" if i == 1 else None)
        for q in questions:
            t0 = time.time(); poser(s, q); print(f"{titre} | {q[:50]} | {time.time() - t0:.1f} s", flush=True)
        cit = citation(s); bulle = cit.locator("xpath=ancestor::div[contains(@class,'rounded')][1]")
        print("réponse :", bulle.inner_text()[:700].replace("\n", " "), flush=True)
        icones = bulle.locator("xpath=following::button[position()<=2]")
        if i == 3:
            s.ecran(f"0{i + 1}-recette-{i}", [(bulle, "Réponse"), (cit, "Citation"), (icones.nth(0), "Enregistrer en note")])
            icones.nth(0).click(); pg.wait_for_timeout(2500)
        else:
            s.ecran(f"0{i + 1}-recette-{i}", [(bulle, "Réponse"), (cit, "Citation")])
    bouton(s, "Sessions").click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    s.ecran("05-trois-sessions", [(d.get_by_text(re.compile("^Recette 1")).first, "Recette 1"), (d.get_by_text(re.compile("^Recette 2")).first, "Recette 2"),
                                  (d.get_by_text(re.compile("^Recette 3")).first, "Recette 3")])
    pg.keyboard.press("Escape")


def podcast_fin(s):
    """Suite du chapitre 09 : attend la fin de l'épisode, puis le montre dans la page Podcasts."""
    s.chapitre = "09-podcast"; pg = s.pg
    import time
    t0, fin = time.time(), time.time() + 2400
    while time.time() < fin:
        eps = [e for e in api("/api/podcasts/episodes") if e.get("name") == "Vélanor en bref"]
        if eps and eps[0].get("job_status") in ("completed", "failed", "error"):
            break
        time.sleep(15)
    print("épisode :", {k: str(eps[0].get(k))[:200] for k in ("job_status", "error_message", "audio_file", "created")}, f"attente {time.time() - t0:.0f} s", flush=True)
    s.aller("/podcasts", attendre=bouton(s, "Rafraîchir"))
    bouton(s, "Rafraîchir").click(); pg.wait_for_timeout(2500)
    titre = pg.get_by_text("Vélanor en bref").first
    titre.wait_for(state="visible", timeout=30000)
    print("page :", pg.locator("main").inner_text()[:800].replace("\n", "|"), flush=True)
    carte = titre.locator("xpath=ancestor::div[.//audio or .//button][1]")
    elems = [(titre, "Vélanor en bref")]
    if pg.locator("audio").count():
        elems.append((pg.locator("audio").first, "Lecteur audio"))
    s.ecran("05-episode-pret", elems)


def retouches(s):
    """Captures refaites après la relecture novice : fenêtres hautes affichées en entier (fenêtre du navigateur portée à
    1440 × 1300 pour ces trois fenêtres, sinon leur haut sort de l'écran) ; icône « Contexte » annotée. Rien n'est créé :
    chaque fenêtre est remplie puis fermée par « Annuler » ou Échap."""
    pg = s.pg
    nb = carnet(DEMO)
    s.chapitre = "06-discuter"
    s.aller(f"/notebooks/{nb}", attendre=pg.get_by_text("faq-sav.html").first)
    bouton(s, "Écrire une note").locator("xpath=following::button[1]").click(); pg.wait_for_timeout(800)
    print("boutons Contexte :", pg.get_by_role("button", name="Contexte").count(), flush=True)
    # le menu ouvert masque le bouton aux outils d'accessibilité : repère posé avant l'ouverture
    bouton(s, "Contexte").evaluate("e => e.setAttribute('data-rag-repere', 'contexte')")
    ctx = pg.locator("[data-rag-repere=contexte]"); ctx.click(); pg.wait_for_timeout(600)
    s.ecran("01-menu-contexte", [(ctx, "Contexte"), (pg.get_by_role("menuitem", name="Tout inclure (aperçus uniquement)"), "Tout inclure (aperçus uniquement)"),
                                 (pg.get_by_role("menuitem", name="Tout inclure (contenu complet)"), "Tout inclure (contenu complet)"),
                                 (pg.get_by_role("menuitem", name="Tout exclure du contexte"), "Tout exclure du contexte")])
    pg.keyboard.press("Escape")
    pg.set_viewport_size({"width": 1440, "height": 1300})
    s.chapitre = "07-notes"
    s.aller("/transformations", attendre=bouton(s, "Créer une nouvelle"))
    bouton(s, "Créer une nouvelle").click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    ch = d.locator("input"); ch.nth(0).fill("fiche-chiffres-fr"); ch.nth(1).fill("Chiffres clés")
    prompt = d.locator("textarea, [contenteditable=true], .cm-content").last; prompt.click()
    pg.keyboard.type("Réponds en français. À partir du document, dresse une liste à puces des chiffres clés (au plus 8), "
                     "chacun avec son unité et ce qu'il mesure. N'invente aucun chiffre.")
    ch.nth(0).scroll_into_view_if_needed(); pg.wait_for_timeout(300)
    s.ecran("04-nouvelle-transformation", [(ch.nth(0), "Nom"), (ch.nth(1), "Titre"), (prompt, "Prompt Système"),
                                           (d.get_by_role("button", name="Créer une nouvelle").last, "Créer une nouvelle")])
    d.get_by_role("button", name="Annuler").click(); pg.wait_for_timeout(500)
    s.chapitre = "09-podcast"
    s.aller("/podcasts", attendre=pg.get_by_role("tab", name="Profils"))
    pg.get_by_role("tab", name="Profils").click(); pg.wait_for_timeout(1000)
    bouton(s, "Créer un intervenant").click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    vm = d.get_by_role("combobox").first
    if "Kokoro" not in (vm.inner_text() or ""):
        choisir_option(s, vm, "Kokoro")
    d.get_by_placeholder("ex: Discussion tech").fill("duo-fr")
    d.get_by_placeholder("Hôte 1").fill("Camille"); d.get_by_placeholder("voice_123").first.fill("ff_siwis")
    d.get_by_placeholder(re.compile("Courte biographie")).first.fill("Animatrice d'une émission d'entreprise, curieuse et claire.")
    d.get_by_placeholder(re.compile("Décrivez le style")).first.fill("Pose des questions simples et reformule.")
    d.get_by_placeholder("ex: Discussion tech").scroll_into_view_if_needed(); pg.wait_for_timeout(300)
    s.ecran("02-profil-intervenants", [(vm, "Modèle vocal"), (d.get_by_placeholder("ex: Discussion tech"), "Nom du profil"),
                                       (d.get_by_placeholder("Hôte 1"), "Nom"), (d.get_by_placeholder("voice_123").first, "ID de la voix"),
                                       (d.get_by_placeholder(re.compile("Courte biographie")).first, "Histoire (Backstory)"),
                                       (d.get_by_placeholder(re.compile("Décrivez le style")).first, "Personnalité")])
    pg.keyboard.press("Escape"); pg.wait_for_timeout(600)
    bouton(s, "Créer un profil").click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    nom = champ(d, "Nom du profil"); nom.fill("court-fr"); seg = champ(d, "Segments"); seg.fill("3")
    listes = d.get_by_role("combobox")
    nom.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
    print("listes profil épisode :", [l.inner_text().replace("\n", " ") for l in listes.all()], flush=True)
    s.ecran("03-profil-episode", [(nom, "Nom du profil"), (seg, "Segments"), (listes.nth(0), "Profil de l'intervenant"),
                                  (listes.nth(1), "Modèle de plan"), (listes.nth(2), "Modèle de transcription"), (listes.nth(3), "Langue")])
    pg.keyboard.press("Escape")


def retouches2(s):
    """Captures reprises après la seconde relecture novice : les trois modes de contexte côte à côte, citation d'une réponse,
    onglet « Profils » sans fenêtre, profil d'épisode rempli (fenêtre fermée par Échap, rien n'est créé)."""
    pg = s.pg
    nb = carnet(DEMO)
    s.chapitre = "06-discuter"
    s.aller(f"/notebooks/{nb}", attendre=pg.get_by_text("faq-sav.html").first)
    bouton(s, "Écrire une note").locator("xpath=following::button[1]").click(); pg.wait_for_timeout(800)
    bouton(s, "Contexte").click(); pg.get_by_role("menuitem", name="Tout inclure (contenu complet)").click(); pg.wait_for_timeout(1500)
    exclu = icone_contexte(s, "procedure-batteries.docx"); exclu.click(); pg.wait_for_timeout(1200)
    apercu = icone_contexte(s, "message-vocal-production.mp3"); apercu.click(); pg.wait_for_timeout(1000); apercu.click(); pg.wait_for_timeout(1200)
    print("contexte trois modes :", contexte_chat(s).locator("xpath=..").inner_text().replace("\n", " "), flush=True)
    s.ecran("02-modes-de-contexte", [(icone_contexte(s, "faq-sav.html"), "Contenu complet"), (exclu, "Exclue"), (apercu, "Aperçus"),
                                     (contexte_chat(s), "Context")])
    bouton(s, "Contexte").click(); pg.get_by_role("menuitem", name="Tout inclure (contenu complet)").click(); pg.wait_for_timeout(1500)
    bouton(s, "Sessions").click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    d.get_by_text(re.compile("^Combien de salariés")).first.click(); pg.wait_for_timeout(2500)
    if dialogue(s).count() and dialogue(s).is_visible():
        pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    cit = pg.get_by_text(re.compile(r"^source:[a-z0-9]+$")).last
    cit.scroll_into_view_if_needed(); pg.wait_for_timeout(500)
    bulle = cit.locator("xpath=ancestor::div[contains(@class,'rounded')][1]")
    icones = bulle.locator("xpath=following::button[position()<=2]")
    # éléments tous visibles sans défilement : la zone de discussion défile seule et décalerait les cadres
    rep = bulle.get_by_text(re.compile("412 salariés")).first
    s.ecran("03-reponse-citee", [(rep, "Réponse"), (cit, "Citation"), (icones.nth(0), "Enregistrer en note"), (icones.nth(1), "Copier")])
    s.chapitre = "09-podcast"
    s.aller("/podcasts", attendre=pg.get_by_role("tab", name="Profils"))
    pg.get_by_role("tab", name="Profils").click(); pg.wait_for_timeout(1200)
    s.ecran("01b-onglet-profils", [(bouton(s, "Créer un intervenant"), "Créer un intervenant"), (bouton(s, "Créer un profil"), "Créer un profil")])
    pg.set_viewport_size({"width": 1440, "height": 1300})
    bouton(s, "Créer un profil").click(); d = dialogue(s); d.wait_for(state="visible"); pg.wait_for_timeout(800)
    nom = champ(d, "Nom du profil"); nom.fill("court-fr"); seg = champ(d, "Segments"); seg.fill("3")
    listes = d.get_by_role("combobox")
    choisir_option(s, listes.nth(0), "^duo-fr"); choisir_option(s, listes.nth(1), "^chat"); choisir_option(s, listes.nth(2), "^chat")
    choisir_option(s, listes.nth(3), r"\(fr-FR\)")
    nom.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
    s.ecran("03-profil-episode", [(nom, "Nom du profil"), (seg, "Segments"), (listes.nth(0), "Profil de l'intervenant"),
                                  (listes.nth(1), "Modèle de plan"), (listes.nth(2), "Modèle de transcription"), (listes.nth(3), "Langue")])
    pg.keyboard.press("Escape")


SCENARIOS = {"retouches2": retouches2, "retouches": retouches, "09b": podcast_fin, "11": cas_pratiques, "12": problemes, "09": podcast, "07": notes, "08": rechercher, "10": regler, "06": discuter, "02": installer, "03": premiers_pas, "04": premiere_question, "05": sources, "05b": sources_suite}

if __name__ == "__main__":
    with sync_playwright() as p:
        for nom in sys.argv[1:]:
            s = Session(p)
            try:
                if nom != "02":
                    s.connexion()
                SCENARIOS[nom](s)
            except Exception:
                import traceback; traceback.print_exc(); print(f"ÉCHEC du scénario {nom}", flush=True)
            finally:
                s.fermer()
