# Banc open-notebook — gpu-vllm — 2026-11-09T10:56:14

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 27 |
| sur | 34 |
| refus_corrects | 4 |
| pieges | 4 |
| citation_bon_document | 24 |
| citation_bonne_page | 0 |
| citations_avec_page | 0 |
| juge_llm_oui | 0 |
| juge_llm_sur | 0 |
| erreurs | 0 |
| latence_p50_s | 1.86 |
| latence_p95_s | 4.28 |
| par_type | {'tableau': '9/10', 'fait simple': '13/13', 'scan': '0/4', 'anglais': '2/2', 'multi-documents': '1/3', 'audio': '2/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-open-notebook': 522, 'rag-open-notebook-surrealdb': 102, 'vllm-central': 6886, 'vllm-embed': 4978} |
| pic_ram_application_mo | 624 |
| vram | 15695 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | 54.2 |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | - | True | 5.86 | Le chiffre d'affaires de Vélanor pour l'année 2025 s'est établi à **48,6 M€**, c |
| Q02 | fait simple | oui | - | True | 2.21 | Vélanor a été fondée en 2014 à Nantes [source:4qiglhjszgt5pb08ws7p]. |
| Q03 | fait simple | oui | - | True | 1.43 | La présidente de Vélanor est Hélène Marchais. Elle dirige l'entreprise depuis 20 |
| Q04 | fait simple | oui | - | True | 1.39 | Le siège de Vélanor est situé au 12 quai de la Fosse, à Nantes [source:4qiglhjsz |
| Q05 | tableau | oui | - | True | 3.82 | Au 31 décembre 2025, Vélanor comptait 412 salariés [source:4qiglhjszgt5pb08ws7p] |
| Q06 | tableau | oui | - | True | 2.43 | Le chiffre d'affaires du troisième trimestre 2025 était de **14,2 M€**, ce qui r |
| Q07 | tableau | oui | - | True | 1.62 | Le modèle Sèvre Trail, qui est utilisé pour le VTT, a vu **15 400 unités** produ |
| Q08 | tableau | oui | - | True | 1.38 | Le prix public du modèle Erdre Cargo est de 4 290 € TTC [source:4qiglhjszgt5pb08 |
| Q09 | tableau | oui | - | True | 1.38 | Il y a 97 salariés travaillent sur le site de Cholet pour la fabrication des cad |
| Q10 | fait simple | oui | - | True | 1.27 | La fabrication des cadres utilise 82 % d'aluminium recyclé [source:4qiglhjszgt5p |
| Q11 | fait simple | oui | - | True | 1.48 | Le taux de recyclage des batteries usagées atteint 96 % grâce au partenariat ave |
| Q12 | tableau | oui | - | False | 1.41 | Le fournisseur qui livre les moteurs est Motodrive Co., et celui-ci est installé |
| Q13 | tableau | oui | - | True | 1.41 | Vélanor a dégagé un résultat net de 3,1 M€ en 2025 [source:4qiglhjszgt5pb08ws7p] |
| Q14 | fait simple | oui | - | True | 1.58 | Le taux de retour sous garantie de Vélanor s'établit à 1,8 % des vélos vendus en |
| Q15 | scan | non | - | False | 4.07 | Je suis désolé, mais les documents dont je dispose ne précisent pas le prix unit |
| Q16 | scan | non | - | False | 2.9 | Je n'ai pas trouvé de mention du délai de livraison prévu dans le contrat Batter |
| Q17 | scan | non | - | True | 4.28 | Je suis désolé, mais les documents contextuels que j'ai à ma disposition ne cont |
| Q18 | scan | non | - | False | 5.0 | Je suis désolé, mais les documents contextuels fournis ne contiennent aucune inf |
| Q19 | fait simple | oui | - | True | 2.54 | Les batteries doivent être stockées entre $10 \text{ °C}$ et $25 \text{ °C}$ dan |
| Q20 | fait simple | oui | - | True | 2.35 | La personne responsable de la procédure de charge et de stockage des batteries e |
| Q21 | tableau | non | - | True | 3.0 | Je suis désolé, mais les documents dont je dispose ne mentionnent pas la fréquen |
| Q22 | fait simple | oui | - | False | 1.81 | Le prix public du Vilaine Compact, qui est un vélo pliant électrique, est de 2 4 |
| Q23 | fait simple | oui | - | True | 1.68 | L'usine de Saint-Nazaire, prévue pour son ouverture en septembre 2026, aura une  |
| Q24 | tableau | oui | - | True | 2.01 | Le stock actuel pour la référence **BAT-48V-14Ah** (Batterie 48 V 14 Ah) est de  |
| Q25 | fait simple | oui | - | False | 1.16 | La garantie pour le cadre est de 7 ans [dhmo3d0okrig4gqorpvf]. |
| Q26 | fait simple | oui | - | False | 1.63 | Le numéro de téléphone du service après-vente est le 02 40 00 12 34, disponible  |
| Q27 | fait simple | oui | - | False | 1.68 | La prime d'intéressement pour 2025 est fixée à 1 150 euros par salarié, et elle  |
| Q28 | anglais | oui | - | True | 1.61 | Batterix GmbH obtained an overall score of 87 out of 100 during the Supplier Qua |
| Q29 | anglais | oui | - | True | 1.5 | Le taux de défaut des cellules mesuré chez Batterix GmbH lors de l'audit était d |
| Q30 | multi-documents | non | - | True | 4.02 | Pour répondre à votre question, il faut distinguer le délai contractuel (qui n'e |
| Q31 | multi-documents | non | - | True | 3.19 | L'audit de qualité fournisseur mené auprès de Batterix GmbH a abouti à un score  |
| Q32 | multi-documents | oui | - | False | 2.13 | Vélanor vise un chiffre d'affaires de 55 M€ en 2026 [strategie-2026.pptx]. Conce |
| Q33 | audio | oui | - | True | 2.12 | La ligne d'assemblage numéro 3 de Nantes sera arrêtée pour maintenance du 2 au 6 |
| Q34 | audio | oui | - | False | 1.24 | Le directeur de production de Vélanor est Julien Moreau [93hbou93w5obpl49b0lv]. |
| Q35 | piège | oui | - | - | 2.0 | Je suis désolé, mais les documents de contexte que j'ai accès ne contiennent auc |
| Q36 | piège | oui | - | - | 4.0 | Je suis désolé, mais les documents de contexte que j'ai accès ne mentionnent pas |
| Q37 | piège | oui | - | - | 1.86 | Je suis désolé, mais les documents dont je dispose ne contiennent aucune informa |
| Q38 | piège | oui | - | - | 2.04 | Je suis désolé, mais les documents dont je dispose ne contiennent aucune informa |
