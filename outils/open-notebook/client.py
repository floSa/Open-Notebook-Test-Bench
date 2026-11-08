"""Client minimal de l'API REST d'Open Notebook 1.15.1 (bibliothèque standard seulement).

Lit le mot de passe dans donnees/open-notebook/.env. Toutes les routes sont sous /api.
"""
import json, time, urllib.error, urllib.request, uuid
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
ENV = RACINE / "donnees/open-notebook/.env"
API = "http://127.0.0.1:5055"


def lire_env():
    return dict(l.split("=", 1) for l in ENV.read_text().splitlines() if "=" in l and not l.startswith("#"))


class OpenNotebook:
    def __init__(self, api=API, mot_de_passe=None):
        self.api = api
        self.mdp = mot_de_passe if mot_de_passe is not None else lire_env().get("OPEN_NOTEBOOK_PASSWORD", "")

    def _req(self, methode, chemin, corps=None, donnees=None, entetes=None, timeout=1800):
        h = {"Authorization": f"Bearer {self.mdp}"} if self.mdp else {}
        if corps is not None:
            donnees, h["Content-Type"] = json.dumps(corps).encode(), "application/json"
        h.update(entetes or {})
        req = urllib.request.Request(self.api + chemin, data=donnees, headers=h, method=methode)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                t = r.read()
                return json.loads(t) if t else None
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"{methode} {chemin} -> {e.code} {e.read()[:500].decode(errors='replace')}") from None

    def get(self, c, **kw): return self._req("GET", c, **kw)
    def post(self, c, corps=None, **kw): return self._req("POST", c, corps, **kw)
    def put(self, c, corps=None, **kw): return self._req("PUT", c, corps, **kw)
    def delete(self, c, **kw): return self._req("DELETE", c, **kw)

    def attendre_sante(self, delai=300):
        fin = time.time() + delai
        while time.time() < fin:
            try:
                if self._req("GET", "/health", timeout=5)["status"] == "healthy":
                    return True
            except Exception:
                pass
            time.sleep(3)
        raise TimeoutError("API Open Notebook non joignable")

    def ajouter_fichier(self, chemin, notebook_id, embed=True):
        """POST /api/sources en multipart (seul format accepté pour un fichier)."""
        chemin = Path(chemin)
        b = uuid.uuid4().hex
        champs = {"type": "upload", "notebooks": json.dumps([notebook_id]), "embed": str(embed).lower(),
                  "async_processing": "true", "title": chemin.name}
        corps = b"".join(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in champs.items())
        corps += (f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="{chemin.name}"\r\n'
                  f"Content-Type: application/octet-stream\r\n\r\n").encode() + chemin.read_bytes() + f"\r\n--{b}--\r\n".encode()
        return self._req("POST", "/api/sources", donnees=corps, entetes={"Content-Type": f"multipart/form-data; boundary={b}"})

    def attendre_source(self, source_id, delai=1800, embed=True):
        """Attend l'extraction (status) puis l'embedding (embedded_chunks > 0), qui est un job séparé."""
        fin, etat = time.time() + delai, None
        while time.time() < fin:
            etat = self.get(f"/api/sources/{source_id}/status")
            if etat["status"] == "failed":
                return {"status": "failed", "detail": etat}
            if etat["status"] == "completed":
                s = self.get(f"/api/sources/{source_id}")
                if not embed or (s.get("embedded_chunks") or 0) > 0:
                    return {"status": "completed", "embedded_chunks": s.get("embedded_chunks"),
                            "caracteres": len(s.get("full_text") or "")}
            time.sleep(5)
        return {"status": "timeout", "detail": etat}

    def demander(self, notebook_id, question, contexte_sources, titre="banc"):
        """Une question dans une nouvelle session de chat du carnet ; renvoie (réponse, session_id)."""
        s = self.post("/api/chat/sessions", {"notebook_id": notebook_id, "title": titre})
        ctx = self.post("/api/chat/context", {"notebook_id": notebook_id, "context_config": {"sources": contexte_sources}})
        r = self.post("/api/chat/execute", {"session_id": s["id"], "message": question, "context": ctx["context"]})
        ia = [m for m in r["messages"] if m["type"] == "ai"]
        return (ia[-1]["content"] if ia else ""), s["id"], ctx.get("token_count")
