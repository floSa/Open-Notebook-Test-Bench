"""Auto-contrôle de la notation du banc : python3 outils/communs/banc/tests/test_commun.py"""
import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from commun import exacte, citation_correcte, REFUS
assert exacte("Le CA est de 48.6 M€", ["48,6"])
assert exacte("40000 batteries", ["40 000"]) and exacte("40 000 batteries", ["40 000"])
assert exacte("taux de 0,3 %", ["0.3|0,3"])
assert exacte("stock 1240 sous le seuil de 1500", ["1 240|1240", "1 500|1500"])
assert not exacte("environ 48 M€", ["48,6"])
assert not exacte("21 jours", ["21", "24"])
assert REFUS.search("Les documents ne mentionnent pas de directeur financier.")
assert REFUS.search("Je ne trouve aucune information sur 2022.")
assert not REFUS.search("Le chiffre d'affaires est de 48,6 M€.")
s = [{"document": "rapport-annuel-2025.pdf", "page": 3}]
assert citation_correcte([{"document": "rapport-annuel-2025.pdf", "page": 3}], s) == {"document": True, "page": True}
assert citation_correcte([{"document": "rapport-annuel-2025.pdf", "page": None}], s) == {"document": True, "page": None}
assert citation_correcte([{"document": "faq-sav.html"}], s) == {"document": False, "page": None}
assert citation_correcte([], []) is None
print("notation du banc : 13 contrôles OK")
