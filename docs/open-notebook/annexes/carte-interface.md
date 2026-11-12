# Carte de l'interface

Liste de contrôle de la couverture du manuel : chaque page, menu, onglet, fenêtre et réglage visible de l'interface d'Open Notebook 1.15.1 (en français), avec le chapitre de la partie 1 qui l'explique. Relevé le 12 novembre 2026 par Playwright, une fois connecté (scripts `outils/open-notebook/captures/carte.py` et `sonde.py` ; texte et inventaire de chaque page dans `outils/resultats/open-notebook/captures/carte/`). Une capture de repérage par page est gardée dans `../img/carte/`.

## Pages

| Page ou menu | Chemin d'accès | Éléments (boutons, onglets, réglages) | Manuel qui le couvre |
|---|---|---|---|
| Connexion ([repérage](../img/carte/01-connexion.png)) | `http://127.0.0.1:8502` | champ du mot de passe, « Se connecter » | [02](../manuel/02-installer-open-notebook.md), [12](../manuel/12-en-cas-de-probleme.md) |
| Menu de gauche | toutes les pages | « Créer » ; COLLECTER : « Sources » ; TRAITER : « Carnets », « Demander et rechercher » ; CRÉER : « Podcasts » ; GÉRER : « Modèles », « Transformations », « Paramètres », « Avancé » ; flèche de repli du menu | [03](../manuel/03-premiers-pas.md) |
| Bas du menu de gauche | toutes les pages | « Actions rapides » (Ctrl+K), « Thème », « Langue », « Se déconnecter » | [03](../manuel/03-premiers-pas.md) |
| Menu « Créer » ([repérage](../img/carte/16-menu-creer.png)) | menu de gauche › « Créer » | « Source », « Carnet », « Podcast » | [03](../manuel/03-premiers-pas.md), [05](../manuel/05-ajouter-et-organiser-les-sources.md) |
| Menu « Langue » ([repérage](../img/carte/18-menu-langue.png)) | bas du menu › « Langue » | quatorze langues, dont « Français » et « English » | [03](../manuel/03-premiers-pas.md) |
| Menu « Thème » ([repérage](../img/carte/19-menu-theme.png)) | bas du menu › « Thème » | « Clair », « Sombre », « Système » | [03](../manuel/03-premiers-pas.md) |
| Actions rapides ([repérage](../img/carte/20-actions-rapides.png)) | Ctrl+K, ou « Actions rapides » | champ « Entrez votre recherche... », navigation, recherche, question, thème | [03](../manuel/03-premiers-pas.md) |
| Carnets ([repérage](../img/carte/02-carnets.png)) | menu › TRAITER › « Carnets » | bouton d'actualisation, « Vue en mosaïque », « Vue en liste », « Rechercher des carnets... », « Nouveau Carnet », « Consultés récemment » (repliable), « Carnets actifs », cartes de carnet (nombre de sources et de notes) | [04](../manuel/04-premiere-question.md), [05](../manuel/05-ajouter-et-organiser-les-sources.md) |
| Fenêtre « Créer un nouveau carnet » ([repérage](../img/carte/17-fenetre-nouveau-carnet.png)) | Carnets › « Nouveau Carnet », ou « Créer » › « Carnet » | « Nom », « Description », « Annuler », « Créer un nouveau carnet » | [04](../manuel/04-premiere-question.md) |
| Page d'un carnet ([repérage](../img/carte/03-carnet.png)) | Carnets › clic sur une carte | nom et description modifiables, « Archiver », « Supprimer » ; colonnes SOURCES, NOTES, DISCUTER AVEC LE CARNET | [04](../manuel/04-premiere-question.md), [05](../manuel/05-ajouter-et-organiser-les-sources.md), [06](../manuel/06-discuter-avec-les-sources.md) |
| Colonne SOURCES | page d'un carnet | « Ajouter la source » (menu : « Ajouter la source », « Ajouter des sources existantes »), « Contexte » (menu : « Tout inclure (aperçus uniquement) », « Tout inclure (contenu complet) », « Tout exclure du contexte »), repli de la colonne, cartes de source, icône de mode de contexte, « Réessayer le traitement » sur une source en échec | [04](../manuel/04-premiere-question.md), [05](../manuel/05-ajouter-et-organiser-les-sources.md), [06](../manuel/06-discuter-avec-les-sources.md) |
| Fenêtre « Ajouter la source » ([repérage](../img/carte/21-fenetre-ajouter-source.png)) | colonne SOURCES › « Ajouter la source » | type de source (lien, fichier, texte), carnets de destination, transformations à appliquer, traitement et embedding | [04](../manuel/04-premiere-question.md), [05](../manuel/05-ajouter-et-organiser-les-sources.md) |
| Colonne NOTES | page d'un carnet | « Écrire une note », repli de la colonne, cartes de note | [07](../manuel/07-notes-et-transformations.md) |
| Fenêtre de note ([repérage](../img/carte/22-fenetre-note.png)) | NOTES › « Écrire une note » | titre « Note sans titre », éditeur avec barre de mise en forme (gras, italique, barré…), aperçu, enregistrement | [07](../manuel/07-notes-et-transformations.md) |
| Colonne DISCUTER AVEC LE CARNET | page d'un carnet | « Sessions », compteur « Context » (sources, notes, jetons, caractères), « Modèle », champ de question, bouton d'envoi, icônes sous une réponse (enregistrer en note, copier), « Références » | [04](../manuel/04-premiere-question.md), [06](../manuel/06-discuter-avec-les-sources.md) |
| Fenêtre « Sessions de Chat » | colonne de discussion › « Sessions » | liste des conversations, création, renommage, suppression | [06](../manuel/06-discuter-avec-les-sources.md), [11](../manuel/11-cas-pratiques.md) |
| Fenêtre « Configuration du modèle » | colonne de discussion › bouton du modèle | « Modèle » (par défaut : `chat`), « Réinitialiser », « Enregistrer les modifications » | [06](../manuel/06-discuter-avec-les-sources.md) |
| Sources ([repérage](../img/carte/04-sources.png)) | menu › COLLECTER › « Sources » | tableau « Toutes les sources » : « Type », « Titre », « Créé », « Mis à jour », « Aperçus », « Indexé (Embedded) », « Actions » (tri par colonne) | [05](../manuel/05-ajouter-et-organiser-les-sources.md) |
| Page d'une source ([repérage](../img/carte/05-source.png)) | Sources › clic sur une ligne, ou citation | « Back to Sources », titre, onglets « Contenu », « Analyses », « Détails » ; conversation propre à la source (« Sessions », modèle, question) | [05](../manuel/05-ajouter-et-organiser-les-sources.md), [06](../manuel/06-discuter-avec-les-sources.md) |
| Onglet « Analyses » ([repérage](../img/carte/06-source-analyses.png)) | page d'une source | « Sélectionner une transformation... », « Créer », analyses produites | [07](../manuel/07-notes-et-transformations.md) |
| Onglet « Détails » ([repérage](../img/carte/07-source-détails.png)) | page d'une source | type, dates, carnets, embedding, « Télécharger » | [05](../manuel/05-ajouter-et-organiser-les-sources.md) |
| Demander et rechercher, onglet « Demander (bêta) » ([repérage](../img/carte/08-demander-et-rechercher.png)) | menu › TRAITER › « Demander et rechercher » | « Question », « Carnets » (« Tous les carnets »), « Utilisation des modèles par défaut », « Avancé » (« Stratégie », « Réponse », « Final »), « Demander » | [08](../manuel/08-rechercher-et-demander.md) |
| Demander et rechercher, onglet « Recherche » ([repérage](../img/carte/09-recherche-recherche.png)) | même page › « Recherche » | champ « Entrez votre recherche... », « Carnets », « Type de recherche » (« Recherche textuelle », « Recherche vectorielle »), « Rechercher dans les Sources », « Rechercher dans les Notes » | [08](../manuel/08-rechercher-et-demander.md) |
| Podcasts, onglet « Épisodes » ([repérage](../img/carte/10-podcasts.png)) | menu › CRÉER › « Podcasts » | « Aperçu des épisodes », « Générer un podcast », « Rafraîchir », épisodes (état, lecteur, suppression) | [09](../manuel/09-creer-un-podcast.md) |
| Fenêtre « Générer un épisode de podcast » | Épisodes › « Générer un podcast », ou « Créer » › « Podcast » | CONTENU (carnets, sources, notes à inclure), « Profil de l'épisode », « Nom de l'épisode », « Instructions supplémentaires », « Générer » | [09](../manuel/09-creer-un-podcast.md) |
| Podcasts, onglet « Profils » ([repérage](../img/carte/11-podcasts-profils.png)) | Podcasts › « Profils » | « Comment les profils propulsent la génération », « Profils d'intervenants » (« Créer un intervenant », « Modifier »), « Profils d'épisode » (« Créer un profil ») | [09](../manuel/09-creer-un-podcast.md) |
| Fenêtre « Créer un profil d'intervenant » | Profils › « Créer un intervenant » | « Nom du profil », « Description », « Modèle vocal », « Ajouter un intervenant » (un à quatre), par intervenant : « Nom », « ID de la voix », « Histoire (Backstory) », « Personnalité », remplacement TTS | [09](../manuel/09-creer-un-podcast.md) |
| Fenêtre « Créer un profil d'épisode » | Profils › « Créer un profil » | « Nom du profil », « Segments », « Jetons de sortie maximum », « Description », profil d'intervenant, modèles du plan et de la transcription, langue, briefing par défaut | [09](../manuel/09-creer-un-podcast.md) |
| Modèles ([repérage](../img/carte/12-modeles.png)) | menu › GÉRER › « Modèles » | « Attributions des modèles par défaut » : « Modèle de Chat », « Modèle d'Embedding », « Modèle de Synthèse Vocale (TTS) », « Modèle de Transcription Vocale (STT) », « Avancé » : « Modèle de Transformation », « Modèle d'Outils », « Modèle à large contexte » ; blocs de fournisseurs (« OpenAI Compatible », Ollama, services en ligne…) avec configurations : « Test », « Models », « Modifier », « Supprimer », « Tester le modèle », « Supprimer le modèle », « Ajouter une configuration » | [03](../manuel/03-premiers-pas.md) |
| Fenêtre « Ajouter une configuration » ([repérage](../img/carte/23-fenetre-ajout-fournisseur.png)) | Modèles › bloc du fournisseur › « Ajouter une configuration » | « Nom de la configuration », « Clé API (Optionnel) » (« Show »), « URL de base », « Annuler », « Ajouter une configuration » ; même fenêtre en modification (« Modifier la configuration ») | [03](../manuel/03-premiers-pas.md) |
| Fenêtre « Découvrir les modèles » | Modèles › configuration › « Models » | « Type de modèle », cases des modèles proposés par le fournisseur, « Ajouter (N) » | [03](../manuel/03-premiers-pas.md) |
| Transformations ([repérage](../img/carte/13-transformations.png)) | menu › GÉRER › « Transformations » | onglets « Transformations » et « Bac à sable (Playground) » ; « Prompt de transformation par défaut », « Créer une nouvelle », six transformations fournies (« Modifier », suppression) | [07](../manuel/07-notes-et-transformations.md) |
| Fenêtre « Créer une nouvelle » (transformation) | Transformations › « Créer une nouvelle » | « Nom », « Titre », « Modèle », « Suggérer par défaut sur les nouvelles sources », « Ajouter une description », « Prompt Système » | [07](../manuel/07-notes-et-transformations.md) |
| Onglet « Bac à sable (Playground) » | Transformations › « Bac à sable (Playground) » | transformation, modèle, texte d'essai, exécution | [07](../manuel/07-notes-et-transformations.md) |
| Paramètres ([repérage](../img/carte/14-parametres.png)) | menu › GÉRER › « Paramètres » | « Traitement du contenu » : « Moteur de traitement de documents », « Activer l'OCR », « Extraire les formules », « Décrire les images et les graphiques », « Moteur de traitement d'URL » ; « Indexation (Embedding) et Recherche » : « Option d'indexation par défaut » (« Demander », « Toujours », « Jamais ») ; « Gestion des fichiers » : « Suppression automatique des fichiers » ; « Aidez-moi à choisir » ; « Enregistrer » | [10](../manuel/10-regler-l-application.md) |
| Avancé ([repérage](../img/carte/15-avance.png)) | menu › GÉRER › « Avancé » | « Infos Système » (« Version actuelle », « Dernière version », « État ») ; « Reconstruire les index (Embeddings) » : « Mode de reconstruction », « Inclure dans la reconstruction » (« Sources », « Notes », « Analyses »), « Lancer la reconstruction », trois questions dépliables | [10](../manuel/10-regler-l-application.md) |
| Se déconnecter | bas du menu › « Se déconnecter » | retour à la page de connexion | [03](../manuel/03-premiers-pas.md) |

