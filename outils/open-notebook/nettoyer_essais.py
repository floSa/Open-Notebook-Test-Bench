#!/usr/bin/env python3
"""Fin de mission : supprime les carnets d'essai (et leurs sources propres), garde « Démo Vélanor », l'épisode de podcast,
les profils et la transformation personnalisée. Sortie : outils/resultats/open-notebook/nettoyage-<date>.txt"""
import datetime, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from client import RACINE, OpenNotebook

GARDER = {"Démo Vélanor"}
on = OpenNotebook()
lignes = [f"# Nettoyage des artefacts d'essai, {datetime.datetime.now().isoformat(timespec='seconds')}"]
for n in on.get("/api/notebooks"):
    if n["name"] in GARDER:
        lignes.append(f"gardé : {n['name']}")
    else:
        on.delete(f"/api/notebooks/{n['id']}?delete_exclusive_sources=true")
        lignes.append(f"supprimé : {n['name']} (et ses sources propres)")
lignes.append("carnets restants : " + ", ".join(n["name"] for n in on.get("/api/notebooks")))
lignes.append(f"sources restantes : {len(on.get('/api/sources?limit=100'))}")
lignes.append("épisodes : " + ", ".join(e["name"] for e in on.get("/api/podcasts/episodes")))
out = RACINE / f"outils/resultats/open-notebook/nettoyage-{datetime.date.today()}.txt"
out.write_text("\n".join(lignes) + "\n")
print("\n".join(lignes))
