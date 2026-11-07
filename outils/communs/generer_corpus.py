#!/usr/bin/env python3
"""Génère le corpus fictif (entreprise Vélanor) et corpus/MANIFEST.json (SHA-256).

Graine fixe, sortie reproductible au contenu près (les PDF embarquent une date fixe).
Usage : .venv/bin/python outils/communs/generer_corpus.py
"""
import hashlib, json, random
from pathlib import Path

from docx import Document
from openpyxl import Workbook
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pptx import Presentation
from pptx.util import Pt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

GRAINE = 20251108
DATE_PDF = __import__("time").strptime("2025-11-08", "%Y-%m-%d")
RACINE = Path(__file__).resolve().parents[2]
CORPUS = RACINE / "corpus"
DOCS = CORPUS / "documents"
POLICE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
POLICE_GRAS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

pdfmetrics.registerFont(TTFont("DejaVu", POLICE))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", POLICE_GRAS))
STY = getSampleStyleSheet()
for s in STY.byName.values():
    s.fontName = "DejaVu-Bold" if s.name.startswith(("Heading", "Title")) else "DejaVu"


def table(lignes, larg=None):
    t = Table(lignes, colWidths=larg)
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "DejaVu"), ("FONTNAME", (0, 0), (-1, 0), "DejaVu-Bold"),
                           ("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey)]))
    return t


def p(txt, style="BodyText"):
    return Paragraph(txt, STY[style])


def pdf(chemin, pages, titre):
    doc = SimpleDocTemplate(str(chemin), pagesize=A4, title=titre, author="Vélanor SAS (fictif)",
                            creator="generer_corpus.py", invariant=1)
    flux = []
    for i, page in enumerate(pages):
        flux += page
        if i < len(pages) - 1:
            flux.append(PageBreak())
    doc.build(flux, onLaterPages=pied, onFirstPage=pied)


def pied(canvas, doc):
    canvas.setFont("DejaVu", 8)
    canvas.drawString(40, 25, f"Vélanor SAS — document fictif — page {doc.page}")


def rapport_annuel():
    pages = [
        [p("Vélanor SAS — Rapport annuel 2025", "Title"), Spacer(1, 20),
         p("Document fictif généré pour des essais. Toute ressemblance serait fortuite."),
         p("Sommaire : 1. Mot de la présidente — 2. Chiffres clés — 3. Chiffre d'affaires trimestriel — "
           "4. Production par modèle — 5. Effectifs — 6. Environnement — 7. Fournisseurs — 8. Risques — 9. Perspectives 2026.")],
        [p("1. Mot de la présidente", "Heading1"),
         p("Fondée en 2014 à Nantes, Vélanor conçoit et assemble des vélos à assistance électrique. Son siège est situé "
           "au 12 quai de la Fosse, à Nantes. La présidente, Hélène Marchais, dirige l'entreprise depuis 2019."),
         p("L'année 2025 a été marquée par une croissance soutenue malgré les tensions sur les cellules de batterie. "
           "L'entreprise a franchi pour la première fois le seuil de 60 000 vélos produits dans l'année.")],
        [p("2. Chiffres clés 2025", "Heading1"),
         table([["Indicateur", "2025", "Évolution"],
                ["Chiffre d'affaires", "48,6 M€", "+12,4 %"],
                ["Résultat net", "3,1 M€", "+0,6 M€"],
                ["Vélos produits", "61 800", "+9 %"],
                ["Effectif au 31/12/2025", "412 salariés", "+38"],
                ["Part de l'export", "27 %", "+4 points"]], [180, 120, 100]),
         Spacer(1, 12), p("Le taux de retour sous garantie s'établit à 1,8 % des vélos vendus.")],
        [p("3. Chiffre d'affaires trimestriel", "Heading1"),
         table([["Trimestre", "Chiffre d'affaires (M€)", "Part du total"],
                ["T1 2025", "9,8", "20 %"], ["T2 2025", "13,7", "28 %"],
                ["T3 2025", "14,2", "29 %"], ["T4 2025", "10,9", "22 %"], ["Total", "48,6", "100 %"]], [120, 160, 100]),
         Spacer(1, 12), p("Le troisième trimestre est le plus élevé de l'année, porté par la saison estivale.")],
        [p("4. Production par modèle", "Heading1"),
         table([["Modèle", "Usage", "Unités produites", "Prix public TTC"],
                ["Loire Urban", "ville", "24 300", "1 890 €"], ["Sèvre Trail", "VTT", "15 400", "3 150 €"],
                ["Brière Kid", "enfant", "13 200", "990 €"], ["Erdre Cargo", "cargo", "8 900", "4 290 €"],
                ["Total", "", "61 800", ""]], [110, 80, 110, 110]),
         Spacer(1, 12), p("Le modèle cargo Erdre Cargo est le plus cher de la gamme ; le Loire Urban est le plus vendu.")],
        [p("5. Effectifs par site", "Heading1"),
         table([["Site", "Activité", "Salariés au 31/12/2025"],
                ["Nantes", "siège et assemblage", "268"], ["Cholet", "fabrication des cadres", "97"],
                ["Lyon", "agence commerciale", "31"], ["Bruxelles", "filiale Benelux", "16"], ["Total", "", "412"]], [100, 170, 140]),
         Spacer(1, 12), p("L'âge moyen des salariés est de 36 ans. 41 % des postes d'encadrement sont occupés par des femmes.")],
        [p("6. Environnement", "Heading1"),
         p("Les cadres sont fabriqués à partir d'aluminium recyclé à 82 %. La consommation électrique des sites a atteint "
           "3,4 GWh en 2025. Vélanor vise la neutralité carbone de ses sites en 2030."),
         p("Le taux de recyclage des batteries usagées collectées atteint 96 %, grâce au partenariat avec la filière "
           "de collecte Recylo.")],
        [p("7. Fournisseurs principaux", "Heading1"),
         table([["Composant", "Fournisseur", "Pays"],
                ["Batteries", "Batterix GmbH", "Allemagne (Brême)"], ["Moteurs", "Motodrive Co.", "Taïwan"],
                ["Freins", "Stopline", "Italie"], ["Pneus", "Gomma Ouest", "France"]], [120, 140, 150]),
         Spacer(1, 12), p("Le contrat d'approvisionnement en batteries avec Batterix a été renouvelé en mars 2025.")],
        [p("8. Risques", "Heading1"),
         p("Les principaux risques identifiés sont la pénurie de cellules lithium-ion, la hausse du prix de l'aluminium "
           "et la concurrence des marques asiatiques à bas prix. Un stock de sécurité de batteries a été mis en place."),
         p("Le risque de change concerne surtout les achats de moteurs, réglés en dollars américains.")],
        [p("9. Perspectives 2026", "Heading1"),
         p("Vélanor vise un chiffre d'affaires de 55 M€ en 2026. Une seconde usine d'assemblage ouvrira à Saint-Nazaire "
           "en septembre 2026, avec 70 embauches prévues."),
         p("Un nouveau modèle compact, le Vilaine Compact, sera lancé en avril 2026.")],
    ]
    pdf(DOCS / "rapport-annuel-2025.pdf", pages, "Vélanor — Rapport annuel 2025")


CONTRAT = [
    ["CONTRAT D'APPROVISIONNEMENT N° BX-2025-117", "",
     "Entre : Vélanor SAS, 12 quai de la Fosse, 44000 Nantes (l'Acheteur)",
     "Et : Batterix GmbH, Brême, Allemagne (le Fournisseur)", "",
     "Article 1 - Objet",
     "Fourniture de batteries 48 V 14 Ah, référence BAT-48V-14Ah.", "",
     "Article 2 - Durée",
     "Trois ans à compter du 1er mars 2025.", "",
     "Article 3 - Volumes",
     "Volume minimal annuel : 40 000 batteries.", "",
     "Article 4 - Prix",
     "Prix unitaire : 212 euros HT, révisable une fois par an."],
    ["Article 5 - Délais de livraison",
     "Le Fournisseur livre sous 21 jours après la commande.", "",
     "Article 6 - Pénalités de retard",
     "0,5 % du montant de la commande par jour de retard,",
     "plafonnées à 8 % du montant de la commande.", "",
     "Article 7 - Garantie",
     "5 ans ou 1 000 cycles de charge, au premier terme atteint.", "",
     "Article 8 - Litiges",
     "Tribunal de commerce de Nantes.", "",
     "Fait à Nantes, le 14 février 2025.",
     "Pour Vélanor : Hélène Marchais    Pour Batterix : Jonas Weber"],
]


def scan():
    rnd = random.Random(GRAINE)
    police = ImageFont.truetype(POLICE, 30)
    images = []
    for lignes in CONTRAT:
        img = Image.new("L", (1240, 1754), 250)
        d = ImageDraw.Draw(img)
        y = 140
        for l in lignes:
            d.text((120, y), l, fill=20, font=police)
            y += 52
        img = img.rotate(rnd.uniform(1.0, 2.0), expand=False, fillcolor=250)
        px = img.load()
        for _ in range(60000):
            x, yy = rnd.randrange(1240), rnd.randrange(1754)
            px[x, yy] = rnd.choice((90, 140, 200))
        img = img.filter(ImageFilter.GaussianBlur(0.6))
        images.append(img.convert("RGB"))
    images[0].save(DOCS / "contrat-batterix-scan.pdf", save_all=True, append_images=images[1:], resolution=150,
                   creationDate=DATE_PDF, modDate=DATE_PDF)


def docx():
    d = Document()
    d.core_properties.created = d.core_properties.modified = __import__("datetime").datetime(2025, 9, 1)
    d.add_heading("Procédure PR-SEC-04 — Charge et stockage des batteries", 0)
    d.add_paragraph("Responsable de la procédure : Karim Benali, responsable HSE. Version 3 du 1er septembre 2025.")
    d.add_heading("1. Stockage", 1)
    d.add_paragraph("Les batteries sont stockées entre 10 °C et 25 °C, dans le local B2 équipé d'une détection incendie.")
    d.add_paragraph("Pour un stockage de plus de 30 jours, la charge est ramenée à 80 % au maximum.")
    d.add_heading("2. Charge", 1)
    d.add_paragraph("La charge se fait uniquement sur les postes équipés d'un chargeur homologué, sous surveillance.")
    d.add_paragraph("Une batterie gonflée ou chaude est isolée immédiatement dans le bac sable du local B2.")
    d.add_heading("3. Contrôles", 1)
    t = d.add_table(rows=1, cols=3)
    t.style = "Table Grid"
    for c, v in zip(t.rows[0].cells, ("Contrôle", "Fréquence", "Responsable")): c.text = v
    for ligne in (("Inspection du local B2", "le premier lundi de chaque mois", "Karim Benali"),
                  ("Vérification des extincteurs de classe D", "tous les 6 mois", "prestataire Sécurifeu"),
                  ("Formation des opérateurs", "à l'embauche puis tous les 2 ans", "service RH")):
        for c, v in zip(t.add_row().cells, ligne): c.text = v
    d.save(DOCS / "procedure-batteries.docx")


def pptx():
    pr = Presentation()
    pr.core_properties.created = pr.core_properties.modified = __import__("datetime").datetime(2025, 11, 20)
    diapos = [("Stratégie 2026", ["Comité de direction du 20 novembre 2025", "Document fictif"]),
              ("Objectifs 2026", ["Chiffre d'affaires visé : 55 M€", "Part de l'export visée : 32 %", "Marge nette visée : 7 %"]),
              ("Nouveau modèle", ["Vilaine Compact : vélo pliant électrique", "Lancement en avril 2026", "Prix public : 2 490 € TTC"]),
              ("Usine de Saint-Nazaire", ["Ouverture en septembre 2026", "Capacité : 25 000 vélos par an", "Investissement : 14 M€"]),
              ("Export", ["Allemagne : croissance visée de 30 %", "Pays-Bas : ouverture d'un showroom à Utrecht"])]
    for titre, puces in diapos:
        s = pr.slides.add_slide(pr.slide_layouts[1])
        s.shapes.title.text = titre
        tf = s.placeholders[1].text_frame
        tf.text = puces[0]
        for x in puces[1:]:
            tf.add_paragraph().text = x
        for para in tf.paragraphs:
            for r in para.runs: r.font.size = Pt(24)
    pr.save(DOCS / "strategie-2026.pptx")


def xlsx():
    wb = Workbook()
    wb.properties.created = wb.properties.modified = __import__("datetime").datetime(2025, 10, 31)
    ws = wb.active
    ws.title = "Stocks"
    ws.append(["Référence", "Désignation", "Quantité", "Seuil d'alerte", "Entrepôt"])
    for l in (["BAT-48V-14Ah", "Batterie 48 V 14 Ah", 1240, 1500, "Nantes"],
              ["MOT-250W", "Moteur roue arrière 250 W", 2105, 1200, "Nantes"],
              ["CAD-ALU-L", "Cadre aluminium taille L", 860, 600, "Cholet"],
              ["CAD-ALU-M", "Cadre aluminium taille M", 1020, 600, "Cholet"],
              ["FRN-HYD-02", "Frein hydraulique", 3400, 2000, "Nantes"],
              ["PNU-700-38", "Pneu 700x38", 5150, 3000, "Nantes"]):
        ws.append(l)
    ws2 = wb.create_sheet("Fournisseurs")
    ws2.append(["Fournisseur", "Composant", "Délai moyen constaté (jours)"])
    for l in (["Batterix GmbH", "Batteries", 24], ["Motodrive Co.", "Moteurs", 45],
              ["Stopline", "Freins", 12], ["Gomma Ouest", "Pneus", 6]):
        ws2.append(l)
    wb.save(DOCS / "stocks-octobre-2025.xlsx")


HTML = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Vélanor — FAQ du service après-vente</title></head>
<body>
<h1>FAQ du service après-vente</h1>
<p>Document fictif.</p>
<h2>Quelle est la durée de la garantie ?</h2>
<p>Le cadre est garanti 7 ans. La batterie et le moteur sont garantis 2 ans.</p>
<h2>Quel est le délai de réparation ?</h2>
<p>Une réparation en atelier prend 10 jours ouvrés en moyenne. Le diagnostic est gratuit.</p>
<h2>Comment joindre le service après-vente ?</h2>
<p>Par téléphone au 02 40 00 12 34, du lundi au vendredi de 9 h à 18 h, ou par le formulaire du site.</p>
<h2>Peut-on remplacer soi-même la batterie ?</h2>
<p>Oui, la batterie se retire avec la clé fournie. Seule une batterie d'origine Vélanor est couverte par la garantie.</p>
</body></html>
"""

MD = """# Compte rendu de la réunion du CSE du 14 octobre 2025

Document fictif.

## Participants

Hélène Marchais (présidente), Sophie Le Gall (secrétaire du CSE), sept élus.

## Décisions

- Prime d'intéressement 2025 : 1 150 euros par salarié, versée en avril 2026.
- Télétravail : jusqu'à 2 jours par semaine pour les postes compatibles.
- Le nouveau restaurant d'entreprise du site de Nantes ouvrira en janvier 2026.

## Points reportés

La question des horaires d'été de l'atelier de Cholet est reportée à la réunion de décembre.
"""


def anglais():
    pages = [[p("Supplier Quality Audit — Batterix GmbH, Bremen", "Title"),
              p("Fictional document. Audit date: 18 June 2025. Lead auditor: Laura Fischer (Vélanor quality team)."),
              p("Overall score: 87 out of 100. The supplier is approved for another year."),
              p("Two minor non-conformities were found: incomplete labelling of pallets, and missing ESD wrist straps "
                "at one assembly station."),
              p("The measured cell defect rate is 0.3 %. The next audit is scheduled for June 2026.")]]
    pdf(DOCS / "supplier-audit-batterix-en.pdf", pages, "Supplier Quality Audit — Batterix")


def figer_zip(chemin):
    """Réécrit un fichier Office (zip) avec des dates fixes, pour des empreintes reproductibles."""
    import zipfile
    with zipfile.ZipFile(chemin) as z:
        entrees = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED) as z:
        for nom, data in entrees:
            if nom == "docProps/core.xml":  # openpyxl y écrit l'heure de l'enregistrement
                data = __import__("re").sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*", rb"\g<1>2025-11-08T00:00:00Z", data)
            z.writestr(zipfile.ZipInfo(nom, (2025, 11, 8, 0, 0, 0)), data, zipfile.ZIP_DEFLATED)


def main():
    random.seed(GRAINE)
    DOCS.mkdir(parents=True, exist_ok=True)
    rapport_annuel(); scan(); docx(); pptx(); xlsx(); anglais()
    for f in ("procedure-batteries.docx", "strategie-2026.pptx", "stocks-octobre-2025.xlsx"):
        figer_zip(DOCS / f)
    (DOCS / "faq-sav.html").write_text(HTML, encoding="utf-8")
    (DOCS / "cse-2025-10-14.md").write_text(MD, encoding="utf-8")
    fichiers = sorted(f for f in DOCS.iterdir() if f.is_file())
    man = {"graine": GRAINE, "entreprise": "Vélanor SAS (fictive)",
           "documents": [{"fichier": f.name, "octets": f.stat().st_size,
                          "sha256": hashlib.sha256(f.read_bytes()).hexdigest()} for f in fichiers]}
    (CORPUS / "MANIFEST.json").write_text(json.dumps(man, ensure_ascii=False, indent=2))
    for d in man["documents"]:
        print(f"{d['octets']:>9}  {d['sha256'][:12]}  {d['fichier']}")


if __name__ == "__main__":
    main()
