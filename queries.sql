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
ORDER BY NbResumes DESC
LIMIT 1;

-- 4. Les résumés les mieux notés (note moyenne maximale) pour chaque cours
SELECT r.Code, r.Titre, AVG(e.Note) AS NoteMoyenne
FROM Resume r
JOIN Evaluation e ON r.Id = e.IdResume
GROUP BY r.Id, r.Code, r.Titre
HAVING AVG(e.Note) = (
    SELECT MAX(avg_note) FROM (
        SELECT AVG(e2.Note) AS avg_note
        FROM Resume r2
        JOIN Evaluation e2 ON r2.Id = e2.IdResume
        WHERE r2.Code = r.Code
        GROUP BY r2.Id
    ) AS sous_requete
);

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
       COALESCE(SUM(oc.Prix), 0) AS PointsDepenses
FROM Utilisateur u
JOIN Transaction t ON u.IdUtilisateur = t.IdUtilisateur
JOIN ObjetCosmetique oc ON t.IdObjetCosmetique = oc.Id
GROUP BY u.IdUtilisateur, u.Nom, u.Points
HAVING COALESCE(SUM(oc.Prix), 0) > u.Points;

-- 8. Le nombre moyen de résumés publiés par utilisateur
SELECT ROUND(AVG(NbResumes), 2) AS MoyenneResumesParUtilisateur
FROM (
    SELECT u.IdUtilisateur, COUNT(r.Id) AS NbResumes
    FROM Utilisateur u
    LEFT JOIN Contribution c ON u.IdUtilisateur = c.IdUtilisateur
    LEFT JOIN Resume r ON c.Id = r.Id
    GROUP BY u.IdUtilisateur
) AS sous_requete;