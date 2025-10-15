```
@startuml
title Empty Diagram - NF18
@startuml
skinparam linetype ortho
hide methods
hide stereotypes



' ===================== ENTITÉS =====================

class USERS {

email : TEXT {PK}
--
nom : TEXT
motDePasse : TEXT
dateInscription : DATE
typeUtilisateur : ENUM("regulier","premium")
}

class PREMIUM {
qualiteGeneration : TEXT
horsLigneAutorise : BOOL
}
class MODELE {

nom : TEXT {PK}
--
description : TEXT
dateCreation : DATE
typeModele : ENUM("texte","image","video")
}


class LIMITEIMAGE {
resolution : TEXT
}
class LIMITEVIDEO {
duree : TEXT
}
class LIMITETEXTE {
longueurMax : TEXT
}
class DONNEE_ENTRAINEMENT {

contenu : TEXT {PK}
--
typeDonnee : TEXT
dateAjout : DATE
}

class RESULTAT {

dateDebut : DATE {PK}
}

class METADONNEE {

cle : TEXT {PK}
--
valeur : TEXT {PK}
}


class EVALUATION {

note : INT {PK}
commentaire : TEXT {PK}
date : DATE {PK}
}


class COLLABORATION {
dateDebut : DATE
dateFin : DATE
}
note right of COLLABORATION
CHECK utilisateurs_distincts: A <> B
end note
class HISTORIQUE_UTILISATION {
typeInteraction : TEXT 
date : DATE {PK}
}


' ===================== ASSOCIATIONS / CARDINALITÉS =====================

HISTORIQUE_UTILISATION  "*" -- "1" USERS : "sont associé"
DONNEE_ENTRAINEMENT  "*" -- "*" MODELE : "entraine"
MODELE  "1" -- "*" RESULTAT : "produit"
METADONNEE "1..N" -- "1" RESULTAT : "décrit"
RESULTAT  "1" -- "*" EVALUATION : "est évalué"
USERS "2" .. "*" COLLABORATION : "collaborent sur"
COLLABORATION }o--|| MODELE      : "utilise"
USERS "1" -- "*" RESULTAT
(USERS, RESULTAT) .. EVALUATION
LIMITETEXTE --|> MODELE
LIMITEIMAGE --|> MODELE
LIMITEVIDEO --|> MODELE
PREMIUM --|> USERS
USERS "1" -- "*" EVALUATION
MODELE "1"-- "*" HISTORIQUE_UTILISATION

@enduml
```
