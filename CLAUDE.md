# Dépôt : manuels vérifiés de solutions de RAG local

La mission complète est dans `kit/PROMPT.md`. La solution en cours est indiquée par le `/goal` de la session et par `JOURNAL.md`.

## À relire après toute compaction ou reprise

1. `JOURNAL.md` (dernière entrée : où en est le travail).
2. La fiche de la solution en cours dans `kit/fiches/`.
3. Les sections du `kit/PROMPT.md` utiles à la phase en cours.

## Règles permanentes

- Travail autonome : ne jamais poser de question ni attendre. Une décision hors enveloppe va dans « Décisions en attente », puis le travail continue avec l'option la plus prudente.
- Rien n'est écrit de mémoire : chaque affirmation [Vérifié] renvoie à un script de `outils/` et à un résultat brut de `outils/resultats/`.
- Interdits : `sudo`, `sysctl`, `pkill -f`, `git push`, port publié hors de `127.0.0.1`, compte en ligne, dépense, `curl … | bash`, `docker … prune`, suppression hors du dépôt et des ressources Docker préfixées `rag-`.
- Ressources Docker préfixées `rag-` ; données dans `donnees/` (ignoré par git).
- Manuels : ton impersonnel (aucun « vous », « nous », « notre », « vos »), aucun pictogramme, libellés de l'interface cités tels quels.
- Avant chaque commit : `python3 outils/communs/verifier_docs.py` à 0 point (dès que le script existe).
- Commits en français, un par fonctionnalité, essai ou manuel, préfixés par le périmètre, sans trailer Co-Authored-By ni mention d'outil.
- Toujours la dernière version stable de la solution et des images (`outils/communs/versions.py`), figée par empreinte.
- Modèles : LLM-Service seulement (`outils/communs/llm_service.sh`), jamais un serveur de modèles propre à la solution ; même `num_ctx` (16384) partout.
- Un seul essai lourd à la fois ; `free -m` avant chacun.
- `JOURNAL.md` complété à la fin de chaque étape.
- Lectures volumineuses (documentation, code source, journaux) confiées à des sous-agents.
