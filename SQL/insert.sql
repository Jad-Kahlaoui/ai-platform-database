USERS

SELECT nom, description from modele


INSERT INTO Evaluation (email, idResultat, date, note, commentaire)
VALUES (
    'utilisateur@example.com',  
    123,                       
    CURRENT_DATE,               
    5,                          
    'Excellent résultat'        
);



UPDATE Evaluation
SET note = 4,                 
    commentaire = 'Bien joué' 
WHERE email = 'utilisateur@example.com'
  AND idResultat = 123;       


SELECT
    r.idResultat,
    r.nom AS modele,
    m.description AS description_modele,
    r.dateDebut,
    e.note,
    e.commentaire
FROM Resultat r
JOIN Modele m ON r.nom = m.nom
LEFT JOIN Evaluation e
    ON r.idResultat = e.idResultat
   AND e.email = r.email
WHERE r.email = 'diane@gmail.com'
ORDER BY r.dateDebut DESC;

UPDATE Utilisateur
SET motDePasse = '321'
WHERE email = 'alice@gmail.com';



ADMIN 

DELETE FROM Utilisateur
WHERE email = 'charlie@gmail.com';


ajouter un modele

enlever un commentaire

passer qql en premium









1)
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



2) 
SELECT 
    u.email,
    u.nom,
    COUNT(r.idResultat) AS nb_resultats
FROM Utilisateur u
JOIN Resultat r
    ON u.email = r.email
GROUP BY u.email, u.nom
ORDER BY nb_resultats DESC;

3)
SELECT 
    nom,
    TypeModele,
    longueurMax,
    duree
FROM Modele
WHERE 
      (duree IS NOT NULL AND duree > 300)     -- vidéos > 5 minutes
   OR (longueurMax IS NOT NULL AND longueurMax > 1000);  -- textes > 1000 mots

4)

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


5)

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



OU ALORS


SELECT
    m.nom AS modele,
    m.description,
    COUNT(DISTINCT r.idResultat) AS nb_resultats,
    COUNT(DISTINCT h.date) AS nb_interactions,
    (COUNT(DISTINCT r.idResultat) + COUNT(DISTINCT h.date)) AS total_utilisations
FROM Modele m
LEFT JOIN Resultat r
       ON r.nom = m.nom
      AND r.dateDebut >= '2025-10-17'
LEFT JOIN HistoriqueUtilisation h
       ON h.nom = m.nom
      AND h.date >= '2025-10-17'
GROUP BY m.nom, m.description
ORDER BY total_utilisations DESC;



OU ALORS



SELECT
    m.nom AS modele,
    m.description,
    COUNT(DISTINCT r.idResultat) AS nb_resultats,
    COUNT(DISTINCT h.date) AS nb_interactions,
    (COUNT(DISTINCT r.idResultat) + COUNT(DISTINCT h.date)) AS total_utilisations
FROM Modele m
LEFT JOIN Resultat r
       ON r.nom = m.nom
      AND CURRENT_DATE - r.dateDebut <= 30
LEFT JOIN HistoriqueUtilisation h
       ON h.nom = m.nom
      AND CURRENT_DATE - h.date <= 30
GROUP BY m.nom, m.description
ORDER BY total_utilisations DESC;



6)

SELECT
    emailA,
    emailB,
    nom AS modele,
    dateDebut,
    dateFin
FROM Collaboration
WHERE dateFin >= CURRENT_DATE
ORDER BY dateDebut DESC;


