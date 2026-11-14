# Banc open-notebook — docling-qwen-fullcontent-ctx6144 — 2026-11-08T17:30:05

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 28 |
| sur | 34 |
| refus_corrects | 4 |
| pieges | 4 |
| citation_bon_document | 30 |
| citation_bonne_page | 0 |
| citations_avec_page | 0 |
| juge_llm_oui | 35 |
| juge_llm_sur | 38 |
| erreurs | 0 |
| latence_p50_s | 91.82 |
| latence_p95_s | 114.13 |
| par_type | {'tableau': '10/10', 'fait simple': '13/13', 'scan': '0/4', 'anglais': '2/2', 'multi-documents': '1/3', 'audio': '2/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-open-notebook': 2442, 'rag-open-notebook-surrealdb': 113, 'rag-socle-ollama': 10177} |
| pic_ram_application_mo | 2555 |
| vram | sans objet (aucun GPU NVIDIA, socle CPU) |
| indexation_s | None |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | True | True | 93.22 | Le chiffre d'affaires de Vélanor en 2025 s'élève à 48,6 millions d'euros [source |
| Q02 | fait simple | oui | True | True | 88.83 | Vélanor a été fondée en 2014. [source:t5pnatx1ejz177x6kjgd] |
| Q03 | fait simple | oui | False | True | 89.14 | La présidente de Vélanor est Hélène Marchais [source:t5pnatx1ejz177x6kjgd]. |
| Q04 | fait simple | oui | True | True | 91.98 | L'adresse du siège de Vélanor est : 12 quai de la Fosse, à Nantes. [source:t5pna |
| Q05 | tableau | oui | True | True | 87.99 | Vélanor compte 412 salariés au 31 décembre 2025 [source:t5pnatx1ejz177x6kjgd]. |
| Q06 | tableau | oui | True | True | 92.26 | Le chiffre d'affaires du troisième trimestre 2025 a été de 14,2 M€. Cela représe |
| Q07 | tableau | oui | True | True | 91.82 | En 2025, 15 400 unités du modèle Sèvre Trail ont été produites. Cette informatio |
| Q08 | tableau | oui | True | True | 87.53 | Le prix public du modèle Erdre Cargo est de 4 290 € TTC. [source:t5pnatx1ejz177x |
| Q09 | tableau | oui | True | True | 88.38 | Sur le site de Cholet, 97 salariés travaillent dans la fabrication des cadres [s |
| Q10 | fait simple | oui | True | True | 87.46 | Les cadres sont fabriqués à partir d'aluminium recyclé à 82 %. [source:t5pnatx1e |
| Q11 | fait simple | oui | True | True | 90.37 | Le taux de recyclage des batteries usagées collectées atteint 96 %, grâce au par |
| Q12 | tableau | oui | True | False | 87.97 | Les moteurs sont livrés par Motodrive Co., qui est installé en Taïwan. [source:7 |
| Q13 | tableau | oui | True | True | 89.47 | En 2025, Vélanor a dégagé un résultat net de 3,1 M€ [source:t5pnatx1ejz177x6kjgd |
| Q14 | fait simple | oui | True | True | 88.01 | Le taux de retour sous garantie s'établit à 1,8 % des vélos vendus [source:t5pna |
| Q15 | scan | non | True | False | 109.66 | Le prix unitaire des batteries n'est pas indiqué dans les documents fournis. Bie |
| Q16 | scan | non | True | False | 106.96 | Le délai de livraison prévu par le contrat avec Batterix n'est pas explicitement |
| Q17 | scan | non | True | True | 102.22 | Le plafond des pénalités de retard du contrat avec Batterix n'est pas mentionné  |
| Q18 | scan | non | False | False | 114.24 | Le contrat avec Batterix GmbH ne précise pas explicitement le volume minimal ann |
| Q19 | fait simple | oui | True | True | 87.61 | Les batteries doivent être stockées entre 10 °C et 25 °C. [source:xetpyxai5eddgg |
| Q20 | fait simple | oui | True | True | 88.49 | Karim Benali, responsable HSE, est responsable de la procédure de charge et de s |
| Q21 | tableau | oui | True | True | 86.86 | Le local B2 est inspecté le premier lundi de chaque mois. [source:xetpyxai5eddgg |
| Q22 | fait simple | oui | True | True | 89.7 | Le prix public du modèle Vilaine Compact, qui est un vélo pliant électrique, est |
| Q23 | fait simple | oui | True | True | 90.56 | La capacité prévue de l'usine de Saint-Nazaire est de 25 000 vélos par an. Cette |
| Q24 | tableau | oui | True | True | 102.82 | Le stock de batteries BAT-48V-14Ah reste de 1 240 unités, comme indiqué dans le  |
| Q25 | fait simple | oui | True | True | 88.43 | La durée de garantie du cadre est de 7 ans. Cette information est mentionnée dan |
| Q26 | fait simple | oui | True | True | 90.48 | Le numéro de téléphone du service après-vente est 02 40 00 12 34, disponible du  |
| Q27 | fait simple | oui | True | True | 86.93 | La prime d'intéressement 2025 est de 1 150 euros par salarié. [source:rx0s8mci0v |
| Q28 | anglais | oui | True | True | 95.27 | Batterix obtained an overall score of 87 out of 100 at the supplier audit. [sour |
| Q29 | anglais | oui | True | True | 93.48 | Le taux de cellules défectueuses mesuré chez Batterix lors de l'audit est de 0,3 |
| Q30 | multi-documents | non | True | True | 114.13 | Le délai contractuel de Batterix n'est pas explicitement mentionné dans les docu |
| Q31 | multi-documents | non | False | True | 108.56 | Batterix a obtenu un score global de 87 sur 100 lors de l'audit qualité réalisé  |
| Q32 | multi-documents | oui | True | True | 103.55 | Vélanor vise un chiffre d'affaires de 55 M€ en 2026 [source:x5glza818yr0zev85chw |
| Q33 | audio | oui | True | True | 148.0 | Il n'y a pas d'information dans le contexte concernant une interruption de produ |
| Q34 | audio | oui | True | True | 100.15 | Le directeur de production de Vélanor est Julien Moreau. Cette information est t |
| Q35 | piège | oui | True | - | 103.77 | Le chiffre d'affaires de Vélanor en 2022 n'est pas mentionné dans les documents  |
| Q36 | piège | oui | True | - | 106.39 | Le rôle du directeur financier de Vélanor n'est pas mentionné dans les documents |
| Q37 | piège | oui | True | - | 101.09 | Il n’y a aucune mention dans les documents fournis sur la vente de trottinettes  |
| Q38 | piège | oui | True | - | 97.45 | Le salaire de Karim Benali n'est pas mentionné dans les documents fournis. Il es |
