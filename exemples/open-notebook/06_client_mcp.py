#!/usr/bin/env python3
"""Client MCP minimal (stdio) pour le serveur tiers open-notebook-mcp 0.3.0 : liste des outils, puis appels.

Prérequis : uv pip install --python .venv/bin/python "open-notebook-mcp==0.3.0" "mcp<2"
Lancement : .venv/bin/python exemples/open-notebook/06_client_mcp.py
Seuls des outils de lecture sont appelés, plus create_source pour constater son refus (défaut connu)."""
import asyncio, json, os, sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

RACINE = Path(__file__).resolve().parents[2]
env = RACINE / "donnees/open-notebook/.env"
MDP = os.environ.get("ON_MDP") or next(l.split("=", 1)[1] for l in env.read_text().splitlines() if l.startswith("OPEN_NOTEBOOK_PASSWORD="))
PARAMS = StdioServerParameters(command=str(Path(sys.executable).with_name("open-notebook-mcp")),
                               env={"OPEN_NOTEBOOK_URL": "http://127.0.0.1:5055", "OPEN_NOTEBOOK_PASSWORD": MDP})


async def appel(s, nom, args):
    r = await s.call_tool(nom, args)
    texte = r.content[0].text if r.content else ""
    print(f"-- {nom} {json.dumps(args, ensure_ascii=False)} -> {'ERREUR' if r.isError else 'ok'} : {texte[:400]}")
    return texte


async def main():
    async with stdio_client(PARAMS) as (lecture, ecriture):
        async with ClientSession(lecture, ecriture) as s:
            await s.initialize()
            outils = (await s.list_tools()).tools
            print(len(outils), "outils :", ", ".join(sorted(o.name for o in outils)))
            carnets = json.loads(await appel(s, "list_notebooks", {"limit": 20}))
            liste = carnets.get("notebooks", carnets) if isinstance(carnets, dict) else carnets
            essai = next(n["id"] for n in liste if n["name"] == "Essai installation")
            await appel(s, "search", {"query": "prime d'intéressement", "type": "text", "limit": 3})
            await appel(s, "create_source", {"notebook_id": essai, "type": "text", "content": "essai MCP", "title": "essai MCP"})


asyncio.run(main())
