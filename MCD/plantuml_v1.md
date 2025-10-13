@startuml
title Empty Diagram - NF18
@startuml
' Optionnel : quelques réglages de lisibilité
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
note right of USERS
typeUtilisateur: regulier | premium
Les champs "qualiteGeneration" et "horsLigneAutorise"
ne concernent que les comptes premium.
end note

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
note right of MODELE
limiteTechnique (JSONB) ex:
{ max_resolution, max_duree_sec, max_longueur }
end note

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
valeur : TEXT
}
note right of METADONNEE
PK composite: (idGeneration, cleMeta)
idGeneration est aussi une FK vers GENERATION.
end note

class EVALUATION {

note : INT {PK}
commentaire : TEXT
date : DATE
}
note right of EVALUATION
Contrôle d'unicité logique:
UNIQUE(idGeneration, idUtilisateur)
(endroit exact à implémenter au niveau BDD)
end note

class COLLABORATION {
dateDebut : DATE
dateFin : DATE
}
note right of COLLABORATION
CHECK utilisateurs_distincts: A <> B
CHECK borne_dates: dateFin IS NULL OR dateFin > dateDebut
(endroit exact à implémenter au niveau BDD)
end note
class HISTORIQUE_UTILISATION {
typeInteraction : TEXT
date : DATE
}
' ===================== ASSOCIATIONS / CARDINALITÉS =====================
HISTORIQUE_UTILISATION  "*" -- "1" USERS : "sont associé"
DONNEE_ENTRAINEMENT  "*" -- "*" MODELE : "entraine"
MODELE  "1" -- "*" RESULTAT : "produit"
METADONNEE "1..N" -- "1" RESULTAT : "décrit"
RESULTAT  "1" -- "*" EVALUATION : "est évalué"
USERS "2" -- "*" COLLABORATION : "collaborent sur"
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