#!/usr/bin/env python3
"""Podcasts : choix d'une seconde voix pour le français, profils de locuteur et d'épisode, génération, mesure.

1. aller-retour synthèse (Kokoro) puis transcription (faster-whisper-small) d'une phrase française, par voix :
   taux de mots retrouvés (mesure de l'intelligibilité, pas de la qualité perçue) ;
2. profil de locuteur « duo-fr » (2 voix) et profil d'épisode « court-fr » (fr-FR, 3 segments) ;
3. génération à partir du carnet indiqué, suivi du job, durée, taille et durée audio, extrait de transcription.
Sortie : outils/resultats/open-notebook/podcast-<date>.json ; audio dans donnees/podcasts/.
"""
import datetime, json, re, subprocess, sys, time, unicodedata, urllib.request, uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from client import RACINE, OpenNotebook

SP = "http://127.0.0.1:8969/v1"
PHRASE = ("Le chiffre d'affaires de l'entreprise a progressé de douze pour cent, et la nouvelle usine de "
          "Saint-Nazaire ouvrira en septembre avec soixante-dix embauches.")
VOIX = ["ff_siwis", "em_alex", "im_nicola", "pm_alex", "am_michael", "bm_george"]
CARNET = sys.argv[1] if len(sys.argv) > 1 else "Essai installation"


def mots(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return re.findall(r"[a-z]+", "".join(c for c in t if not unicodedata.combining(c)))


def tts(voix, texte):
    req = urllib.request.Request(SP + "/audio/speech", json.dumps({"model": "speaches-ai/Kokoro-82M-v1.0-ONNX", "voice": voix,
                                 "input": texte, "response_format": "mp3"}).encode(), {"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=300).read()


def stt(audio):
    b = uuid.uuid4().hex
    corps = (f'--{b}\r\nContent-Disposition: form-data; name="model"\r\n\r\nSystran/faster-whisper-small\r\n'
             f'--{b}\r\nContent-Disposition: form-data; name="language"\r\n\r\nfr\r\n'
             f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n').encode() \
        + audio + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request(SP + "/audio/transcriptions", corps, {"Content-Type": f"multipart/form-data; boundary={b}"})
    return json.loads(urllib.request.urlopen(req, timeout=300).read())["text"]


res = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "phrase": PHRASE, "voix": []}
ref = mots(PHRASE)
for v in VOIX:
    t0 = time.time(); a = tts(v, PHRASE); d_tts = time.time() - t0
    t = stt(a); h = mots(t)
    taux = round(sum(1 for m in ref if m in h) / len(ref), 2)
    res["voix"].append({"voix": v, "mots_retrouves": taux, "transcription": t, "tts_s": round(d_tts, 1)})
    print(f"{v:12} {taux:.2f}  {t}", flush=True)
seconde = max((x for x in res["voix"] if x["voix"] != "ff_siwis"), key=lambda x: x["mots_retrouves"])["voix"]
res["seconde_voix"] = seconde

on = OpenNotebook()
mods = {m["name"]: m["id"] for m in on.get("/api/models")}
spk = next((p for p in on.get("/api/speaker-profiles") if p["name"] == "duo-fr"), None) or on.post("/api/speaker-profiles", {
    "name": "duo-fr", "description": "Deux voix pour un épisode en français", "voice_model": mods["speaches-ai/Kokoro-82M-v1.0-ONNX"],
    "speakers": [
        {"name": "Camille", "voice_id": "ff_siwis", "backstory": "Animatrice, pose des questions simples.",
         "personality": "Curieuse, claire, phrases courtes."},
        {"name": "Hugo", "voice_id": seconde, "backstory": "Analyste de l'entreprise, connaît les documents.",
         "personality": "Précis, cite les chiffres."}]})
ep = next((p for p in on.get("/api/episode-profiles") if p["name"] == "court-fr"), None) or on.post("/api/episode-profiles", {
    "name": "court-fr", "description": "Épisode court en français", "speaker_config": spk["id"],
    "outline_llm": mods["qwen3:4b-instruct"], "transcript_llm": mods["qwen3:4b-instruct"], "language": "fr-FR",
    "default_briefing": "Épisode court et factuel, en français, qui présente les informations principales des sources.",
    "num_segments": 3, "max_tokens": 4096})
res["profils"] = {"locuteur": spk, "episode": ep}
nb = next(n for n in on.get("/api/notebooks") if n["name"] == CARNET)
t0 = time.time()
job = on.post("/api/podcasts/generate", {"episode_profile": "court-fr", "speaker_profile": "duo-fr",
                                         "episode_name": f"Essai {CARNET}", "notebook_id": nb["id"]})
res["job"] = job
etat = {}
while time.time() - t0 < 3600:
    time.sleep(15)
    etat = on.get(f"/api/podcasts/jobs/{job['job_id']}")
    if etat["status"] in ("completed", "failed", "error"):
        break
res["etat_final"] = etat
res["duree_generation_s"] = round(time.time() - t0, 1)
print("job :", etat.get("status"), res["duree_generation_s"], "s", etat.get("error_message"))
episodes = [e for e in on.get("/api/podcasts/episodes") if e.get("name") == f"Essai {CARNET}"]
if episodes:
    e = on.get(f"/api/podcasts/episodes/{episodes[0]['id']}")
    res["episode"] = {k: e.get(k) for k in ("id", "name", "job_status", "error_message", "audio_file")}
    tr = e.get("transcript") or {}
    res["episode"]["transcription_debut"] = json.dumps(tr, ensure_ascii=False)[:1500]
    try:
        req = urllib.request.Request(f"http://127.0.0.1:5055/api/podcasts/episodes/{e['id']}/audio",
                                     headers={"Authorization": f"Bearer {on.mdp}"})
        dest = RACINE / "donnees/podcasts" / f"{e['id'].replace(':', '_')}.mp3"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(urllib.request.urlopen(req, timeout=120).read())
        res["episode"]["octets"] = dest.stat().st_size
        res["episode"]["duree_audio_s"] = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                                                "-of", "csv=p=0", str(dest)], capture_output=True, text=True).stdout or 0)
        res["episode"]["fichier_local"] = str(dest.relative_to(RACINE))
    except Exception as ex:
        res["episode"]["audio_erreur"] = repr(ex)[:300]
    print("épisode :", {k: v for k, v in res["episode"].items() if k != "transcription_debut"})
sortie = RACINE / f"outils/resultats/open-notebook/podcast-{datetime.date.today()}.json"
sortie.write_text(json.dumps(res, ensure_ascii=False, indent=2))
print("->", sortie.relative_to(RACINE))
