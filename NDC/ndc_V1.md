 # Notice de Clarification Conceptuelle

**Users**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| nom | texte | Nom complet de l’utilisateur | non nul |
| email | texte | Adresse électronique unique | unique, non nul , clé candidate|
| motDePasse | texte | Mot de passe chiffré de connexion | non nul |
| dateInscription | date | Date d’inscription au service | non nul |
| typeUtilisateur | enumération(régulier,premium) | Catégorie d’abonnement | non nul |

**Premium**

| Nom | Type | Description | Contraintes |
| ----- | ----- | ----- | ----- |
| qualiteGeneration| texte | Qualité de génération | présent uniquement si premium |
| horsLigneAutorise | booléen | Droit d’utilisation hors ligne | présent uniquement si premium |

Premium est un héritage de Users
Plusieurs catégorie de  


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



