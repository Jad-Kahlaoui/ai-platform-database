#!/usr/bin/python3

import psycopg2
from datetime import date


HOST = "tuxa.sme.utc"
USER = "nf18a016"
PASSWORD = "EX8GdC5vmx9e"
DATABASE = "nf18a016"


conn = psycopg2.connect(
    "host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD)
)

# Version J 
def suppUser(conn):

    print("\n--- SUPPRIMER UN UTILISATEUR ---\n")

    email_supp = input("Entrez l'adresse email de l'utilisateur à supprimer : ").strip()

    try:
        with conn.cursor() as cur:

            cur.execute("""
                DELETE FROM Utilisateur
                WHERE email = %s
            """, (email_supp,))

            conn.commit()

            if cur.rowcount == 0:
                print("\nAucun utilisateur trouvé avec cet email.\n")
            else:
                print("\nUtilisateur supprimé avec succès.\n")

    except Exception as e:
        conn.rollback()
        print("Erreur SQL :", e)


# version J 
def ajouterModele(conn):

    print("\n--- AJOUTER UN NOUVEAU MODELE ---\n")

    nom = input("Nom du modèle : ").strip()
    descript = input("Description du modèle : ").strip()
    dateCreation = date.today()

    # Liste des types possibles
    types_modele = ["image", "texte", "video"]

    type_modele = input("Type de modèle (image / texte / video) : ").lower()
    while type_modele not in types_modele:
        print("Valeur invalide. Veuillez entrer : image, texte ou video.")
        type_modele = input("Type de modèle (image / texte / video) : ").lower()

    try:
        longueur = int(input("Longueur maximum de la saisie : "))
        resolution = int(input("Résolution : "))
        duree = int(input("Durée moyenne de génération (en secondes) : "))
    except ValueError:
        print("\nErreur : vous devez saisir des entiers.\n")
        return

    try:
        with conn.cursor() as cur:
            sql = """
                INSERT INTO Modele
                (nom, description, dateCreation, TypeModele, longueurMax, resolution, duree)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cur.execute(sql, (
                nom,
                descript,
                dateCreation,
                type_modele,
                longueur,
                resolution,
                duree
            ))

            conn.commit()

            print("\n>>> Modèle ajouté avec succès !\n")

    except Exception as e:
        conn.rollback()
        print("\nErreur SQL :", e)


# choix Supprimer commentaire 
def suppComment(conn):

    print("\n--- SUPPRIMER UNE ÉVALUATION (COMMENTAIRE) ---")

    email = input("Email de l'utilisateur ayant laissé l'évaluation : ")
    id_resultat = input("ID du résultat associé : ")

    cur = conn.cursor()

    cur.execute("""
        DELETE FROM Evaluation
        WHERE email = %s AND idResultat = %s
    """, (email, id_resultat))

    conn.commit()

    print("\n Évaluation supprimée (s'il y en avait une).\n")

    



#modifier statut de premium a normal ou inverse 
def modifierStatutUser(conn):

    print("\n--- MODIFIER LE STATUT D'UN UTILISATEUR ---")

    email = input("Entrez l'email de l'utilisateur : ")

    try:
        with conn.cursor() as cur:

            # Vérifier si l'utilisateur existe
            cur.execute("SELECT TypeUtilisateur, qualiteGeneration, horsLigneAutorise FROM Utilisateur WHERE email = %s", (email,))
            row = cur.fetchone()

            if row is None:
                print("\n Cet utilisateur n'existe pas.\n")
                return

            current_status, current_quality, current_horsligne = row

            print(f"\nStatut actuel : {current_status}")
            print(f"Qualité actuelle : {current_quality}")
            print(f"Hors-ligne actuel : {current_horsligne}")

            # Choisir le nouveau statut
            new_status = input("\nNouveau statut (normal / premium) : ").lower()
            while new_status not in ['normal', 'premium']:
                new_status = input("Valeur invalide. Entrez 'normal' ou 'premium' : ").lower()

            # Déterminer les contraintes métier etablie en MLD 
            if new_status == 'premium':
                # Premium peut choisir entre haute ou moyenne
                new_quality = input("Choisir la qualité (haute / moyenne) : ").lower()
                while new_quality not in ['haute', 'moyenne']:
                    new_quality = input("Valeur invalide. Choisir 'haute' ou 'moyenne' : ").lower()

                hors_ligne = True  # premium = TRUE obligatoire

            else:
                # normal : qualité = moyenne
                new_quality = 'moyenne'
                hors_ligne = False

            # Mise à jour SQL
            cur.execute("""
                UPDATE Utilisateur
                SET TypeUtilisateur = %s,
                    qualiteGeneration = %s,
                    horsLigneAutorise = %s
                WHERE email = %s
            """, (new_status, new_quality, hors_ligne, email))

            conn.commit()

            print(f"\n Le statut de {email} a été mis à jour :")
            print(f"  → Type : {new_status}")
            print(f"  → Qualité : {new_quality}")
            print(f"  → Hors-ligne : {hors_ligne}\n")

    except Exception as e:
        conn.rollback()
        print("Erreur : ", e)



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
    else: 
        print("Fin du programme.")
        break



conn.close()



