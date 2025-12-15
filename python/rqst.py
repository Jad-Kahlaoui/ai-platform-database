from datetime import date

def dureeMoyenneGeneration(conn):

    print("\n--- DURÉE MOYENNE DE GÉNÉRATION PAR MODÈLE ---\n")

    sql = """
        SELECT 
            m.nom AS modele,
            AVG(md.valeur::int) AS duree_moyenne_generation,
            COUNT(*) AS nb_generations
        FROM Modele m
        JOIN Resultat r 
            ON r.nom = m.nom
        JOIN MetaDonnee md 
            ON md.idResultat = r.idResultat
           AND md.cle = 'duree_generation'
        GROUP BY m.nom
        HAVING COUNT(*) >= 5
        ORDER BY duree_moyenne_generation;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            if not rows:
                print("Aucun modèle avec au moins 5 générations.\n")
                return

            for modele, duree_moy, nb_gen in rows:
                print(f"• Modèle : {modele}")
                print(f"  Durée moyenne : {duree_moy:.2f} sec")
                print(f"  Nombre de générations : {nb_gen}\n")

    except Exception as e:
        print("Erreur SQL :", e)





def Utilisateuractif(conn):
    print("\n--- UTILISATEURS LES PLUS ACTIFS ---\n")

    sql = """
        SELECT 
            u.email,
            u.nom,
            COUNT(r.idResultat) AS nb_resultats
        FROM Utilisateur u
        JOIN Resultat r
            ON u.email = r.email
        GROUP BY u.email, u.nom
        ORDER BY nb_resultats DESC;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            if not rows:
                print("Aucun utilisateur n'a encore généré de résultat.\n")
                return

            for email, nom, nb in rows:
                print(f"• {nom} ({email}) → {nb} résultat(s) généré(s)")

            print()

    except Exception as e:
        print("Erreur SQL :", e)


def collaborationsActives(conn):

    print("\n--- MODELES AVEC PARAMÈTRES IMPORTANTS ---\n")

    sql = """
        SELECT 
            nom,
            TypeModele,
            longueurMax,
            duree
        FROM Modele
        WHERE 
              (duree IS NOT NULL AND duree > 300)     -- vidéos > 5 min
           OR (longueurMax IS NOT NULL AND longueurMax > 1000);  -- textes > 1000 mots
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            if not rows:
                print("Aucun modèle ne dépasse les seuils.")
                return

            for nom, type_m, longueur, duree in rows:
                print(f"• Modèle : {nom}")
                print(f"  Type : {type_m}")
                print(f"  Longueur max : {longueur}")
                print(f"  Durée : {duree}")
                print()

    except Exception as e:
        print("Erreur SQL :", e)



def statistiquesEvaluations(conn):

    print("\n--- STATISTIQUES DES ÉVALUATIONS PAR MODÈLE ---\n")

    sql = """
        SELECT
            m.nom AS modele,
            m.description,
            m.TypeModele,
            COUNT(e.note) AS nb_evaluations,
            AVG(e.note) AS note_moyenne
        FROM Evaluation e
        JOIN Resultat r
            ON e.idResultat = r.idResultat
        JOIN Modele m
            ON r.nom = m.nom
        GROUP BY m.nom, m.description, m.TypeModele
        ORDER BY note_moyenne DESC, nb_evaluations DESC;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            if not rows:
                print("Aucune évaluation trouvée.\n")
                return

            for nom, desc, type_m, nb_eval, note_moyenne in rows:
                print(f"• Modèle : {nom}")
                print(f"  Description : {desc}")
                print(f"  Type : {type_m}")
                print(f"  Nombre d'évaluations : {nb_eval}")
                print(f"  Note moyenne : {note_moyenne:.2f}\n")

    except Exception as e:
        print("Erreur SQL :", e)



def modelesUtilisationRecente(conn):

    print("\n--- MODELES LES PLUS UTILISÉS (9 DERNIERS MOIS) ---\n")

    sql = """
        SELECT
            m.nom AS modele,
            m.description,
            COUNT(DISTINCT r.idResultat) AS nb_resultats,
            COUNT(DISTINCT h.date) AS nb_interactions,
            (COUNT(DISTINCT r.idResultat) + COUNT(DISTINCT h.date)) AS total_utilisations
        FROM Modele m
        LEFT JOIN Resultat r
               ON r.nom = m.nom
              AND r.dateDebut >= CURRENT_DATE - INTERVAL '9 months'
        LEFT JOIN HistoriqueUtilisation h
               ON h.nom = m.nom
              AND h.date >= CURRENT_DATE - INTERVAL '9 months'
        GROUP BY m.nom, m.description
        ORDER BY total_utilisations DESC;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            if not rows:
                print("Aucune donnée disponible.\n")
                return

            for nom, desc, nb_res, nb_inter, total in rows:
                print(f"• Modèle : {nom}")
                print(f"  Description : {desc}")
                print(f"  Résultats : {nb_res}")
                print(f"  Interactions : {nb_inter}")
                print(f"  Total utilisations : {total}\n")

    except Exception as e:
        print("Erreur SQL :", e)



def collaborationsActivesModeles(conn):

    print("\n--- COLLABORATIONS ACTIVES ---\n")

    sql = """
        SELECT
            emailA,
            emailB,
            nom AS modele,
            dateDebut,
            dateFin
        FROM Collaboration
        WHERE dateFin >= CURRENT_DATE
        ORDER BY dateDebut DESC;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            if not rows:
                print("Aucune collaboration active.\n")
                return

            for emailA, emailB, modele, debut, fin in rows:
                print(f"• {emailA} ↔ {emailB}")
                print(f"  Modèle : {modele}")
                print(f"  Début : {debut}")
                print(f"  Fin : {fin}\n")

    except Exception as e:
        print("Erreur SQL :", e)

