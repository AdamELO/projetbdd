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