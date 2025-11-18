#!/usr/bin/python3

import psycopg2

HOST = "tuxa.sme.utc"
USER = "nf18a016"
PASSWORD = "EX8GdC5vmx9e"
DATABASE = "nf18a016"

conn = psycopg2.connect(
    "host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD)
)

choice = '1'
while choice in ['1','2','3','4','5','6','7']:
    print("1 - Supprimer un utilisateur")
    print("2 - Supprimer un commentaire")
    print("3 - Modifier le statut d'un utilisateur")
    print("4 - Ajouter un modèle")
    print("5 - Calculer la durée moyenne de génération de contenu pour chaque modèle d’IA")
    print("6 - Identifier les utilisateurs les plus actifs dans la base de données")
    print("7 - Lister les collaborations actives entre utilisateurs et modèles d’IA")
    print("Autre - Quitter")

    choice = input()

    if choice == '1':
        suppUser(conn)
    elif choice == '2':
        suppComment(conn)  
    elif choice == '3':
        modifierStatutUser(conn) 
    elif choice == '4':
        ajouterModele(conn)  
    elif choice == '5':
        dureeMoyenneGeneration(conn) 
    elif choice == '6':
        utilisateursActifs(conn) 
    elif choice == '7':
        collaborationsActives(conn) 

conn.close()
