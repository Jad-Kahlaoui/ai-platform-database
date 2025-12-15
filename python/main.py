#!/usr/bin/python3

import psycopg2
import rqst as rq
import getpass

from datetime import date


HOST = "tuxa.sme.utc"
USER = "nf18a016"
PASSWORD = "EX8GdC5vmx9e"
DATABASE = "dbnf18a016"


# Constantes pour admin
ADMIN_EMAIL = "admin"
ADMIN_PASSWORD = "admin123
conn = psycopg2.connect(
    "host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD)
)




def connexion(conn):
    print("\n--- CONNEXION ---\n")
    email = input("Email : ").strip()
    password = getpass.getpass("Mot de passe : ").strip()

    # Cas ADMIN
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        print("\nConnexion administrateur réussie.\n")
        return "admin"

    # Cas UTILISATEUR NORMAL
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT motDePasse FROM Utilisateur WHERE email = %s", (email,))
            row = cur.fetchone()

            if row is None:
                print("Utilisateur inconnu.")
                return None

            if password == row[0]:
                print(f"\nConnexion utilisateur réussie ({email}).\n")
                return "user"
            else:
                print("Mot de passe incorrect.")
                return None
    except Exception as e:
        print("Erreur SQL :", e)
        return None

# Boucle de connexion
role = None
while role is None:
    role = connexion(conn)

# Menu admin
if role == "admin":
    choice = '1'
    while choice in [str(i) for i in range(1, 11)]:
        print("\n--- MENU ADMIN ---")
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

# Menu utilisateur minimaliste
elif role == "user":
    choice = '1'
    while choice == '1':
        print("\n--- MENU UTILISATEUR ---")
        print("1 - Mettre une évaluation")
        print("2 - Afficher mon historique d'utilisation")
        print("3 - Afficher mes résultats générés")
        print("4 - Afficher mes collaborations")
        print("5 - Afficher les modèles dipsonibles")
        print("Autre - Quitter")

        choice = input()

        if choice == '1':
            mettreUneEvaluations(conn)
        elif choice == '2':
            afficherMonHistorique(conn)
        elif choice == '3':
            afficherMesResultats(conn)
        elif choice == '4':
            afficherMesCollaborations(conn)
        elif choice == '5':
            afficherTousLesModeles(conn)
        else:
            print("Fin du programme.")
            break
        else:
            print("Fin du programme.")

conn.close()