# Version Jad
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
from datetime import date

def ajouterModele(conn):

    print("\n--- AJOUTER UN NOUVEAU MODELE ---\n")

    nom = input("Nom du modèle : ").strip()
    descript = input("Description du modèle : ").strip()
    dateCreation = date.today()

    # Types autorisés
    types_modele = ["image", "texte", "video"]

    type_modele = input("Type de modèle (image / texte / video) : ").lower()
    while type_modele not in types_modele:
        print("Valeur invalide. Veuillez entrer : image, texte ou video.")
        type_modele = input("Type de modèle (image / texte / video) : ").lower()

    # Initialisation (important : None → NULL en SQL)
    longueur = None
    resolution = None
    duree = None

    try:
        if type_modele == "texte":
            longueur = int(input("Longueur maximum (en mots) : "))
            if longueur <= 0:
                raise ValueError

        elif type_modele == "image":
            resolution = int(input("Résolution (en pixels) : "))
            if resolution <= 0:
                raise ValueError

        elif type_modele == "video":
            resolution = int(input("Résolution (en pixels) : "))
            duree = int(input("Durée moyenne de génération (en secondes) : "))
            if resolution <= 0 or duree <= 0:
                raise ValueError

    except ValueError:
        print("\nErreur : valeurs numériques invalides (doivent être strictement positives).\n")
        return

    try:
        with conn.cursor() as cur:
            sql = """
                INSERT INTO Modele
                (nom, description, dateCreation, TypeModele,
                 longueurMax, resolution, duree)
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

        

def creerUtilisateur(conn):

    print("\n--- CRÉER UN NOUVEL UTILISATEUR ---\n")

    email = input("Email : ").strip()
    nom = input("Nom : ").strip()
    mot_de_passe = input("Mot de passe : ").strip()
    date_inscription = date.today()

    # Type utilisateur
    type_user = input("Type utilisateur (normal / premium) : ").lower()
    while type_user not in ['normal', 'premium']:
        type_user = input("Valeur invalide. Entrez 'normal' ou 'premium' : ").lower()

    # Application stricte des règles métier
    if type_user == 'premium':
        qualite = input("Qualité de génération (moyenne / haute) : ").lower()
        while qualite not in ['moyenne', 'haute']:
            qualite = input("Valeur invalide. Choisir 'moyenne' ou 'haute' : ").lower()
        hors_ligne = True
    else:
        qualite = 'moyenne'
        hors_ligne = False

    try:
        with conn.cursor() as cur:

            # Vérification d'existence
            cur.execute(
                "SELECT 1 FROM Utilisateur WHERE email = %s",
                (email,)
            )

            if cur.fetchone():
                print("\n Un utilisateur avec cet email existe déjà.\n")
                return

            # Insertion conforme au MLD
            cur.execute("""
                INSERT INTO Utilisateur
                (email, nom, motDePasse, dateInscription,
                 TypeUtilisateur, qualiteGeneration, horsLigneAutorise)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                email,
                nom,
                mot_de_passe,
                date_inscription,
                type_user,
                qualite,
                hors_ligne
            ))

            conn.commit()

            print("\n Utilisateur créé avec succès :")
            print(f"  → Email : {email}")
            print(f"  → Nom : {nom}")
            print(f"  → Date d'inscription : {date_inscription}")
            print(f"  → Type : {type_user}")
            print(f"  → Qualité : {qualite}")
            print(f"  → Hors-ligne : {hors_ligne}\n")

    except Exception as e:
        conn.rollback()
        print("Erreur SQL :", e)

def afficherToutesLesEvaluations(conn):

    print("\n--- LISTE DE TOUTES LES ÉVALUATIONS ---\n")

    sql = """
        SELECT
            e.idResultat,
            e.email,
            r.nom AS modele,
            e.note,
            e.commentaire,
            e.date
        FROM Evaluation e
        JOIN Resultat r
            ON e.idResultat = r.idResultat
        ORDER BY e.date DESC;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            if not rows:
                print("Aucune évaluation enregistrée.\n")
                return

            for id_res, email, modele, note, commentaire, date_eval in rows:
                print(f"• ID Résultat : {id_res}")
                print(f"  Utilisateur : {email}")
                print(f"  Modèle : {modele}")
                print(f"  Date : {date_eval}")
                print(f"  Note : {note}/5")
                print(f"  Commentaire : {commentaire if commentaire else 'Aucun'}\n")

    except Exception as e:
        conn.rollback()
        print("Erreur SQL :", e)

