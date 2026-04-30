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