## Non couvert

| Élément | Chemin d'accès | Éléments | Manuel qui le couvre |
|---|---|---|---|
| Fournisseurs en ligne payants (OpenAI, Anthropic, Google…) | Modèles › blocs des fournisseurs | configurations avec clé d'API payante | Non couvert : hors périmètre de la mission (aucun compte en ligne, aucune dépense) |
| Page de démonstration du thème (`/dev/design`) | adresse saisie à la main | composants graphiques | Non couvert : page de développement, absente des menus |

## Captures de repérage

Une capture par page ou fenêtre, prise pendant le relevé (sans annotation).

![Repérage : 01-connexion](../img/carte/01-connexion.png)
*Repérage : connexion.*

![Repérage : 02-carnets](../img/carte/02-carnets.png)
*Repérage : carnets.*

![Repérage : 03-carnet](../img/carte/03-carnet.png)
*Repérage : carnet.*

![Repérage : 04-sources](../img/carte/04-sources.png)
*Repérage : sources.*

![Repérage : 05-source](../img/carte/05-source.png)
*Repérage : source.*

![Repérage : 06-source-analyses](../img/carte/06-source-analyses.png)
*Repérage : source analyses.*

![Repérage : 07-source-détails](../img/carte/07-source-détails.png)
*Repérage : source détails.*

