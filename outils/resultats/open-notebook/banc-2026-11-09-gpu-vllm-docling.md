# Banc open-notebook — gpu-vllm-docling — 2026-11-09T11:08:04

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 28 |
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
| latence_p95_s | 4.59 |
| par_type | {'tableau': '10/10', 'fait simple': '13/13', 'scan': '0/4', 'anglais': '2/2', 'multi-documents': '1/3', 'audio': '2/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-open-notebook': 7301, 'rag-open-notebook-surrealdb': 113, 'vllm-central': 6798, 'vllm-embed': 4899} |
| pic_ram_application_mo | 7414 |
| vram | 15693 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | 70.1 |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | - | True | 4.59 | Le chiffre d'affaires de Vélanor pour l'année 2025 était de **48,6 M€** [source: |
| Q02 | fait simple | oui | - | True | 1.26 | Vélanor a été fondée en 2014 à Nantes [source:81ggj1mrclmyi21pjq27]. |
| Q03 | fait simple | oui | - | True | 1.76 | La présidente de Vélanor est Hélène Marchais. Elle dirige l'entreprise depuis 20 |
| Q04 | fait simple | oui | - | True | 1.37 | Le siège de Vélanor est situé au 12 quai de la Fosse, à Nantes [source:81ggj1mrc |
| Q05 | tableau | oui | - | True | 1.91 | Vélanor comptait 412 salariés au 31 décembre 2025 [source:81ggj1mrclmyi21pjq27]. |
| Q06 | tableau | oui | - | True | 2.22 | Le chiffre d'affaires du troisième trimestre 2025 s'est élevé à 14,2 M€, ce qui  |
| Q07 | tableau | oui | - | True | 1.41 | Le modèle Sèvre Trail a produit **15 400** unités en 2025. [source:81ggj1mrclmyi |
| Q08 | tableau | oui | - | True | 2.1 | Le prix public du modèle Erdre Cargo est de 4 290 € TTC [source:81ggj1mrclmyi21p |
| Q09 | tableau | oui | - | True | 1.87 | Le site de Cholet emploie 97 salariés au 31/12/2025 [source:81ggj1mrclmyi21pjq27 |
| Q10 | fait simple | oui | - | True | 1.46 | Les cadres de Vélanor sont fabriqués à partir d'aluminium recyclé à hauteur de * |
| Q11 | fait simple | oui | - | True | 1.65 | Le taux de recyclage des batteries usagées chez Vélanor atteint $96\%$, ce qui e |
| Q12 | tableau | oui | - | True | 2.16 | Le fournisseur qui livre les moteurs est **Motodrive Co.** et il est installé à  |
| Q13 | tableau | oui | - | True | 1.43 | Vélanor a dégagé un résultat net de 3,1 M€ en 2025 [source:81ggj1mrclmyi21pjq27] |
| Q14 | fait simple | oui | - | True | 1.59 | Le taux de retour sous garantie pour Vélanor s'établit à **1,8 %** des vélos ven |
| Q15 | scan | non | - | True | 6.12 | Je suis désolé, mais les documents contextuels que j'ai sont les suivants : un r |
| Q16 | scan | non | - | False | 2.15 | Le délai moyen constaté pour les livraisons de batteries de la part de Batterix  |
| Q17 | scan | non | - | True | 4.04 | Je suis désolé, mais je n'ai pas trouvé d'information concernant le plafond des  |
| Q18 | scan | non | - | True | 4.73 | Je n'ai trouvé aucune information concernant un volume minimal annuel de batteri |
| Q19 | fait simple | oui | - | False | 2.21 | Les batteries doivent être stockées entre $10\,^\circ\text{C}$ et $25\,^\circ\te |
| Q20 | fait simple | oui | - | False | 1.4 | La responsabilité de la procédure de charge et de stockage des batteries incombe |
| Q21 | tableau | oui | - | False | 1.38 | Le local B2 est inspecté le premier lundi de chaque mois, et c'est Karim Benali  |
| Q22 | fait simple | oui | - | False | 1.33 | Le prix public du Vilaine Compact, qui est un vélo pliant électrique, est de 2 4 |
| Q23 | fait simple | oui | - | False | 1.86 | La capacité prévue pour l'usine de Saint-Nazaire est de **25 000 vélos par an**  |
| Q24 | tableau | oui | - | False | 1.65 | Le stock actuel de la batterie BAT-48V-14Ah est de 1240 unités, ce qui est en de |
| Q25 | fait simple | oui | - | True | 1.21 | La garantie pour le cadre est de 7 ans. [source:zfw2v0083daeckkaxloq] |
| Q26 | fait simple | oui | - | False | 1.86 | Le numéro de téléphone du service après-vente est le 02 40 00 12 34, et il est d |
| Q27 | fait simple | oui | - | True | 1.67 | La prime d'intéressement pour 2025 est de 1 150 euros par salarié, et elle sera  |
| Q28 | anglais | oui | - | True | 1.57 | Batterix GmbH obtained an overall score of 87 out of 100 during the Supplier Qua |
| Q29 | anglais | oui | - | True | 1.45 | Le taux de défaut des cellules mesuré chez Batterix GmbH lors de l'audit était d |
| Q30 | multi-documents | non | - | True | 2.56 | Le document ne précise pas le délai de livraison **contractuel** de Batterix. Ce |
| Q31 | multi-documents | non | - | True | 2.64 | Le score obtenu par Batterix lors de l'audit est de 87 sur 100 [source:kculylfw5 |
| Q32 | multi-documents | oui | - | True | 2.54 | Vélanor vise un chiffre d'affaires de **55 M€** en 2026 [source:xvba2xzxt6jghnqa |
| Q33 | audio | oui | - | False | 1.99 | La ligne d'assoblage numéro 3 de Nantes sera arrêtée pour maintenance du 2 au 6  |
| Q34 | audio | oui | - | False | 1.82 | Le directeur de production de Vélanor est Julien Moreau [z7jmrzx6em1n3jzr0vdg].  |
| Q35 | piège | oui | - | - | 4.34 | Je suis désolé, mais les documents dont je dispose ne contiennent aucune informa |
| Q36 | piège | oui | - | - | 2.42 | Je suis désolé, mais les documents de contexte que j'ai à ma disposition ne ment |
| Q37 | piège | oui | - | - | 2.3 | Je suis désolé, mais les documents contextuels que j'ai accès ne contiennent auc |
| Q38 | piège | oui | - | - | 1.76 | Je suis désolé, mais les documents contextuels que j'ai consultés ne contiennent |
