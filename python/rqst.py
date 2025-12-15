

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

