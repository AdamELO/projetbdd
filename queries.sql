-- 1. Les 10 utilisateurs ayant le plus de points
SELECT IdUtilisateur, Nom, Points
FROM Utilisateur
ORDER BY Points DESC
LIMIT 10;

-- 2. Les utilisateurs ayant publié des résumés dans au moins 3 cours différents
SELECT u.IdUtilisateur, u.Nom, COUNT(DISTINCT r.Code) AS NbCours
FROM Utilisateur u
JOIN Contribution c ON u.IdUtilisateur = c.IdUtilisateur
JOIN Resume r ON c.Id = r.Id
GROUP BY u.IdUtilisateur, u.Nom
HAVING COUNT(DISTINCT r.Code) >= 3;

-- 3. Le cours ayant le plus de résumés publiés
SELECT r.Code, c.Nom, COUNT(*) AS NbResumes
FROM Resume r
JOIN Cours c ON r.Code = c.Code
GROUP BY r.Code, c.Nom
HAVING COUNT(*) = (
    SELECT MAX(cnt) FROM (
        SELECT COUNT(*) AS cnt FROM Resume GROUP BY Code
    ) AS m
);

-- 4. Les résumés les mieux notés (note moyenne maximale) pour chaque cours
WITH notes AS (
    SELECT r.Id, r.Code, r.Titre,
           AVG(e.Note) AS NoteMoyenne,
           RANK() OVER (PARTITION BY r.Code ORDER BY AVG(e.Note) DESC) AS rang
    FROM Resume r
    JOIN Evaluation e ON r.Id = e.IdResume
    GROUP BY r.Id, r.Code, r.Titre
)
SELECT Code, Titre, NoteMoyenne
FROM notes
WHERE rang = 1
ORDER BY Code;

-- 5. Les utilisateurs n'ayant jamais publié de résumé
SELECT u.IdUtilisateur, u.Nom
FROM Utilisateur u
WHERE u.IdUtilisateur NOT IN (
    SELECT DISTINCT c.IdUtilisateur
    FROM Contribution c
    JOIN Resume r ON c.Id = r.Id
);

-- 6. L'objet cosmétique le plus acheté
SELECT oc.Id, oc.Nom, COUNT(*) AS NbAchats
FROM Transaction t
JOIN ObjetCosmetique oc ON t.IdObjetCosmetique = oc.Id
GROUP BY oc.Id, oc.Nom
ORDER BY NbAchats DESC
LIMIT 1;

-- 7. Les utilisateurs ayant dépensé plus de points qu'ils n'en ont disponibles
SELECT u.IdUtilisateur, u.Nom, u.Points,
       ABS(SUM(CASE WHEN t.Montant < 0 THEN t.Montant ELSE 0 END)) AS PointsDepenses,
       SUM(CASE WHEN t.Montant > 0 THEN t.Montant ELSE 0 END) AS PointsGagnes
FROM Utilisateur u
JOIN Transaction t ON u.IdUtilisateur = t.IdUtilisateur
GROUP BY u.IdUtilisateur, u.Nom, u.Points
HAVING ABS(SUM(CASE WHEN t.Montant < 0 THEN t.Montant ELSE 0 END)) 
     > SUM(CASE WHEN t.Montant > 0 THEN t.Montant ELSE 0 END);
     
-- 8. Le nombre moyen de résumés publiés par utilisateur
SELECT ROUND(AVG(NbResumes), 2) AS MoyenneResumesParUtilisateur
FROM (
    SELECT u.IdUtilisateur, COUNT(r.Id) AS NbResumes
    FROM Utilisateur u
    LEFT JOIN Contribution c ON u.IdUtilisateur = c.IdUtilisateur
    LEFT JOIN Resume r ON c.Id = r.Id
    GROUP BY u.IdUtilisateur
) AS sous_requete;