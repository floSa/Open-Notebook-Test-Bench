#!/usr/bin/env python3
"""Bilan d'un épisode généré : script (transcript), fichier audio, transcription de contrôle par Speaches.

Complète outils/resultats/open-notebook/podcast-<date>.json (clé « episode »).
Usage : bilan_podcast.py [nom de l'épisode]
"""
import datetime, json, sys, urllib.request, uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from client import RACINE, OpenNotebook

on = OpenNotebook()
nom = sys.argv[1] if len(sys.argv) > 1 else None
eps = [e for e in on.get("/api/podcasts/episodes") if e.get("audio_file") and (nom is None or e["name"] == nom)]
assert eps, "aucun épisode avec audio"
e = eps[0]
mp3 = RACINE / "donnees/open-notebook/notebook_data/podcasts" / e["audio_file"]
donnees = mp3.read_bytes()
# transcription de contrôle (multipart construit à la main, sans dépendance)
b = uuid.uuid4().hex
corps = (f"--{b}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\nSystran/faster-whisper-small\r\n"
         f"--{b}\r\nContent-Disposition: form-data; name=\"language\"\r\n\r\nfr\r\n"
         f"--{b}\r\nContent-Disposition: form-data; name=\"response_format\"\r\n\r\nverbose_json\r\n"
         f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"e.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n").encode() + donnees + f"\r\n--{b}--\r\n".encode()
req = urllib.request.Request("http://127.0.0.1:8969/v1/audio/transcriptions", corps,
                             {"Content-Type": f"multipart/form-data; boundary={b}"})
stt = json.load(urllib.request.urlopen(req, timeout=900))
script = e["transcript"]["transcript"]
bilan = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "nom": e["name"], "id": e["id"],
         "fichier": str(mp3.relative_to(RACINE)), "taille_octets": len(donnees),
         "duree_s": round(stt.get("duration", 0), 1), "repliques": len(script),
         "locuteurs": sorted({r["speaker"] for r in script}), "script": script,
         "transcription_controle": stt["text"]}
f = RACINE / "outils/resultats/open-notebook/podcast-2026-11-08.json"
res = json.loads(f.read_text())
res["episode"] = bilan
f.write_text(json.dumps(res, ensure_ascii=False, indent=2))
print(json.dumps({k: v for k, v in bilan.items() if k != "script"}, ensure_ascii=False, indent=2))
