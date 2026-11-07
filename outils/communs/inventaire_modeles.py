#!/usr/bin/env python3
"""Inventaire en lecture seule des modèles présents sur la machine.

Écrit outils/resultats/socle/modeles-existants.json. Ne modifie rien dans les dossiers lus.
Usage : python3 outils/communs/inventaire_modeles.py [MODELES_EXISTANTS]
"""
import glob, json, os, sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
SORTIE = RACINE / "outils/resultats/socle/modeles-existants.json"


def taille(p):
    if os.path.isfile(p):
        return os.path.getsize(p)
    return sum(f.stat().st_size for f in Path(p).rglob("*") if f.is_file() and not f.is_symlink()) + \
        sum(os.path.getsize(os.path.realpath(f)) for f in Path(p).rglob("*") if f.is_symlink() and os.path.isfile(f))


def type_de(nom):
    n = nom.lower()
    if any(k in n for k in ("embed", "bge-m3", "minilm", "e5-")):
        return "embedding"
    if "rerank" in n:
        return "reranker"
    if "whisper" in n:
        return "stt"
    if "mmproj" in n:
        return "projecteur-vision"
    if any(k in n for k in ("demucs",)):
        return "audio"
    return "chat"


def hf(dossier):
    for d in sorted(glob.glob(os.path.join(dossier, "models--*"))):
        nom = os.path.basename(d)[8:].replace("--", "/")
        fichiers = [f.name for f in Path(d).rglob("*") if f.is_file() or f.is_symlink()]
        fmt = "gguf" if any(f.endswith(".gguf") for f in fichiers) else \
            "safetensors" if any(f.endswith(".safetensors") for f in fichiers) else "autre"
        if "awq" in nom.lower(): fmt += " (AWQ)"
        if "gptq" in nom.lower(): fmt += " (GPTQ)"
        yield {"nom": nom, "source": d, "format": fmt, "taille_mo": taille(d) // 10**6, "type": type_de(nom)}


def gguf(dossier):
    for f in sorted(glob.glob(os.path.join(dossier, "**/*.gguf"), recursive=True)):
        yield {"nom": os.path.basename(f), "source": f, "format": "gguf",
               "taille_mo": os.path.getsize(f) // 10**6, "type": type_de(f)}


def ollama(dossier):
    for m in sorted(glob.glob(os.path.join(dossier, "manifests/registry.ollama.ai/library/*/*"))):
        man = json.load(open(m))
        nom = f"{Path(m).parent.name}:{Path(m).name}"
        yield {"nom": nom, "source": m, "format": "gguf (Ollama)",
               "taille_mo": sum(l["size"] for l in man["layers"]) // 10**6, "type": type_de(nom)}


def main():
    cherches = []
    extra = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("MODELES_EXISTANTS")
    modeles = []
    hf_dirs = [os.path.expanduser("~/.cache/huggingface/hub")] + glob.glob("/mnt/c/Users/*/.cache/huggingface/hub")
    lms = glob.glob("/mnt/c/Users/*/.lmstudio/models")
    oll = [os.path.expanduser("~/.ollama/models")] + glob.glob("/mnt/c/Users/*/.ollama/models")
    if extra:
        hf_dirs.append(extra); lms.append(extra)
    for d in hf_dirs:
        cherches.append(d); modeles += list(hf(d)) if os.path.isdir(d) else []
    for d in lms:
        cherches.append(d); modeles += list(gguf(d)) if os.path.isdir(d) else []
    for d in oll:
        cherches.append(d); modeles += list(ollama(d)) if os.path.isdir(d) else []
    res = {"dossiers_cherches": cherches, "modeles": modeles}
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(json.dumps(res, ensure_ascii=False, indent=2))
    for m in modeles:
        print(f"{m['type']:18} {m['taille_mo']:>7} Mo  {m['format']:16} {m['nom']}")
    print(f"{len(modeles)} modèles -> {SORTIE.relative_to(RACINE)}")


if __name__ == "__main__":
    main()
