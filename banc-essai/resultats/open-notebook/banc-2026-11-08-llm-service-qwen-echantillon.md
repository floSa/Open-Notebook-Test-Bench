# Banc open-notebook — llm-service-qwen-echantillon — 2026-11-08T22:45:45

| Mesure | Valeur |
|---|---|
| questions | 6 |
| exactes | 4 |
| sur | 5 |
| refus_corrects | 1 |
| pieges | 1 |
| citation_bon_document | 3 |
| citation_bonne_page | 0 |
| citations_avec_page | 0 |
| juge_llm_oui | 0 |
| juge_llm_sur | 0 |
| erreurs | 0 |
| latence_p50_s | 17.35 |
| latence_p95_s | 127.49 |
| par_type | {'tableau': '3/3', 'scan': '0/1', 'multi-documents': '1/1', 'piège': '1/1'} |
| pic_ram_mo | {'rag-open-notebook': 3886, 'rag-open-notebook-surrealdb': 100, 'ollama-central': 5593} |
| pic_ram_application_mo | 3986 |
| vram | sans objet (aucun GPU NVIDIA, socle CPU) |
| indexation_s | None |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | - | True | 127.49 | Le chiffre d'affaires de Vélanor en 2025 s'élève à 48,6 M€ [source:ky761pntfu5q1 |
| Q08 | tableau | oui | - | False | 8.63 | Le prix public du modèle Erdre Cargo est de 4 290 € TTC. [source:kyqoz60d4gkh1ko |
| Q18 | scan | non | - | False | 19.2 | Le contrat de Batterix n’indique pas explicitement un volume minimal annuel de b |
| Q24 | tableau | oui | - | True | 20.38 | Le stock de batteries BAT-48V-14Ah reste de 1240 unités, comme indiqué dans le t |
| Q32 | multi-documents | oui | - | True | 17.35 | Vélanor vise un chiffre d'affaires de 55 M€ en 2026 [source:kyqoz60d4gkh1koz7k1c |
| Q35 | piège | oui | - | - | 16.55 | Le chiffre d'affaires de Vélanor en 2022 n'est pas mentionné dans les documents  |
