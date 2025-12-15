#!/usr/bin/python3

import psycopg2
import rqst as rq
from datetime import date


HOST = "tuxa.sme.utc"
USER = "nf18a016"
PASSWORD = "EX8GdC5vmx9e"
DATABASE = "dbnf18a016"


conn = psycopg2.connect(
    "host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD)
)




choice = '1'
while choice in ['1','2','3','4','5','6','7','8','9','10']:
    print("1 - Supprimer un utilisateur")
    print("2 - Supprimer un commentaire")
    print("3 - Modifier le statut d'un utilisateur")
    print("4 - Ajouter un modèle")
    print("5 - Calculer la durée moyenne de génération de contenu pour chaque modèle d’IA")
    print("6 - Identifier les utilisateurs les plus actifs dans la base de données")
    print("7 - Lister les collaborations actives entre utilisateurs et modèles d’IA")
    print("8 - Statistiques des évaluations par modèle")
    print("9 - Modèles les plus utilisés (9 derniers mois)")
    print("10 - Collaborations actives")

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
        rq.dureeMoyenneGeneration(conn) 
    elif choice == '6':
        rq.Utilisateuractif(conn)
    elif choice == '7':
        rq.collaborationsActives(conn)
    elif choice == '8':
        rq.statistiquesEvaluations(conn)
    elif choice == '9':
        rq.modelesUtilisationRecente(conn)
    elif choice == '10':
        rq.collaborationsActivesModeles(conn)
    else: 
        print("Fin du programme.")
        break



conn.close()