![Repérage : 08-demander-et-rechercher](../img/carte/08-demander-et-rechercher.png)
*Repérage : demander et rechercher.*

![Repérage : 09-recherche-recherche](../img/carte/09-recherche-recherche.png)
*Repérage : recherche recherche.*

![Repérage : 10-podcasts](../img/carte/10-podcasts.png)
*Repérage : podcasts.*

![Repérage : 11-podcasts-profils](../img/carte/11-podcasts-profils.png)
*Repérage : podcasts profils.*

![Repérage : 12-modeles](../img/carte/12-modeles.png)
*Repérage : modeles.*

![Repérage : 13-transformations](../img/carte/13-transformations.png)
*Repérage : transformations.*

![Repérage : 14-parametres](../img/carte/14-parametres.png)
*Repérage : parametres.*

![Repérage : 15-avance](../img/carte/15-avance.png)
*Repérage : avance.*

![Repérage : 16-menu-creer](../img/carte/16-menu-creer.png)
*Repérage : menu creer.*

![Repérage : 17-fenetre-nouveau-carnet](../img/carte/17-fenetre-nouveau-carnet.png)
*Repérage : fenetre nouveau carnet.*

![Repérage : 18-menu-langue](../img/carte/18-menu-langue.png)
*Repérage : menu langue.*

![Repérage : 19-menu-theme](../img/carte/19-menu-theme.png)
*Repérage : menu theme.*

![Repérage : 20-actions-rapides](../img/carte/20-actions-rapides.png)
*Repérage : actions rapides.*

![Repérage : 21-fenetre-ajouter-source](../img/carte/21-fenetre-ajouter-source.png)
*Repérage : fenetre ajouter source.*

![Repérage : 22-fenetre-note](../img/carte/22-fenetre-note.png)
*Repérage : fenetre note.*

![Repérage : 23-fenetre-ajout-fournisseur](../img/carte/23-fenetre-ajout-fournisseur.png)
*Repérage : fenetre ajout fournisseur.*
