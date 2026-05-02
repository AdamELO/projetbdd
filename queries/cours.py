from db import get_connection

def get_all_cours():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.Code as code, c.Nom as nom, c.Faculte as faculte,
               COUNT(r.Id) as nb_resumes
        FROM Cours c
        LEFT JOIN Resume r ON c.Code = r.Code
        GROUP BY c.Code, c.Nom, c.Faculte
        ORDER BY c.Code
    """)
    results = cur.fetchall()
    conn.close()
    return [dict(row) for row in results]

def get_resumes_by_cours(code):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.Id as id, r.Titre as titre, c.Date as date,
               ROUND(AVG(e.Note), 1) as note,
               COUNT(e.Id) as nb_commentaires
        FROM Resume r
        JOIN Contribution c ON r.Id = c.Id
        LEFT JOIN Evaluation e ON r.Id = e.IdResume
        WHERE r.Code = %s
        GROUP BY r.Id, r.Titre, c.Date
        ORDER BY c.Date DESC
    """, (code,))
    results = cur.fetchall()
    conn.close()
    return [dict(row) for row in results]

def get_resume_by_id(resume_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.Id as id, r.Titre as titre, r.Code as code_cours,
               co.Nom as nom_cours, c.Date as date,
               u.Nom as auteur,
               ROUND(AVG(e.Note), 1) as note,
               COUNT(DISTINCT e.Id) as nb_commentaires
        FROM Resume r
        JOIN Cours co ON r.Code = co.Code
        JOIN Contribution c ON r.Id = c.Id
        JOIN Utilisateur u ON c.IdUtilisateur = u.IdUtilisateur
        LEFT JOIN Evaluation e ON r.Id = e.IdResume
        WHERE r.Id = %s
        GROUP BY r.Id, r.Titre, r.Code, co.Nom, c.Date, u.Nom
    """, (resume_id,))
    result = cur.fetchone()
    conn.close()
    return dict(result) if result else None

def get_evaluations_by_resume(resume_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT u.Nom as name,
           e.Note as rating, e.Commentaire as comment
    FROM Evaluation e
    JOIN Contribution c ON e.Id = c.Id
    JOIN Utilisateur u ON c.IdUtilisateur = u.IdUtilisateur
    WHERE e.IdResume = %s
    ORDER BY e.Id DESC
    """, (resume_id,))
    results = cur.fetchall()
    conn.close()
    return [dict(row) for row in results]


def add_cours(code, nom, faculte, credits):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Cours (Code, Nom, Faculte, Credits)
            VALUES (%s, %s, %s, %s)
        """, (code, nom, faculte, credits))
        conn.commit()
        return True
    except Exception as e:
        print(f"ERREUR add_cours: {e}", flush=True)
        conn.rollback()
        return False
    finally:
        conn.close()