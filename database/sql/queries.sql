-- Les 10 utilisateurs ayant le plus de points
SELECT u.IdUtilisateur AS id, u.Nom AS name, u.Niveau AS level, u.Points
FROM Utilisateur u
ORDER BY u.Points DESC
LIMIT 10;

-- Les utilisateurs ayant publié des résumés dans au moins 3 cours différents
SELECT u.IdUtilisateur AS id, u.Nom AS name, COUNT(DISTINCT r.Code) AS course_count
FROM Utilisateur u
JOIN Contribution c ON u.IdUtilisateur = c.IdUtilisateur
JOIN Resume r ON c.Id = r.Id
WHERE c.EstSupprime = FALSE
GROUP BY u.IdUtilisateur, u.Nom
HAVING COUNT(DISTINCT r.Code) >= 3;

-- Le cours ayant le plus de résumés publiés
SELECT r.Code, co.Nom AS name, COUNT(*) AS summary_count
FROM Resume r
JOIN Contribution c ON r.Id = c.Id
JOIN Cours co ON r.Code = co.Code
WHERE c.EstSupprime = FALSE
GROUP BY r.Code, co.Nom
HAVING COUNT(*) = (
    SELECT MAX(cnt) FROM (
        SELECT COUNT(*) AS cnt
        FROM Resume r2
        JOIN Contribution c2 ON r2.Id = c2.Id
        WHERE c2.EstSupprime = FALSE
        GROUP BY r2.Code
    ) AS m
);

-- Les résumés les mieux notés (note moyenne maximale) pour chaque cours
SELECT r.Code, r.Titre, AVG(e.Note)
FROM Resume r
JOIN Contribution c ON r.Id = c.Id
JOIN Evaluation e ON r.Id = e.IdResume
WHERE c.EstSupprime = FALSE
GROUP BY r.Id, r.Code, r.Titre
HAVING AVG(e.Note) = (
    SELECT MAX(avg_note)
    FROM (
        SELECT AVG(e2.Note) AS avg_note
        FROM Resume r2
        JOIN Contribution c2 ON r2.Id = c2.Id
        JOIN Evaluation e2 ON r2.Id = e2.IdResume
        WHERE c2.EstSupprime = FALSE
        AND r2.Code = r.Code
        GROUP BY r2.Id
    ) sub
)
ORDER BY r.Code;

-- Les utilisateurs n'ayant jamais publié de résumé
SELECT u.IdUtilisateur AS id, u.Nom AS name
FROM Utilisateur u
WHERE NOT EXISTS (
    SELECT 1 FROM Contribution c
    JOIN Resume r ON c.Id = r.Id
    WHERE c.IdUtilisateur = u.IdUtilisateur AND c.EstSupprime = FALSE
);

-- L'objet cosmétique le plus acheté
SELECT o.Id, o.Nom AS name, COUNT(*) AS purchase_count
FROM Transaction t
JOIN Objet o ON t.IdObjet = o.Id
GROUP BY o.Id, o.Nom
ORDER BY purchase_count DESC
LIMIT 1;

-- Les utilisateurs ayant dépensé plus de points qu'ils n'en ont disponibles
SELECT u.IdUtilisateur AS id,
       u.Nom AS name,
       u.Points,
       ABS(SUM(CASE WHEN t.Montant < 0 THEN t.Montant ELSE 0 END)) AS points_spent
FROM Utilisateur u
JOIN Transaction t ON u.IdUtilisateur = t.IdUtilisateur
GROUP BY u.IdUtilisateur, u.Nom, u.Points
HAVING ABS(SUM(CASE WHEN t.Montant < 0 THEN t.Montant ELSE 0 END)) > u.Points;

-- Le nombre moyen de résumés publiés par utilisateur
SELECT ROUND(AVG(summary_count), 2) AS average
FROM (
    SELECT u.IdUtilisateur, COUNT(r.Id) AS summary_count
    FROM Utilisateur u
    LEFT JOIN Contribution c ON u.IdUtilisateur = c.IdUtilisateur AND c.EstSupprime = FALSE
    LEFT JOIN Resume r ON c.Id = r.Id
    GROUP BY u.IdUtilisateur
) AS subquery;
