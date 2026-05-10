from db import get_connection

# Requête 1 : Les 10 utilisateurs ayant le plus de points
def top_10_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT IdUtilisateur as id, Nom as nom, Niveau as niveau, Points as points
        FROM Utilisateur
        ORDER BY Points DESC
        LIMIT 10
    """)
    results = cur.fetchall()
    conn.close()
    return results

# Requête 2 : Les utilisateurs ayant publié des résumés dans au moins 3 cours différents
def users_min_3_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.IdUtilisateur as id, u.Nom as nom, COUNT(DISTINCT r.Code) as nb_cours
        FROM Utilisateur u
        JOIN Contribution c ON u.IdUtilisateur = c.IdUtilisateur
        JOIN Resume r ON c.Id = r.Id
        GROUP BY u.IdUtilisateur, u.Nom
        HAVING COUNT(DISTINCT r.Code) >= 3
        ORDER BY nb_cours DESC
    """)
    results = cur.fetchall()
    conn.close()
    return results

# Requête 3 : Le cours ayant le plus de résumés publiés
def most_summarized_course():
    conn = get_connection()
    cur = conn.cursor()
    # On utilise une sous-requête pour trouver le MAX du COUNT
    cur.execute("""
        SELECT r.Code as code, c.Nom as nom, COUNT(*) as nb_resumes
        FROM Resume r
        JOIN Cours c ON r.Code = c.Code
        GROUP BY r.Code, c.Nom
        HAVING COUNT(*) = (
            SELECT MAX(cnt) 
            FROM (SELECT COUNT(*) as cnt FROM Resume GROUP BY Code)
        )
    """)
    results = cur.fetchall() # On utilise fetchall car il peut y en avoir plusieurs
    conn.close()
    return results

# Requête 4 : Les résumés les mieux notés pour chaque cours
def best_rated_resumes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        WITH Moyennes AS (
            SELECT r.Code, r.Titre, ROUND(AVG(e.Note), 2) as note_moyenne
            FROM Resume r
            JOIN Evaluation e ON r.Id = e.IdResume
            GROUP BY r.Id, r.Code, r.Titre
        )
        SELECT m1.Code as code, m1.Titre as titre, CAST(m1.note_moyenne AS FLOAT) as note_moyenne
        FROM Moyennes m1
        WHERE m1.note_moyenne = (
            SELECT MAX(m2.note_moyenne)
            FROM Moyennes m2
            WHERE m2.Code = m1.Code
        )
        ORDER BY m1.Code
    """)
    results = cur.fetchall()
    conn.close()
    return [dict(row) for row in results]

# Requête 5 : Les utilisateurs n'ayant jamais publié de résumé
def users_no_resume():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.IdUtilisateur as id, u.Nom as nom
        FROM Utilisateur u
        WHERE u.IdUtilisateur NOT IN (
            SELECT DISTINCT c.IdUtilisateur
            FROM Contribution c
            JOIN Resume r ON c.Id = r.Id
        )
        ORDER BY u.Nom
    """)
    results = cur.fetchall()
    conn.close()
    return [dict(row) for row in results]


# Requête 6 : L'objet cosmétique le plus acheté
def most_bought_item():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT oc.Id as id, oc.Nom as nom, COUNT(*) as nb_achats
        FROM Transaction t
        JOIN ObjetCosmetique oc ON t.IdObjetCosmetique = oc.Id
        GROUP BY oc.Id, oc.Nom
        ORDER BY nb_achats DESC
        LIMIT 1
    """)
    result = cur.fetchone()
    conn.close()
    return result

# Requête 7 : Les utilisateurs ayant dépensé plus de points qu'ils n'en ont
def users_overspent():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.IdUtilisateur as id, u.Nom as nom, u.Points as points,
               COALESCE(SUM(oc.Prix), 0) as points_depenses
        FROM Utilisateur u
        JOIN Transaction t ON u.IdUtilisateur = t.IdUtilisateur
        JOIN ObjetCosmetique oc ON t.IdObjetCosmetique = oc.Id
        GROUP BY u.IdUtilisateur, u.Nom, u.Points
        HAVING COALESCE(SUM(oc.Prix), 0) > u.Points
        ORDER BY points_depenses DESC
    """)
    results = cur.fetchall()
    conn.close()
    return results

# Requête 8 : Le nombre moyen de résumés publiés par utilisateur
def avg_resumes_per_user():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ROUND(AVG(nb_resumes), 2) as moyenne
        FROM (
            SELECT u.IdUtilisateur, COUNT(r.Id) as nb_resumes
            FROM Utilisateur u
            LEFT JOIN Contribution c ON u.IdUtilisateur = c.IdUtilisateur
            LEFT JOIN Resume r ON c.Id = r.Id
            GROUP BY u.IdUtilisateur
        ) as sous_requete
    """)
    result = cur.fetchone()
    conn.close()
    return result