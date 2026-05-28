from database.db import get_connection

def get_all_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT c.Code, c.Nom as name, c.Faculte as faculty,
           COUNT(r.Id) as summary_count
    FROM Cours c
    LEFT JOIN (
        SELECT r.Id, r.Code
        FROM Resume r
        JOIN Contribution co ON r.Id = co.Id
        WHERE r.Visibilite = 'public' AND co.EstSupprime = FALSE
    ) r ON c.Code = r.Code
    GROUP BY c.Code, c.Nom, c.Faculte
    ORDER BY c.Code
""")
    results = cur.fetchall()
    conn.close()
    return results

def get_summaries_by_course(code):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.Id, r.Titre AS title, c.Date,
               ROUND(AVG(e.Note), 1) as note,
               COUNT(e.Id) as comment_count
        FROM Resume r
        JOIN Contribution c ON r.Id = c.Id
        LEFT JOIN Evaluation e ON r.Id = e.IdResume
        WHERE r.Code = %s AND r.Visibilite = 'public' AND c.EstSupprime = FALSE
        GROUP BY r.Id, r.Titre, c.Date
        ORDER BY c.Date DESC
    """, (code,))
    results = cur.fetchall()
    conn.close()
    return results

def get_summary_by_id(summary_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.Id, r.Titre as title, r.Code as course_code,
               co.Nom as course_name, c.Date,
               u.Nom as author,
               ROUND(AVG(e.Note), 1) as note,
               COUNT(DISTINCT e.Id) as comment_count
        FROM Resume r
        JOIN Cours co ON r.Code = co.Code
        JOIN Contribution c ON r.Id = c.Id
        JOIN Utilisateur u ON c.IdUtilisateur = u.IdUtilisateur
        LEFT JOIN Evaluation e ON r.Id = e.IdResume
        WHERE r.Id = %s AND r.Visibilite = 'public' AND c.EstSupprime = FALSE
        GROUP BY r.Id, r.Titre, r.Code, co.Nom, c.Date, u.Nom
    """, (summary_id,))
    result = cur.fetchone()
    conn.close()
    return result

def get_evaluations_by_summary(summary_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT u.Nom as name,
           e.Note as rating, e.Commentaire as comment,
           obj.Nom as title
    FROM Evaluation e
    JOIN Contribution c ON e.Id = c.Id
    JOIN Utilisateur u ON c.IdUtilisateur = u.IdUtilisateur
    LEFT JOIN (
        SELECT obju.IdUtilisateur, MIN(obju.IdObjet) AS IdObjet
        FROM ObjetUtilisateur obju
        JOIN Titre t ON obju.IdObjet = t.Id
        WHERE obju.EstActif = TRUE
        GROUP BY obju.IdUtilisateur
    ) active_title ON u.IdUtilisateur = active_title.IdUtilisateur
    LEFT JOIN Objet obj ON active_title.IdObjet = obj.Id
    WHERE e.IdResume = %s AND c.EstSupprime = FALSE
    ORDER BY e.Id DESC
    """, (summary_id,))
    results = cur.fetchall()
    conn.close()
    return results

def add_course(code, name, faculty, credits):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Cours (Code, Nom, Faculte, Credits)
            VALUES (%s, %s, %s, %s)
        """, (code, name, faculty, credits))
        conn.commit()
        return True
    except Exception as e:
        print(f"ERROR add_course: {e}", flush=True)
        conn.rollback()
        return False
    finally:
        conn.close()
