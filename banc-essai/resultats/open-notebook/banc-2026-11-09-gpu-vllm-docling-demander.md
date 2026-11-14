# Banc open-notebook — gpu-vllm-docling-demander — 2026-11-09T11:10:53

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
| juge_llm_oui | 0 |
| juge_llm_sur | 0 |
| erreurs | 0 |
| latence_p50_s | 7.7 |
| latence_p95_s | 13.35 |
| par_type | {'tableau': '10/10', 'fait simple': '13/13', 'scan': '0/4', 'anglais': '2/2', 'multi-documents': '1/3', 'audio': '2/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-open-notebook': 7118, 'rag-open-notebook-surrealdb': 92, 'vllm-central': 6740, 'vllm-embed': 4518} |
| pic_ram_application_mo | 7210 |
| vram | 15684 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | None |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | - | True | 15.4 | Le chiffre d'affaires de Vélanor pour l'année 2025 s'est établi à **48,6 M€**, c |
| Q02 | fait simple | oui | - | True | 5.39 | Vélanor a été fondée en 2014 à Nantes [source:81ggj1mrclmyi21pjq27]. |
| Q03 | fait simple | oui | - | True | 6.26 | La présidente de Vélanor est Hélène Marchais [source:81ggj1mrclmyi21pjq27]. Elle |
| Q04 | fait simple | oui | - | True | 5.47 | L'adresse du siège de Vélanor est le **12 quai de la Fosse à Nantes** [source:81 |
| Q05 | tableau | oui | - | True | 4.44 | Au 31 décembre 2025, Vélanor comptait 412 salariés [source:81ggj1mrclmyi21pjq27] |
| Q06 | tableau | oui | - | True | 7.68 | Le chiffre d'affaires pour le troisième trimestre (T3) 2025 a été de **14,2 M€** |
| Q07 | tableau | oui | - | True | 10.94 | Le modèle Sèvre Trail a produit **15 400 unités** en 2025 [source:81ggj1mrclmyi2 |
| Q08 | tableau | oui | - | True | 6.82 | Le prix public TTC du modèle Erdre Cargo est de **4 290 €** [source:81ggj1mrclmy |
| Q09 | tableau | oui | - | True | 4.78 | Au 31/12/2025, il y avait **97** salariés travaillant sur le site de Cholet pour |
| Q10 | fait simple | oui | - | True | 7.28 | La part d'aluminium recyclé dans les cadres est de **82 %** [source:81ggj1mrclmy |
| Q11 | fait simple | oui | - | True | 8.68 | Le taux de recyclage des batteries usagées collectées atteint **96 %**, ceci grâ |
| Q12 | tableau | oui | - | True | 5.88 | Le fournisseur qui livre les moteurs est **Motodrive Co.**, et cette entreprise  |
| Q13 | tableau | oui | - | True | 11.51 | Le résultat net que Vélanor a dégagé en 2025 est de **3,1 M€** [source:81ggj1mrc |
| Q14 | fait simple | oui | - | True | 9.23 | Le taux de retour sous garantie s'élève à **1,8 %** des vélos vendus [source:81g |
| Q15 | scan | non | - | False | 8.23 | Les documents consultés ne mentionnent pas le prix unitaire des batteries prévu  |
| Q16 | scan | non | - | False | 5.5 | Le délai moyen constaté pour la livraison des batteries de Batterix GmbH est de  |
| Q17 | scan | non | - | False | 11.12 | Je n'ai trouvé aucune information concernant le plafond des pénalités de retard  |
| Q18 | scan | non | - | False | 5.71 | Je n'ai trouvé aucune information spécifique dans les documents fournis concerna |
| Q19 | fait simple | oui | - | True | 5.86 | La température recommandée pour le stockage des batteries se situe **entre 10 °C |
| Q20 | fait simple | oui | - | True | 14.04 | Le responsable de la procédure de charge et de stockage des batteries est **Kari |
| Q21 | tableau | oui | - | True | 9.03 | Le local B2 doit être inspecté **le premier lundi de chaque mois** [source:vh2m7 |
| Q22 | fait simple | oui | - | True | 4.27 | Le prix public du Vilaine Compact, qui est un vélo pliant électrique, est de **2 |
| Q23 | fait simple | oui | - | True | 8.07 | La capacité prévue de l'usine de Saint-Nazaire est de **25 000 vélos par an** [s |
| Q24 | tableau | oui | - | True | 7.83 | Il reste **1240** batteries BAT-48V-14Ah en stock à l'entrepôt de Nantes [source |
| Q25 | fait simple | oui | - | True | 7.8 | La durée de garantie pour le cadre est de **7 ans** [source:zfw2v0083daeckkaxloq |
| Q26 | fait simple | oui | - | True | 7.01 | Le numéro de téléphone du service après-vente est le **02 40 00 12 34** [source: |
| Q27 | fait simple | oui | - | True | 13.35 | Selon les documents consultés, un document fictif intitulé « Compte rendu de la  |
| Q28 | anglais | oui | - | True | 5.77 | Batterix obtained an overall score of **87 out of 100** during the supplier qual |
| Q29 | anglais | oui | - | True | 5.48 | Le taux de cellules défectueuses mesuré chez Batterix lors de l'audit était de * |
| Q30 | multi-documents | non | - | True | 8.98 | D'après les documents disponibles, voici les informations concernant les délais  |
| Q31 | multi-documents | non | - | True | 10.74 | Batterix a obtenu un score global de **87 sur 100** lors de l'audit de qualité f |
| Q32 | multi-documents | oui | - | True | 6.81 | Vélanor vise un chiffre d'affaires de **55 M€ en 2026** [source:81ggj1mrclmyi21p |
| Q33 | audio | oui | - | True | 8.94 | La ligne d'assemblage qui sera arrêtée pour maintenance en mars 2026 est la **li |
| Q34 | audio | oui | - | True | 5.17 | Le directeur de production de Vélanor est Julien Moreau [source:z7jmrzx6em1n3jzr |
| Q35 | piège | oui | - | - | 7.83 | Je n'ai pas trouvé d'information concernant le chiffre d'affaires de Vélanor pou |
| Q36 | piège | oui | - | - | 7.7 | Les documents consultés ne précisent pas le nom du directeur financier de Vélano |
| Q37 | piège | oui | - | - | 11.93 | Les documents fournis ne contiennent aucune information concernant le nombre de  |
| Q38 | piège | oui | - | - | 7.76 | Je n'ai trouvé aucune information concernant le salaire de Karim Benali dans les |
