# Banc open-notebook — gpu-vllm-demander — 2026-11-09T10:59:27

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 27 |
| sur | 34 |
| refus_corrects | 3 |
| pieges | 4 |
| citation_bon_document | 29 |
| citation_bonne_page | 0 |
| citations_avec_page | 0 |
| juge_llm_oui | 0 |
| juge_llm_sur | 0 |
| erreurs | 0 |
| latence_p50_s | 7.05 |
| latence_p95_s | 15.39 |
| par_type | {'tableau': '9/10', 'fait simple': '13/13', 'scan': '0/4', 'anglais': '2/2', 'multi-documents': '1/3', 'audio': '2/2', 'piège': '3/4'} |
| pic_ram_mo | {'rag-open-notebook': 556, 'rag-open-notebook-surrealdb': 105, 'vllm-central': 7062, 'vllm-embed': 4976} |
| pic_ram_application_mo | 661 |
| vram | 15695 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | None |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | - | True | 15.39 | Le chiffre d'affaires de Vélanor pour l'année 2025 est de **48,6 M€** [source:4q |
| Q02 | fait simple | oui | - | True | 3.92 | Vélanor a été fondée en 2014 à Nantes [source:4qiglhjszgt5pb08ws7p]. |
| Q03 | fait simple | oui | - | True | 5.7 | La présidente de Vélanor est Hélène Marchais, qui dirige l'entreprise depuis 201 |
| Q04 | fait simple | oui | - | True | 4.24 | Le siège de Vélanor SAS est situé au **12 quai de la Fosse à Nantes** [source:4q |
| Q05 | tableau | oui | - | True | 15.55 | Au 31 décembre 2025, Vélanor comptait **412 salariés** [source:4qiglhjszgt5pb08w |
| Q06 | tableau | oui | - | True | 6.92 | Le chiffre d'affaires du troisième trimestre 2025 était de **14,2 M€**, ce monta |
| Q07 | tableau | oui | - | True | 9.56 | Le modèle Sèvre Trail a produit **15 400 unités** en 2025 [source:4qiglhjszgt5pb |
| Q08 | tableau | oui | - | True | 3.81 | Le prix public TTC du modèle Erdre Cargo est de **4 290 €** [source:4qiglhjszgt5 |
| Q09 | tableau | oui | - | True | 13.39 | Au 31 décembre 2025, il y avait **97 salariés** sur le site de Cholet, qui est d |
| Q10 | fait simple | oui | - | True | 4.51 | La part d'aluminium recyclé dans les cadres est de **82 %** [source:4qiglhjszgt5 |
| Q11 | fait simple | oui | - | True | 4.9 | Selon les informations disponibles, le taux de recyclage des batteries usagées c |
| Q12 | tableau | oui | - | False | 4.96 | Le fournisseur qui livre les moteurs est **Motodrive Co.**, et il est installé à |
| Q13 | tableau | oui | - | True | 9.31 | Vélanor a dégagé un résultat net de **3,1 M€** en 2025 [source:4qiglhjszgt5pb08w |
| Q14 | fait simple | oui | - | True | 8.76 | Le taux de retour sous garantie s'établit à **1,8 %** des vélos vendus [source:4 |
| Q15 | scan | non | - | False | 6.75 | Les documents fournis indiquent que **Batterix GmbH** est bien le fournisseur de |
| Q16 | scan | non | - | False | 6.68 | Le document consulté ne spécifie pas de délai de livraison général pour le contr |
| Q17 | scan | non | - | False | 8.95 | Je n'ai trouvé aucune information dans les documents fournis concernant le plafo |
| Q18 | scan | non | - | False | 10.35 | Les documents fournis ne contiennent aucune information spécifiant un volume min |
| Q19 | fait simple | oui | - | True | 11.91 | La température recommandée pour le stockage des batteries se situe **entre 10 °C |
| Q20 | fait simple | oui | - | True | 18.77 | La responsabilité de la procédure de charge et de stockage des batteries est ass |
| Q21 | tableau | non | - | True | 6.02 | Les documents consultés ne spécifient pas la fréquence à laquelle le local B2 es |
| Q22 | fait simple | oui | - | True | 5.93 | Le prix public du Vilaine Compact, qui est un vélo pliant électrique, est de **2 |
| Q23 | fait simple | oui | - | True | 9.2 | La capacité prévue de l'usine de Saint-Nazaire est de **25 000 vélos par an**, a |
| Q24 | tableau | oui | - | True | 7.87 | Il reste **1240** unités de la batterie BAT-48V-14Ah.  Ce stock est **inférieur  |
| Q25 | fait simple | oui | - | True | 4.14 | La durée de garantie du cadre est de **7 ans** [source:dhmo3d0okrig4gqorpvf]. Pa |
| Q26 | fait simple | oui | - | True | 5.07 | Le numéro de téléphone du service après-vente est le **02 40 00 12 34**, et il e |
| Q27 | fait simple | oui | - | True | 9.13 | Selon les documents consultés, le montant de la prime d'intéressement pour 2025  |
| Q28 | anglais | oui | - | True | 5.93 | Batterix obtained an overall score of **87 out of 100** during the supplier qual |
| Q29 | anglais | oui | - | True | 4.5 | Le taux de cellules défectueuses mesuré chez Batterix lors de l'audit était de * |
| Q30 | multi-documents | non | - | True | 7.05 | Le délai de livraison contractuel pour les batteries Batterix n'est pas spécifié |
| Q31 | multi-documents | non | - | True | 10.73 | Le score obtenu par Batterix lors de l'audit est de **87/100** [source:2dd81uwuu |
| Q32 | multi-documents | oui | - | True | 11.93 | Vélanor vise un chiffre d'affaires de **55 M€** en 2026 [source:b3z7vu8hvgd73sab |
| Q33 | audio | oui | - | True | 7.31 | La ligne d'assemblage qui sera arrêtée pour maintenance en mars 2026 est la **li |
| Q34 | audio | oui | - | True | 4.04 | Le directeur de production chez Vélanor est Julien Moreau [source:93hbou93w5obpl |
| Q35 | piège | oui | - | - | 9.98 | Les documents disponibles ne contiennent aucune information concernant le chiffr |
| Q36 | piège | oui | - | - | 8.11 | Les documents fournis ne mentionnent pas le nom du directeur financier de Vélano |
| Q37 | piège | non | - | - | 8.67 | Vélanor n'a pas spécifié le nombre exact de trottinettes électriques vendues en  |
| Q38 | piège | oui | - | - | 7.01 | Je n'ai trouvé aucune information concernant le salaire de Karim Benali dans les |
