#!/usr/bin/env python3
"""Génère le document audio du corpus (message vocal fictif) par synthèse vocale locale (Speaches, Kokoro, voix ff_siwis).

Prérequis : outils/communs/voix.sh (rag-speaches sur 127.0.0.1:8969). Puis relancer generer_corpus.py pour le MANIFEST.
La synthèse n'est pas garantie identique à l'octet d'une version de Speaches à l'autre ; l'empreinte du MANIFEST fait foi.
"""
import json, urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
TEXTE = ("Message vocal de Julien Moreau, directeur de production chez Vélanor, enregistré le 3 novembre 2025. "
         "La ligne d'assemblage numéro 3 de Nantes sera arrêtée du 2 au 6 mars 2026 pour maintenance. "
         "Pendant cet arrêt, la production du Loire Urban sera transférée sur la ligne 1. "
         "La réunion de lancement aura lieu le lundi 9 février à 10 heures, dans la salle Erdre.")
corps = {"model": "speaches-ai/Kokoro-82M-v1.0-ONNX", "voice": "ff_siwis", "input": TEXTE, "response_format": "mp3"}
req = urllib.request.Request("http://127.0.0.1:8969/v1/audio/speech", json.dumps(corps).encode(), {"Content-Type": "application/json"})
sortie = RACINE / "corpus/documents/message-vocal-production.mp3"
sortie.write_bytes(urllib.request.urlopen(req, timeout=300).read())
print(sortie.relative_to(RACINE), sortie.stat().st_size, "octets")
