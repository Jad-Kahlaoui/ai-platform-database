 #Niveau de Description Conceptuelle

**UTILISATEUR**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| idUtilisateur | entier (PK) | Identifiant unique de l’utilisateur | clé primaire |
| nom | texte | Nom complet de l’utilisateur | non nul |
| email | texte | Adresse électronique unique | unique, non nul |
| motDePasse | texte | Mot de passe chiffré de connexion | non nul |
| dateInscription | date/heure | Date d’inscription au service | défaut \= now() |
| typeUtilisateur | enum('régulier','premium') | Catégorie d’abonnement | non nul |
| qualiteGeneration | numérique | Qualité de génération (optionnel) | présent uniquement si premium |
| horsLigneAutorise | booléen | Droit d’utilisation hors ligne (optionnel) | présent uniquement si premium |

Les utilisateurs premium ont accès à des fonctionnalités supplémentaires (qualité, hors ligne, génération d’images/vidéos).  
Les utilisateurs réguliers n’ont pas ces attributs.

**MODELE**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| idModele | entier (PK) | Identifiant unique du modèle | clé primaire |
| nom | texte | Nom du modèle d’IA | unique, non nul |
| description | texte | Description du modèle | \- |
| dateCreation | date | Date de création du modèle | non nul |
| typeModele | enum('texte','image','video') | Type de modèle d’IA | non nul |
| limiteTechnique | texte / JSON | Spécifie la limite (résolution, durée, longueur max) | dépend du typeModele |

Chaque modèle d’IA a des limites techniques spécifiques selon son type :

* texte → longueur max de mots  
* image → résolution max  
* vidéo → durée max

**DONNEE\_ENTRAINEMENT**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| idDonnee | entier (PK) | Identifiant unique de la donnée d’entraînement | clé primaire |
| typeDonnee | texte | Type (texte, image, vidéo…) | non nul |
| contenu | texte | Référence ou chemin vers la donnée | non nul |
| dateAjout | date/heure | Date d’ajout de la donnée | défaut \= now() |
| idModele | entier (FK) | Référence au modèle entraîné | clé étrangère → MODELE.idModele |

Chaque donnée d’entraînement appartient à un **seul modèle** d’IA.

**GENERATION**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| idGeneration | entier (PK) | Identifiant du contenu généré | clé primaire |
| dateDebut | date/heure | Date de début de génération | défaut \= now() |
| idUtilisateur | entier (FK) | Utilisateur ayant lancé la génération | clé étrangère → UTILISATEUR.idUtilisateur |
| idModele | entier (FK) | Modèle utilisé pour la génération | clé étrangère → MODELE.idModele |

Une génération correspond à un contenu produit par un modèle pour un utilisateur.

**META\_GENERATION**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| idGeneration | entier (FK) | Référence à la génération associée | clé étrangère → GENERATION.idGeneration |
| cleMeta | texte | Nom du paramètre (ex : “duree\_sec”, “resolution”, “word\_count”) | clé primaire partielle |
| valeurMeta | texte | Valeur du paramètre | non nul |

**Clé primaire composée :** (idGeneration, cleMeta)

Ce modèle permet de stocker des métadonnées dynamiques, sous forme de paires clé–valeur.

**EVALUATION**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| idEvaluation | entier (PK) | Identifiant de l’évaluation | clé primaire |
| note | numérique (0..5) | Note donnée par un utilisateur | CHECK 0 ≤ note ≤ 5 |
| commentaire | texte | Avis textuel | facultatif |
| ts | date/heure | Date et heure de l’évaluation | défaut \= now() |
| idGeneration | entier (FK) | Génération évaluée | clé étrangère → GENERATION.idGeneration |
| idUtilisateur | entier (FK) | Utilisateur évaluateur | clé étrangère → UTILISATEUR.idUtilisateur |

Un utilisateur ne peut évaluer une génération qu’une seule fois   
		→ **UNIQUE(idGeneration, idUtilisateur)**

**COLLABORATION**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| idCollab | entier (PK) | Identifiant unique de la collaboration | clé primaire |
| dateDebut | date | Date de début de la collaboration | non nul |
| dateFin | date | Date de fin (null si en cours) | doit être \> dateDebut |
| idUtilisateurA | entier (FK) | Premier utilisateur | clé étrangère → UTILISATEUR.idUtilisateur |
| idUtilisateurB | entier (FK) | Second utilisateur | clé étrangère → UTILISATEUR.idUtilisateur |
| idModele | entier (FK) | Modèle utilisé dans la collaboration | clé étrangère → MODELE.idModele |

**Contraintes :**

* idUtilisateurA ≠ idUtilisateurB  
* dateFin \> dateDebut (ou null si active)

**HISTORIQUE\_UTILISATION**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| idHistorique | entier (PK) | Identifiant unique de l’action | clé primaire |
| typeInteraction | texte | Type d’action (génération, téléchargement, etc.) | non nul |
| ts | date/heure | Date de l’action | défaut \= now() |
| idUtilisateur | entier (FK) | Utilisateur concerné | clé étrangère → UTILISATEUR.idUtilisateur |
| idModele | entier (FK) | Modèle concerné | clé étrangère → MODELE.idModele |

Cette table journalise toutes les actions faites par les utilisateurs sur les modèles.

**Contraintes générales**

1. **Intégrité référentielle** : toutes les clés étrangères doivent pointer vers des entités existantes.  
2. **Intégrité de domaine** :  
   * note ∈ \[0,5\]  
   * typeUtilisateur ∈ {régulier, premium}  
   * typeModele ∈ {texte, image, vidéo}  
3. **Intégrité sémantique** :  
   * un utilisateur régulier ne peut pas avoir de qualiteGeneration ni horsLigneAutorise.  
   * dateFin \> dateDebut dans Collaboration.


