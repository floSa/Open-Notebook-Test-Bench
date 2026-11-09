# Banc open-notebook — docling-qwen-fullcontent-ollama040 — 2026-11-08T23:45:33

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 28 |
| sur | 34 |
| refus_corrects | 4 |
| pieges | 4 |
| citation_bon_document | 28 |
| citation_bonne_page | 0 |
| citations_avec_page | 0 |
| juge_llm_oui | 34 |
| juge_llm_sur | 38 |
| erreurs | 0 |
| latence_p50_s | 7.44 |
| latence_p95_s | 24.19 |
| par_type | {'tableau': '10/10', 'fait simple': '13/13', 'scan': '0/4', 'anglais': '2/2', 'multi-documents': '1/3', 'audio': '2/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-open-notebook': 2989, 'rag-open-notebook-surrealdb': 144, 'ollama-central': 8653} |
| pic_ram_application_mo | 3133 |
| vram | sans objet (aucun GPU NVIDIA, socle CPU) |
| indexation_s | 84.3 |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | True | True | 71.24 | Le chiffre d'affaires de Vélanor en 2025 s'élève à 48,6 M€ [source:7xhym97yt2vhs |
| Q02 | fait simple | oui | True | True | 9.77 | Vélanor a été fondée en 2014. Cela est mentionné dans le rapport annuel 2025, où |
| Q03 | fait simple | oui | False | True | 5.07 | La présidente de Vélanor est Hélène Marchais [source:7xhym97yt2vhs1du37em]. |
| Q04 | fait simple | oui | True | False | 6.44 | L'adresse du siège de Vélanor est : 12 quai de la Fosse, à Nantes. [source:726ap |
| Q05 | tableau | oui | True | True | 5.68 | Vélanor compte 412 salariés au 31 décembre 2025 [source:7xhym97yt2vhs1du37em]. |
| Q06 | tableau | oui | True | True | 6.45 | Le chiffre d'affaires du troisième trimestre 2025 a été de 14,2 M€ [source:7xhym |
| Q07 | tableau | oui | True | True | 8.43 | Le modèle Sèvre Trail a été produit en quantité de 15 400 unités en 2025. Cela e |
| Q08 | tableau | oui | True | False | 5.42 | Le prix public du modèle Erdre Cargo est de 4 290 € TTC. [source:726apry3o6tztlo |
| Q09 | tableau | oui | True | True | 5.64 | Sur le site de Cholet, 97 salariés travaillent dans la fabrication des cadres [s |
| Q10 | fait simple | oui | True | True | 5.48 | Les cadres sont fabriqués à partir d'aluminium recyclé à 82 %. [source:7xhym97yt |
| Q11 | fait simple | oui | True | True | 6.98 | Le taux de recyclage des batteries usagées collectées atteint 96 %, grâce au par |
| Q12 | tableau | oui | True | False | 5.66 | Les moteurs sont livrés par Motodrive Co., qui est installé en Taïwan. [source:7 |
| Q13 | tableau | oui | True | True | 6.47 | Vélanor a dégagé un résultat net de 3,1 M€ en 2025 [source:7xhym97yt2vhs1du37em] |
| Q14 | fait simple | oui | True | True | 6.23 | Le taux de retour sous garantie s'établit à 1,8 % des vélos vendus. [source:7xhy |
| Q15 | scan | non | True | False | 13.33 | Le prix unitaire des batteries n'est pas indiqué dans les documents disponibles. |
| Q16 | scan | non | True | False | 13.97 | Le délai de livraison prévu par le contrat avec Batterix n'est pas explicitement |
| Q17 | scan | non | True | True | 12.26 | Le plafond des pénalités de retard du contrat avec Batterix n'est pas mentionné  |
| Q18 | scan | non | False | False | 19.92 | Le contrat de Batterix n'indique pas explicitement un volume minimal annuel de b |
| Q19 | fait simple | oui | True | True | 5.4 | Les batteries doivent être stockées entre 10 °C et 25 °C. [source:ldl6ga0ifdo1o7 |
| Q20 | fait simple | oui | True | True | 6.7 | Karim Benali est responsable de la procédure de charge et de stockage des batter |
| Q21 | tableau | oui | True | True | 4.73 | Le local B2 est inspecté le premier lundi de chaque mois. [source:ldl6ga0ifdo1o7 |
| Q22 | fait simple | oui | True | True | 7.61 | Le prix du modèle Vilaine Compact, qui sera lancé en avril 2026, est de 2 490 €  |
| Q23 | fait simple | oui | True | True | 6.08 | La capacité prévue de l'usine de Saint-Nazaire est de 25 000 vélos par an. [sour |
| Q24 | tableau | oui | True | True | 30253.57 | Le stock de batteries BAT-48V-14Ah reste de 1 240 unités, comme indiqué dans le  |
| Q25 | fait simple | oui | True | True | 6.48 | La durée de garantie du cadre est de 7 ans. Cette information est indiquée dans  |
| Q26 | fait simple | oui | True | True | 6.99 | Le numéro de téléphone du service après-vente est le 02 40 00 12 34, disponible  |
| Q27 | fait simple | oui | True | True | 9.45 | La prime d'intéressement 2025 s'élève à 1 150 euros par salarié. Cette décision  |
| Q28 | anglais | oui | True | True | 5.1 | Batterix obtained an overall score of 87 out of 100 at the supplier audit. [sour |
| Q29 | anglais | oui | True | True | 7.44 | Le taux de cellules défectueuses mesuré chez Batterix lors de l'audit est de 0,3 |
| Q30 | multi-documents | non | False | True | 9.08 | Le délai contractuel exact de Batterix n'est pas mentionné dans les documents di |
| Q31 | multi-documents | non | True | True | 18.01 | Batterix a obtenu un score global de 87 sur 100 lors de son audit de qualité, ce |
| Q32 | multi-documents | oui | True | True | 11.77 | Vélanor vise un chiffre d'affaires de 55 M€ en 2026 [source:4zh3zdc0iprtxoeljajv |
| Q33 | audio | oui | False | True | 15.66 | La ligne d'assemblage numéro 3 de Nantes sera arrêtée pour maintenance du 2 au 6 |
| Q34 | audio | oui | True | True | 8.79 | Le directeur de production de Vélanor est Julien Moreau. Cette information est t |
| Q35 | piège | oui | True | - | 10.32 | Le chiffre d'affaires de Vélanor en 2022 n'est pas mentionné dans les documents  |
| Q36 | piège | oui | True | - | 24.19 | Le rôle de directeur financier de Vélanor n'est pas mentionné dans les documents |
| Q37 | piège | oui | True | - | 11.42 | Le document fourni ne contient aucune information sur les trottinettes électriqu |
| Q38 | piège | oui | True | - | 9.61 | Le salaire de Karim Benali n'est pas mentionné dans les documents fournis. Il es |
