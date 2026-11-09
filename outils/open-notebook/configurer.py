#!/usr/bin/env python3
"""Branche Open Notebook au service de modèles LLM-Service par l'API (idempotent).

Équivalent de l'interface : Models > Add Configuration (fournisseur Ollama, Base URL), ajout des modèles,
puis modèles par défaut (PUT explicite plutôt que « Auto-assign », qui choisit par ordre alphabétique).
Usage : python3 outils/open-notebook/configurer.py [--num-ctx 16384] [--chat qwen3:4b-instruct]
"""
import argparse, datetime, json, os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from client import RACINE, OpenNotebook

p = argparse.ArgumentParser()
p.add_argument("--moteur", choices=["ollama", "vllm"], default="ollama", help="service de modèles LLM-Service : branche service-ollama ou service-vllm")
p.add_argument("--num-ctx", type=int, default=16384)
p.add_argument("--chat", default="qwen3:4b-instruct")
p.add_argument("--second", default="ministral-3:3b")
p.add_argument("--embed", default="bge-m3")
p.add_argument("--voix", action="store_true", help="branche aussi Speaches (TTS, STT)")
a = p.parse_args()

on = OpenNotebook()
on.attendre_sante()
journal = {"date": datetime.datetime.now().isoformat(timespec="seconds"), "moteur": a.moteur}

if a.moteur == "ollama":
    provider = "ollama"
    # Modèles servis par LLM-Service (ollama-central, réseau llm-net) ; « ollama-socle » : ancien nom, repris s'il existe.
    cred = next((c for c in on.get("/api/credentials") if c["name"] in ("llm-service", "ollama-socle")), None)
    corps = {"name": "llm-service", "provider": provider, "modalities": ["language", "embedding"],
             "base_url": os.environ.get("LLM_SERVICE_URL", "http://ollama-central:11434"), "num_ctx": a.num_ctx}
    cred = on.put(f"/api/credentials/{cred['id']}", corps) if cred else on.post("/api/credentials", corps)
    journal["credential"] = cred
    journal["test_connexion"] = on.post(f"/api/credentials/{cred['id']}/test")
    journal["decouverte"] = on.post(f"/api/credentials/{cred['id']}/discover")
    cred_chat = cred_embed = cred
else:
    # vLLM : un serveur par modèle (chat et embedding sur deux conteneurs distincts), API OpenAI uniquement.
    provider = "openai_compatible"

    def brancher(nom, base_url, modalite):
        c = next((c for c in on.get("/api/credentials") if c["name"] == nom), None)
        corps = {"name": nom, "provider": provider, "modalities": [modalite], "base_url": base_url, "api_key": "local"}
        c = on.put(f"/api/credentials/{c['id']}", corps) if c else on.post("/api/credentials", corps)
        journal[f"test_connexion_{modalite}"] = on.post(f"/api/credentials/{c['id']}/test")
        return c

    cred_chat = brancher("llm-service-chat", os.environ.get("LLM_SERVICE_CHAT_URL", "http://vllm-central:8000/v1"), "language")
    cred_embed = brancher("llm-service-embed", os.environ.get("LLM_SERVICE_EMBED_URL", "http://vllm-embed:8000/v1"), "embedding")
    journal["credential"] = {"chat": cred_chat, "embed": cred_embed}

existants = {(m["name"], m["type"]): m for m in on.get("/api/models")}
ids = {}
for nom, typ, cred_ in ((a.chat, "language", cred_chat), (a.second, "language", cred_chat), (a.embed, "embedding", cred_embed)):
    if nom in ids:
        continue  # a.second == a.chat (cas vLLM, un seul modèle) : rien à créer deux fois
    m = existants.get((nom, typ)) or on.post("/api/models", {"name": nom, "provider": provider, "type": typ, "credential": cred_["id"]})
    ids[nom] = m["id"]
journal["modeles"] = ids
journal["defauts"] = on.put("/api/models/defaults", {
    "default_chat_model": ids[a.chat], "default_transformation_model": ids[a.chat],
    "large_context_model": ids[a.chat], "default_tools_model": ids[a.chat],
    "default_embedding_model": ids[a.embed]})

# Voix (option --voix) : Speaches (rag-speaches) par le fournisseur « OpenAI Compatible » ; Ollama ne fait ni TTS ni STT.
if a.voix:
    cv = next((c for c in on.get("/api/credentials") if c["name"] == "speaches-voix"), None)
    corps = {"name": "speaches-voix", "provider": "openai_compatible", "modalities": ["text_to_speech", "speech_to_text"],
             "base_url": "http://rag-speaches:8000/v1", "api_key": "local"}
    cv = on.put(f"/api/credentials/{cv['id']}", corps) if cv else on.post("/api/credentials", corps)
    journal["voix_test"] = on.post(f"/api/credentials/{cv['id']}/test")
    existants = {(m["name"], m["type"]): m for m in on.get("/api/models")}
    for nom, typ in (("speaches-ai/Kokoro-82M-v1.0-ONNX", "text_to_speech"), ("Systran/faster-whisper-small", "speech_to_text")):
        m = existants.get((nom, typ)) or on.post("/api/models", {"name": nom, "provider": "openai_compatible", "type": typ, "credential": cv["id"]})
        ids[nom] = m["id"]
    journal["defauts"] = on.put("/api/models/defaults", {
        "default_text_to_speech_model": ids["speaches-ai/Kokoro-82M-v1.0-ONNX"],
        "default_speech_to_text_model": ids["Systran/faster-whisper-small"]})
    journal["modeles"] = ids

# Extraction des URL : moteur « simple » pour éviter le repli vers un service tiers (Jina) en mode auto.
reglages = on.get("/api/settings")
journal["reglages_avant"] = reglages
if "default_content_processing_engine_url" in reglages:
    reglages["default_content_processing_engine_url"] = "simple"
    journal["reglages_apres"] = on.put("/api/settings", reglages)

sortie = RACINE / f"outils/resultats/open-notebook/configuration-{datetime.date.today()}{os.environ.get('RESULTAT_SUFFIXE', '')}.json"
sortie.write_text(json.dumps(journal, ensure_ascii=False, indent=2))
print(json.dumps({k: journal[k] for k in ("test_connexion", "voix_test", "modeles") if k in journal}, ensure_ascii=False))
print("défauts :", {k: v for k, v in journal["defauts"].items() if v})
print("->", sortie.relative_to(RACINE))
