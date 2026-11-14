# Banc open-notebook — defaut-qwen-fullcontent — 2026-11-08T13:56:43

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 25 |
| sur | 34 |
| refus_corrects | 4 |
| pieges | 4 |
| citation_bon_document | 26 |
| citation_bonne_page | 0 |
| citations_avec_page | 0 |
| juge_llm_oui | 32 |
| juge_llm_sur | 38 |
| erreurs | 0 |
| latence_p50_s | 10.81 |
| latence_p95_s | 23.83 |
| par_type | {'tableau': '9/10', 'fait simple': '13/13', 'scan': '0/4', 'anglais': '2/2', 'multi-documents': '1/3', 'audio': '0/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-open-notebook': 798, 'rag-open-notebook-surrealdb': 178, 'rag-socle-ollama': 9994} |
| pic_ram_application_mo | 976 |
| vram | sans objet (aucun GPU NVIDIA, socle CPU) |
| indexation_s | 70.0 |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | True | True | 97.82 | Le chiffre d'affaires de Vélanor en 2025 s'élève à 48,6 M€ [source:s5ztzcy9ykasp |
| Q02 | fait simple | oui | True | True | 6.88 | Vélanor a été fondée en 2014. [source:s5ztzcy9ykaspbznzujy] |
| Q03 | fait simple | oui | False | True | 5.88 | La présidente de Vélanor est Hélène Marchais [source:s5ztzcy9ykaspbznzujy]. |
| Q04 | fait simple | oui | True | True | 10.81 | L'adresse du siège de Vélanor est le 12 quai de la Fosse, à Nantes. [source:s5zt |
| Q05 | tableau | oui | True | True | 8.34 | Au 31 décembre 2025, Vélanor compte 412 salariés [source:s5ztzcy9ykaspbznzujy]. |
| Q06 | tableau | oui | True | True | 8.99 | Le chiffre d'affaires du troisième trimestre 2025 a été de 14,2 M€. [source:s5zt |
| Q07 | tableau | oui | True | True | 16.46 | En 2025, 15 400 unités du modèle Sèvre Trail ont été produites. Cela est indiqué |
| Q08 | tableau | oui | True | True | 6.47 | Le prix public du modèle Erdre Cargo est de 4 290 € TTC. [source:s5ztzcy9ykaspbz |
| Q09 | tableau | oui | True | False | 8.07 | Sur le site de Cholet, 97 salariés travaillent dans la fabrication des cadres. [ |
| Q10 | fait simple | oui | True | True | 6.72 | Les cadres sont fabriqués à partir d'aluminium recyclé à 82 %. [source:s5ztzcy9y |
| Q11 | fait simple | oui | True | True | 8.24 | Le taux de recyclage des batteries usagées collectées atteint 96 %, grâce au par |
| Q12 | tableau | oui | True | False | 6.89 | Le fournisseur des moteurs est Motodrive Co., installé au Taïwan [source:gwyzl6w |
| Q13 | tableau | oui | True | True | 11.53 | Vélanor a dégagé un résultat net de 3,1 M€ en 2025 [source:s5ztzcy9ykaspbznzujy] |
| Q14 | fait simple | oui | True | True | 7.13 | Le taux de retour sous garantie s'établit à 1,8 % des vélos vendus. [source:s5zt |
| Q15 | scan | non | True | False | 23.46 | Le prix unitaire des batteries n'est pas mentionné dans les documents disponible |
| Q16 | scan | non | False | False | 19.57 | Le document qui mentionne les délais des fournisseurs, incluant Batterix, est le |
| Q17 | scan | non | True | False | 20.0 | Le plafond des pénalités de retard n'est pas mentionné dans les documents fourni |
| Q18 | scan | non | False | False | 22.95 | Le contrat avec Batterix ne précise pas un volume minimal annuel de batteries. L |
| Q19 | fait simple | oui | True | True | 6.43 | Les batteries doivent être stockées entre 10 °C et 25 °C. [source:kclolfk6c0keog |
| Q20 | fait simple | oui | True | True | 7.43 | Karim Benali, responsable HSE, est responsable de la procédure de charge et de s |
| Q21 | tableau | non | False | True | 14.67 | Le document contexte ne mentionne pas explicitement la fréquence d'inspection du |
| Q22 | fait simple | oui | True | True | 9.7 | Le prix public du Vilaine Compact, le nouveau modèle de vélo pliant électrique,  |
| Q23 | fait simple | oui | True | True | 7.81 | La capacité prévue de l'usine de Saint-Nazaire est de 25 000 vélos par an. [sour |
| Q24 | tableau | oui | True | True | 19.27 | Le stock de batteries BAT-48V-14Ah reste de 1240 unités, selon les données du fi |
| Q25 | fait simple | oui | True | False | 7.81 | La durée de garantie du cadre est de 7 ans. Cette information est mentionnée dan |
| Q26 | fait simple | oui | True | True | 10.52 | Le numéro de téléphone du service après-vente est 02 40 00 12 34. [source:fklivo |
| Q27 | fait simple | oui | True | True | 7.73 | La prime d'intéressement 2025 s'élève à 1 150 euros par salarié [source:kba5tul1 |
| Q28 | anglais | oui | True | True | 6.79 | Batterix obtained an overall score of 87 out of 100 at the supplier audit. [sour |
| Q29 | anglais | oui | True | True | 13.56 | Le taux de cellules défectueuses mesuré chez Batterix lors de l'audit est de 0,3 |
| Q30 | multi-documents | non | True | True | 13.57 | Le délai contractuel de Batterix n'est pas explicitement mentionné dans les docu |
| Q31 | multi-documents | non | False | True | 27.37 | Le score obtenu par Batterix à l'audit est de 87 sur 100 [source:e6mm5bgdfkl45d1 |
| Q32 | multi-documents | oui | True | True | 14.7 | Vélanor vise un chiffre d'affaires de 55 M€ en 2026 [source:lkudh8prnow82qm2et7x |
| Q33 | audio | non | True | True | 23.83 | Aucune information n'est disponible dans le contexte concernant une ligne d'asse |
| Q34 | audio | non | False | False | 16.48 | Le rôle de directeur de production de Vélanor n'est pas mentionné dans les docum |
| Q35 | piège | oui | True | - | 13.65 | Le chiffre d'affaires de Vélanor en 2022 n'est pas mentionné dans les documents  |
| Q36 | piège | oui | True | - | 17.09 | Le rôle du directeur financier de Vélanor n'est pas mentionné dans les documents |
| Q37 | piège | oui | True | - | 14.61 | Il n'est pas indiqué dans les documents que Vélanor a vendu de trottinettes élec |
| Q38 | piège | oui | True | - | 13.45 | Le salaire de Karim Benali n'est pas mentionné dans les documents fournis. Il es |
