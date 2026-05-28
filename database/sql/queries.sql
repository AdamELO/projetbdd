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
GROUP BY u.IdUtilisateur, u.Nom
HAVING COUNT(DISTINCT r.Code) >= 3;

-- Le cours ayant le plus de résumés publiés
SELECT r.Code, c.Nom AS name, COUNT(*) AS summary_count
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
    SELECT r.Id, r.Code, r.Titre AS title,
           AVG(e.Note) AS avg_rating,
           RANK() OVER (PARTITION BY r.Code ORDER BY AVG(e.Note) DESC) AS rank
    FROM Resume r
    JOIN Evaluation e ON r.Id = e.IdResume
    GROUP BY r.Id, r.Code, r.Titre
)
SELECT code, title, avg_rating
FROM notes
WHERE rank = 1
ORDER BY code;

-- Les utilisateurs n'ayant jamais publié de résumé
SELECT u.IdUtilisateur AS id, u.Nom AS name
FROM Utilisateur u
WHERE NOT EXISTS (
    SELECT 1 FROM Contribution c
    JOIN Resume r ON c.Id = r.Id
    WHERE c.IdUtilisateur = u.IdUtilisateur
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
    LEFT JOIN Contribution c ON u.IdUtilisateur = c.IdUtilisateur
    LEFT JOIN Resume r ON c.Id = r.Id
    GROUP BY u.IdUtilisateur
) AS subquery;
