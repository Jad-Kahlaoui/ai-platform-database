# Transformation du SQL au NOSQL




## Création de la collection "users"
```
db.createCollection("users")
```
**Implémentation d'un premier objet dans "users"**

```
db.users.insertOne({
  _id: "jad@mail.com",
  nom: "Jad",
  motDePasse: "XXXXXX",
  dateInscription: new Date("2025-12-01"),
  typeUtilisateur: "premium",
  qualiteGeneration: "haute",
  horsLigneAutorise: true
})
```
## Création de la collection "modeles"
```
db.createCollection("modeles")
```
**Implémentation d'un premier objet dans "modeles"**
```

db.modeles.insertOne({
  _id: "ModeleTexteV1",
  description: "Modèle de génération de texte",
  dateCreation: new Date("2025-11-20"),
  typeModele: "texte",
  longueurMax: 4096
})
```
 Exemple pour video

```
db.modeles.insertOne({
  _id: "ModelevideoV1",
  description: "Modèle de génération de texte",
  dateCreation: new Date("2025-11-20"),
  typeModele: "video",
  duree: 200
})

```

 Exemple pour image

```
db.modeles.insertOne({
  _id: "ModelevideoV1",
  description: "Modèle de génération de texte",
  dateCreation: new Date("2025-11-20"),
  typeModele: "image",
  Resolution: 1080
})

```



## Création de la collection "donnees_entrainement"

```
db.createCollection("donnees_entrainement")
```
**Implémentation d'un premier objet dans "donnees_entrainements"**
```
db.donnees_entrainement.insertOne({
  contenu: "Textes en français",
  typeDonnee: "texte",
  dateAjout: new Date("2025-11-25")
})
```
On peut égallement avoir une donnee d'entrainements d'un type différent géré par la meme collection 
```
db.donnees_entrainement.insertOne({
  contenu: "Video_de_la_savane.mp4",
  typeDonnee: "video",
  dateAjout: new Date("2025-11-25")
})
```

## Création de la collection "entrainements"
```
db.createCollection("entrainements")
```
**Implémentation d'un premier objet dans "entrainements"**
```
db.entrainements.insertOne({
  modele: "ModeleTexteV1",
  donneeEntrainement: ObjectId("656a1f2c9a1c4b8e4d123456"),  // Exemple de ObjectID
  dateEntrainement: new Date("2025-12-01")
})
``` 
Ici il  est nécessaire d'inclure donneEntrainements dans la collection entrainements , en effet donneeEntrainements est toujours utilisé selon son entrainements.
La collection represente EntrainementModele venant du MLD 

## Création de la collection "resultats"
```
db.createCollection("resultats")
```
**Implémentation d'un premier objet dans "resultat"**
```
db.resultats.insertOne({
  utilisateur: "adrien@mail.com",
  modele: "ModeleTexteV1",
  dateDebut: new Date("2025-12-17"),

  metadonnees: {
    temps_execution_ms: "1200",
    format_sortie: "txt"
  },

  evaluations: [
    {
      utilisateur: "adrien@mail.com",
      date: new Date("2025-12-17"),
      note: 4,
      commentaire: "Bon résultat"
    }
  ]
})
```

Les entités MetaDonnee et Evaluation sont intégrées sous forme de documents JSON imbriqués dans Resultat, car elles dépendent directement de ce dernier et sont toujours consultées dans son contexte. À l’inverse, les entités ayant une existence propre ou un volume important sont conservées dans des collections séparées 




## Création de la collection "collaborations"
```
db.createCollection("collaborations")
```
**Implémentation d'un premier objet dans "collaborations"**
```
db.collaborations.insertOne({
  modele: "ModeleTexteV1",
  emailA: "jad@mail.com",
  emailB: "enora@mail.com",
  dateDebut: new Date("2025-12-01"),
  dateFin: new Date("2025-12-10")
})
```
## Création de la collection "historique_utilisation"

```
db.createCollection("historique_utilisation")
```
**Implémentation d'un premier objet dans "historique_utilisation"**
```
db.historique_utilisation.insertOne({
  utilisateur: "jad@mail.com",
  modele: "ModeleTexteV1",
  date: new Date("2025-12-17"),
  typeInteraction: "generation"
})
```


## Exemples de requêtes MongoDB

1. Lister tous les utilisateurs

```
db.users.find()
```
2. Trouver un utilisateur par email
```
db.users.find({ _id: "jad@mail.com" })

```
3. Lister les évaluations d’un résultat donné
```
db.resultats.find(
  { modele: "ModeleTexteV1" },
  { evaluations: 1, _id: 0 }
)
```

4.Trouver tous les modèles collaboratifs d’un utilisateur


```
db.collaborations.find({
  $or: [
    { emailA: "jad@mail.com" },
    { emailB: "jad@mail.com" }
  ]
})
```

