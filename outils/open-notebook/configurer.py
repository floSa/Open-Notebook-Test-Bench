#!/usr/bin/env python3
"""Branche Open Notebook au service LLM central de LLM-Service par l'API (idempotent).

Équivalent de l'interface : Modèles > fournisseur « OpenAI Compatible » (Base URL http://llm-central:8080/v1, clé du
service), modèles aux noms fixes chat (langage), embed (embedding), transcribe (speech-to-text), puis modèles par
défaut. La synthèse vocale n'est pas servie par le central : option --voix, serveur local rag-speaches (Kokoro).
Les anciennes configurations (Ollama, vLLM, STT de Speaches) sont retirées, avec leurs modèles.
La clé est lue dans le .env du dépôt ; elle n'est jamais affichée ni écrite dans le résultat.
Usage : python3 outils/open-notebook/configurer.py [--voix]
"""
import argparse, datetime, json, os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from client import RACINE, OpenNotebook

ANCIENS = ("llm-service", "ollama-socle", "llm-service-chat", "llm-service-embed")
p = argparse.ArgumentParser()
p.add_argument("--base-url", default="http://llm-central:8080/v1")
p.add_argument("--voix", action="store_true", help="branche aussi la synthèse vocale de rag-speaches (podcasts)")
a = p.parse_args()

env = dict(l.split("=", 1) for l in (RACINE / ".env").read_text().splitlines() if "=" in l and not l.lstrip().startswith("#"))
cle = env.get("LLM_CENTRAL_KEY", "").strip()
if not cle:
    sys.exit("clé LLM_CENTRAL_KEY absente du .env du dépôt : copier .env.example en .env et y mettre la clé du service")

on = OpenNotebook()
on.attendre_sante()
journal = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "base_url": a.base_url}


def sans_secret(c):
    return {k: v for k, v in (c or {}).items() if "key" not in k.lower() or isinstance(v, bool)}


# 1. retrait des anciennes configurations (modèles liés supprimés avec elles)
journal["retires"] = []
for c in on.get("/api/credentials"):
    if c["name"] in ANCIENS:
        r = on.delete(f"/api/credentials/{c['id']}")
        journal["retires"].append({"nom": c["name"], "reponse": r})

# 2. fournisseur « OpenAI Compatible » unique vers le service central
modalites = ["language", "embedding", "speech_to_text"]
cred = next((c for c in on.get("/api/credentials") if c["name"] == "llm-central"), None)
corps = {"name": "llm-central", "provider": "openai_compatible", "modalities": modalites, "base_url": a.base_url, "api_key": cle}
cred = on.put(f"/api/credentials/{cred['id']}", corps) if cred else on.post("/api/credentials", corps)
journal["credential"] = sans_secret(cred)
journal["test_connexion"] = on.post(f"/api/credentials/{cred['id']}/test")

# 3. modèles aux noms fixes
existants = {(m["name"], m["type"]): m for m in on.get("/api/models")}
ids = {}
for nom, typ in (("chat", "language"), ("embed", "embedding"), ("transcribe", "speech_to_text")):
    m = existants.get((nom, typ)) or on.post("/api/models", {"name": nom, "provider": "openai_compatible", "type": typ, "credential": cred["id"]})
    ids[nom] = m["id"]
journal["modeles"] = ids
defauts = {"default_chat_model": ids["chat"], "default_transformation_model": ids["chat"], "large_context_model": ids["chat"],
           "default_tools_model": ids["chat"], "default_embedding_model": ids["embed"], "default_speech_to_text_model": ids["transcribe"]}

# 4. synthèse vocale (podcasts) : rag-speaches, seulement le TTS
if a.voix:
    cv = next((c for c in on.get("/api/credentials") if c["name"] == "speaches-voix"), None)
    corps = {"name": "speaches-voix", "provider": "openai_compatible", "modalities": ["text_to_speech"],
             "base_url": "http://rag-speaches:8000/v1", "api_key": "local"}
    cv = on.put(f"/api/credentials/{cv['id']}", corps) if cv else on.post("/api/credentials", corps)
    journal["voix_test"] = on.post(f"/api/credentials/{cv['id']}/test")
    existants = {(m["name"], m["type"]): m for m in on.get("/api/models")}
    for (nom, typ), m in existants.items():  # ancien STT de Speaches : remplacé par transcribe
        if typ == "speech_to_text" and nom != "transcribe":
            on.delete(f"/api/models/{m['id']}")
            journal["retires"].append({"modele": nom})
    tts = "speaches-ai/Kokoro-82M-v1.0-ONNX"
    m = existants.get((tts, "text_to_speech")) or on.post("/api/models", {"name": tts, "provider": "openai_compatible", "type": "text_to_speech", "credential": cv["id"]})
    ids[tts] = m["id"]
    defauts["default_text_to_speech_model"] = m["id"]
journal["defauts"] = on.put("/api/models/defaults", defauts)

# 5. extraction des URL : moteur « simple » pour éviter le repli vers un service tiers (Jina) en mode auto
reglages = on.get("/api/settings")
if reglages.get("default_content_processing_engine_url") not in (None, "simple"):
    reglages["default_content_processing_engine_url"] = "simple"
    on.put("/api/settings", reglages)
journal["reglages"] = on.get("/api/settings")
journal["modeles_enregistres"] = [{k: m[k] for k in ("name", "type", "provider")} for m in on.get("/api/models")]

sortie = RACINE / f"outils/resultats/open-notebook/configuration-{datetime.date.today()}{os.environ.get('RESULTAT_SUFFIXE', '')}.json"
texte = json.dumps(journal, ensure_ascii=False, indent=2)
assert cle not in texte
sortie.write_text(texte)
print(json.dumps({k: journal[k] for k in ("test_connexion", "voix_test", "modeles") if k in journal}, ensure_ascii=False))
print("modèles enregistrés :", [(m["name"], m["type"]) for m in journal["modeles_enregistres"]])
print("->", sortie.relative_to(RACINE))
