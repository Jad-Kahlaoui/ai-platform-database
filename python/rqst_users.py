def ajouterEvaluation(conn, email_utilisateur):
    """
    Permet à l'utilisateur connecté d'ajouter une évaluation en indiquant :
    - l'id du résultat à évaluer
    - la note (1 à 5)
    - un commentaire
    La date est automatiquement la date actuelle.
    """
    try:
        # Demander l'id du résultat
        while True:
            try:
                id_resultat = int(input("Entrez l'ID du résultat à évaluer : "))
                break
            except ValueError:
                print("Veuillez entrer un nombre entier valide pour l'ID.")

        # Demander la note
        while True:
            try:
                note = int(input("Entrez la note (1 à 5) : "))
                if 1 <= note <= 5:
                    break
                else:
                    print("La note doit être comprise entre 1 et 5.")
            except ValueError:
                print("Veuillez entrer un nombre entier valide pour la note.")

        # Demander un commentaire
        commentaire = input("Entrez votre commentaire : ").strip()

        # Insertion dans la base
        sql = """
            INSERT INTO Evaluation (email, idResultat, date, note, commentaire)
            VALUES (%s, %s, NOW(), %s, %s);
        """

        with conn.cursor() as cur:
            cur.execute(sql, (email_utilisateur, id_resultat, note, commentaire))
            conn.commit()
            print("Évaluation ajoutée avec succès !\n")

    except Exception as e:
        print("Erreur SQL :", e)



def afficherMonHistorique(conn, email_utilisateur):
    print(f"\n--- MON HISTORIQUE D'UTILISATION ({email_utilisateur}) ---\n")
    sql = """
        SELECT 
            nom,
            typeInteraction,
            date
        FROM HistoriqueUtilisation
        WHERE email = %s
        ORDER BY date DESC;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql, (email_utilisateur,))
            rows = cur.fetchall()
            if not rows:
                print("Historique vide.\n")
                return
            for modele, type_int, date_hist in rows:
                print(f"• [{date_hist}] {type_int.upper()} sur le modèle '{modele}'")
            print() 
    except Exception as e:
        print("Erreur SQL :", e)


def afficherMesResultats(conn, email_utilisateur):
    print(f"\n--- MES RÉSULTATS GÉNÉRÉS ({email_utilisateur}) ---\n")
    
    sql = """
        SELECT 
            r.nom AS modele,
            r.dateDebut,
            r.idResultat,
            STRING_AGG(m.cle || ': ' || m.valeur, ', ') AS metadonnees
        FROM Resultat r
        LEFT JOIN MetaDonnee m ON r.idResultat = m.idResultat
        WHERE r.email = %s
        GROUP BY r.idResultat, r.nom, r.dateDebut
        ORDER BY r.dateDebut DESC;
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (email_utilisateur,))
            rows = cur.fetchall()
            if not rows:
                print("Aucun résultat généré.\n")
                return
            for modele, date_deb, id_resultat, metas in rows:
                print(f"• Modèle : {modele}")
                print(f"  ID Résultat : {id_resultat}")
                print(f"  Date : {date_deb}")
                print(f"  Détails : {metas if metas else 'N/A'}\n")
    except Exception as e:
        print("Erreur SQL :", e)


def afficherMesCollaborations(conn, email_utilisateur):
    print(f"\n--- MES COLLABORATIONS ({email_utilisateur}) ---\n")
    sql = """
        SELECT 
            CASE 
                WHEN emailA = %s THEN emailB 
                ELSE emailA 
            END AS partenaire,
            nom,
            dateDebut,
            dateFin
        FROM Collaboration
        WHERE emailA = %s OR emailB = %s
        ORDER BY dateDebut DESC;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql, (email_utilisateur, email_utilisateur, email_utilisateur))
            rows = cur.fetchall()

            if not rows:
                print("Aucune collaboration enregistrée.\n")
                return

            for partenaire, modele, debut, fin in rows:
                print(f"• Avec : {partenaire}")
                print(f"  Sur le modèle : {modele}")
                print(f"  Période : Du {debut} au {fin}\n")

    except Exception as e:
        print("Erreur SQL :", e)


def afficherTousLesModeles(conn):
    print("\n--- CATALOGUE DES MODÈLES DISPONIBLES ---\n")
    sql = """
        SELECT 
            nom,
            description,
            TypeModele,
            longueurMax,
            resolution,
            duree
        FROM Modele
        ORDER BY nom ASC;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            if not rows:
                print("Aucun modèle disponible dans la base.\n")
                return

            for nom, desc, type_m, l_max, res, dur in rows:
                print(f"• [{type_m.upper()}] {nom}")
                print(f"  Description : {desc}")

                if type_m == 'texte' and l_max:
                    print(f"  Limite : {l_max} mots")
                elif type_m == 'image' and res:
                    print(f"  Résolution : {res} px")
                elif type_m == 'video' and dur:
                    print(f"  Durée max : {dur} sec")
                
                print()

    except Exception as e:
        print("Erreur SQL :", e)