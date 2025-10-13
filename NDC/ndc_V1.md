 # Notice de Clarification Conceptuelle

**Users**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| nom | texte | Nom complet de l’utilisateur | non nul |
| email | texte | Adresse électronique unique | unique, non nul , clé candidate|
| motDePasse | texte | Mot de passe chiffré de connexion | non nul |
| dateInscription | date | Date d’inscription au service | non nul |
| typeUtilisateur | enumération(régulier,premium) |  | non nul |

**Premium**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| quantiteGeneration| texte | Quantite de génération |  |
| horsLigneAutorise | booléen | Droit d’utilisation hors ligne | présent uniquement si premium |


Premium est un héritage de Users
quantiteGeneration depend de typeUtilisateur
Plusieurs catégorie de premium exprimée par 0 pour un niveau regulier et 1 pour niveau premium


**MODELE**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| nom | texte | Nom du modèle d’IA | unique, non nul , clé primaire|
| description | texte | Description du modèle | \- |
| dateCreation | date | Date de création du modèle | non nul |
| typeModele | énumération (texte,image,vidéo) | Type de modèle d’IA | non nul |



**LIMITEIMAGE**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| resolution | texte | dans le cas d'une image | |

**LIMITEVIDEO**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| duree| texte | dans le cas d'une video| |


**LIMITETEXTE**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| longuerMax | texte | dans le cas d'un texte | |



LIMITEIMAGE, LIMITEVIDEO, LIMITETEXTE sont des classes filles de MODELE donc héritent des attributs de MODELE 


**DONNEE\_ENTRAINEMENT**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| typeDonnee | texte | Type (texte, image, vidéo…) | non nul, contrainte avec typeModele |
| contenu | texte | Référence ou chemin vers la donnée | |
| dateAjout | date |  | |


**RESULTAT**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| dateDebut | date|  |  |



**METADONNEE**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| cle | texte| cle valeur | Unique non nul |
| valeur| texte| valeur des metadonnee |  |

METADONNEE est une composition de la classe RESULTAT

Comme valeur de METADONNEE, on pourra retrouver la durée de génération ou la résolution d'une image, 
la durée de la vidéo ou la longueur max du texte.

**COLLABORATION**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| dateDebut | date |  | non nul |
| dateFin | date |  | doit être \> dateDebut |

COLLABORATION EST une classe d'association de la relation réflexive USERS vers USERS


**Contraintes :**

* idUtilisateurA ≠ idUtilisateurB  


**EVALUATION**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| note | entier  |  | entier de 0 à 5 |
| commentaire | texte | | |
| date | date|  | |

EVALUATION EST une classe d'association de la relation entre USERS et RESULTAT


**HISTORIQUE\_UTILISATION**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| typeInteraction | texte | | non nul |
| date | date |  | non nul |

**RELATION**

**Un UTILISATEUR 1 évalue  * EVALUATION
**Des HISTORIQUE\_UTILISATION * sont associé a 1 UTILISATEUR
**Un ou Plusieurs Donnee d'entrainement 1..* entraine Un ou Plusieurs MODELE 1...*
**Un MODELE 1 produit * RESULTAT
*Une ou Plusieurs metadonnee 1..* décrit 1 RESULTAT
**1 RESULTAT est évalue par * EVALUATION (classe d'association)
** * USERS collabore avec * USERS (classe d'association)
**Une collaboration 1 est associé à 1 MODELE 



**Contraintes générales**

**-typeUtilisateur de USERS est un énum (régulier,premium)
**-quantiteGeneration et horsLigneAutorise de PREMIUM dépendent de typeUtilisateur de USERS
**-typeModele de USERS est un énum (texte, image, video)
**-typeDonnee de DONNEEENTRAINEMENT dépend de typeModele de MODELE
**-dateFin \> dateDebut dans Collaboration.
**-dans collaboration qui est une classe d'association de la relation USERS vers USERS il faut que idUtilisateurA ≠ idUtilisateurB  
**-note de EVALUATION est compris entre 0 et 5 



