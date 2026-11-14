# Banc open-notebook — docling-qwen-fullcontent — 2026-11-08T14:10:21

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
| juge_llm_oui | 35 |
| juge_llm_sur | 38 |
| erreurs | 0 |
| latence_p50_s | 9.05 |
| latence_p95_s | 23.79 |
| par_type | {'tableau': '10/10', 'fait simple': '13/13', 'scan': '0/4', 'anglais': '2/2', 'multi-documents': '1/3', 'audio': '2/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-open-notebook': 3623, 'rag-open-notebook-surrealdb': 142, 'rag-socle-ollama': 8325} |
| pic_ram_application_mo | 3765 |
| vram | sans objet (aucun GPU NVIDIA, socle CPU) |
| indexation_s | 125.6 |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | True | True | 80.27 | Le chiffre d'affaires de Vélanor en 2025 s'élevait à 48,6 M€ [source:t5pnatx1ejz |
| Q02 | fait simple | oui | True | True | 6.1 | Vélanor a été fondée en 2014 [source:t5pnatx1ejz177x6kjgd]. |
| Q03 | fait simple | oui | False | True | 5.7 | La présidente de Vélanor est Hélène Marchais [source:t5pnatx1ejz177x6kjgd]. |
| Q04 | fait simple | oui | True | True | 7.18 | L'adresse du siège de Vélanor est le 12 quai de la Fosse, à Nantes. [source:t5pn |
| Q05 | tableau | oui | True | True | 7.17 | Vélanor compte 412 salariés au 31 décembre 2025 [source:t5pnatx1ejz177x6kjgd]. |
| Q06 | tableau | oui | True | True | 7.86 | Le chiffre d'affaires du troisième trimestre 2025 a été de 14,2 M€ [source:t5pna |
| Q07 | tableau | oui | True | True | 13.88 | En 2025, 15 400 unités du modèle Sèvre Trail ont été produites. Cette informatio |
| Q08 | tableau | oui | True | True | 6.47 | Le prix public du modèle Erdre Cargo est de 4 290 € TTC. [source:t5pnatx1ejz177x |
| Q09 | tableau | oui | True | False | 6.66 | Sur le site de Cholet, 97 salariés travaillent dans la fabrication des cadres [s |
| Q10 | fait simple | oui | True | True | 6.55 | Les cadres sont fabriqués à partir d'aluminium recyclé à 82 %. [source:t5pnatx1e |
| Q11 | fait simple | oui | True | True | 10.96 | Le taux de recyclage des batteries usagées collectées atteint 96 %, grâce au par |
| Q12 | tableau | oui | True | False | 6.44 | Les moteurs sont livrés par Motodrive Co., qui est installé en Taïwan [source:3i |
| Q13 | tableau | oui | True | True | 7.11 | Vélanor a dégagé un résultat net de 3,1 M€ en 2025 [source:t5pnatx1ejz177x6kjgd] |
| Q14 | fait simple | oui | True | True | 6.55 | Le taux de retour sous garantie s'établit à 1,8 % des vélos vendus. [source:t5pn |
| Q15 | scan | non | True | False | 17.69 | Le prix unitaire des batteries n'est pas mentionné dans les documents fournis. L |
| Q16 | scan | non | True | False | 22.21 | Le délai de livraison prévu par le contrat avec Batterix n'est pas explicitement |
| Q17 | scan | non | True | False | 20.11 | Le plafond des pénalités de retard du contrat avec Batterix n'est pas mentionné  |
| Q18 | scan | non | False | False | 28.22 | Le contrat avec Batterix ne précise pas explicitement un volume minimal annuel d |
| Q19 | fait simple | oui | True | True | 9.15 | Les batteries doivent être stockées entre 10 °C et 25 °C. [source:xetpyxai5eddgg |
| Q20 | fait simple | oui | True | True | 7.55 | Karim Benali est responsable de la procédure de charge et de stockage des batter |
| Q21 | tableau | oui | True | True | 5.66 | Le local B2 est inspecté le premier lundi de chaque mois. [source:xetpyxai5eddgg |
| Q22 | fait simple | oui | True | True | 19.57 | Le prix du modèle Vilaine Compact n'est pas explicitement mentionné dans les doc |
| Q23 | fait simple | oui | True | True | 7.03 | La capacité prévue de l'usine de Saint-Nazaire est de 25 000 vélos par an. [sour |
| Q24 | tableau | oui | True | True | 18.45 | Le stock de batteries BAT-48V-14Ah reste de 1 240 unités, selon les données du f |
| Q25 | fait simple | oui | True | True | 6.65 | La durée de garantie du cadre est de 7 ans. Cette information est mentionnée dan |
| Q26 | fait simple | oui | True | True | 6.89 | Le numéro de téléphone du service après-vente est le 02 40 00 12 34. [source:isk |
| Q27 | fait simple | oui | True | True | 6.92 | La prime d'intéressement 2025 est de 1 150 euros par salarié. [source:rx0s8mci0v |
| Q28 | anglais | oui | True | True | 9.5 | Batterix obtained an overall score of 87 out of 100 at the supplier audit. [sour |
| Q29 | anglais | oui | True | True | 9.14 | Le taux de cellules défectueuses mesuré chez Batterix lors de l'audit est de 0,3 |
| Q30 | multi-documents | non | True | True | 11.92 | Le délai contractuel de Batterix n'est pas explicitement mentionné dans les docu |
| Q31 | multi-documents | non | False | True | 22.45 | Le score obtenu par Batterix lors de l'audit est de 87 sur 100 [source:fktzzi8od |
| Q32 | multi-documents | oui | True | True | 13.44 | Vélanor vise un chiffre d'affaires de 55 M€ en 2026 [source:x5glza818yr0zev85chw |
| Q33 | audio | oui | True | True | 11.94 | La ligne d'assemblage numéro 3 de Nantes sera arrêtée du 2 au 6 mars 2026 pour m |
| Q34 | audio | oui | True | True | 8.8 | Le directeur de production de Vélanor est Julien Moreau. Cette information est t |
| Q35 | piège | oui | True | - | 15.51 | Le chiffre d'affaires de Vélanor en 2022 n'est pas mentionné dans les documents  |
| Q36 | piège | oui | True | - | 23.79 | Le rôle du directeur financier de Vélanor n'est pas mentionné dans les documents |
| Q37 | piège | oui | True | - | 16.18 | Vélanor n’a pas vendu de trottinettes électriques en 2025. Le rapport annuel 202 |
| Q38 | piège | oui | True | - | 9.05 | Le salaire de Karim Benali n'est pas mentionné dans les documents fournis. Il es |
