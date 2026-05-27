-- Les 10 utilisateurs ayant le plus de points
SELECT u.IdUtilisateur, u.Nom, u.Niveau, u.Points
FROM Utilisateur u
ORDER BY u.Points DESC
LIMIT 10;

-- Les utilisateurs ayant publié des résumés dans au moins 3 cours différents
SELECT u.IdUtilisateur AS id, u.Nom AS nom, COUNT(DISTINCT r.Code) AS nb_cours
FROM Utilisateur u
JOIN Contribution c ON u.IdUtilisateur = c.IdUtilisateur
JOIN Resume r ON c.Id = r.Id
GROUP BY u.IdUtilisateur, u.Nom
HAVING COUNT(DISTINCT r.Code) >= 3;

-- Le cours ayant le plus de résumés publiés
SELECT r.Code AS code, c.Nom AS nom, COUNT(*) AS nb_resumes
FROM Resume r
JOIN Cours c ON r.Code = c.Code
GROUP BY r.Code, c.Nom
HAVING COUNT(*) = (
    SELECT MAX(cnt) FROM (
        SELECT COUNT(*) AS cnt FROM Resume GROUP BY Code
    ) AS m
);

-- Les résumés les mieux notés (note moyenne maximale) pour chaque cours
WITH notes AS (
    SELECT r.Id, r.Code AS code, r.Titre AS titre,
           AVG(e.Note) AS note_moyenne,
           RANK() OVER (PARTITION BY r.Code ORDER BY AVG(e.Note) DESC) AS rang
    FROM Resume r
    JOIN Evaluation e ON r.Id = e.IdResume
    GROUP BY r.Id, r.Code, r.Titre
)
SELECT code, titre, note_moyenne
FROM notes
WHERE rang = 1
ORDER BY code;

-- Les utilisateurs n'ayant jamais publié de résumé
SELECT u.IdUtilisateur AS id, u.Nom AS nom
FROM Utilisateur u
WHERE NOT EXISTS (
    SELECT 1 FROM Contribution c
    JOIN Resume r ON c.Id = r.Id
    WHERE c.IdUtilisateur = u.IdUtilisateur
);

-- L'objet cosmétique le plus acheté
SELECT oc.Id AS id, oc.Nom AS nom, COUNT(*) AS nb_achats
FROM Transaction t
JOIN ObjetCosmetique oc ON t.IdObjetCosmetique = oc.Id
GROUP BY oc.Id, oc.Nom
ORDER BY nb_achats DESC
LIMIT 1;

-- Les utilisateurs ayant dépensé plus de points qu'ils n'en ont disponibles
SELECT u.IdUtilisateur AS id, 
       u.Nom AS nom, 
       u.Points AS points_disponibles,
       ABS(SUM(CASE WHEN t.Montant < 0 THEN t.Montant ELSE 0 END)) AS points_depenses
FROM Utilisateur u
JOIN Transaction t ON u.IdUtilisateur = t.IdUtilisateur
GROUP BY u.IdUtilisateur, u.Nom, u.Points
HAVING ABS(SUM(CASE WHEN t.Montant < 0 THEN t.Montant ELSE 0 END)) > u.Points;

-- Le nombre moyen de résumés publiés par utilisateur
SELECT ROUND(AVG(nb_resumes), 2) AS moyenne
FROM (
    SELECT u.IdUtilisateur, COUNT(r.Id) AS nb_resumes
    FROM Utilisateur u
    LEFT JOIN Contribution c ON u.IdUtilisateur = c.IdUtilisateur
    LEFT JOIN Resume r ON c.Id = r.Id
    GROUP BY u.IdUtilisateur
) AS sous_requete;