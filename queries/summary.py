from database.db import get_connection
from queries.user import award_points, update_level

def add_summary(title, description, course_code, user_id, file_bytes=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Contribution (IdUtilisateur)
            VALUES (%s)
            RETURNING Id
        """, (user_id,))
        contribution_id = cur.fetchone()['id']

        cur.execute("""
            INSERT INTO Resume (Id, Titre, Description, Code, Fichier)
            VALUES (%s, %s, %s, %s, %s)
        """, (contribution_id, title, description, course_code, file_bytes))

        award_points(user_id, 300, contribution_id, cur)
        update_level(user_id, cur)
        conn.commit()
        return True
    except Exception as e:
        print(f"ERROR add_summary: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_summary(summary_id, title, description):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE Resume SET Titre = %s, Description = %s
            WHERE Id = %s
        """, (title, description, summary_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"ERROR update_summary: {e}", flush=True)
        conn.rollback()
        return False
    finally:
        conn.close()

def delete_summary(summary_id, user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE Contribution SET EstSupprime = TRUE
            WHERE Id = %s AND IdUtilisateur = %s
        """, (summary_id, user_id))
        if cur.rowcount == 0:
            return False
        cur.execute("""
            UPDATE Contribution SET EstSupprime = TRUE
            WHERE Id IN (SELECT Id FROM Evaluation WHERE IdResume = %s)
        """, (summary_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"ERROR delete_summary: {e}", flush=True)
        conn.rollback()
        return False
    finally:
        conn.close()

def add_evaluation(rating, comment, summary_id, user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Contribution (IdUtilisateur)
            VALUES (%s)
            RETURNING Id
        """, (user_id,))
        contribution_id = cur.fetchone()['id']

        cur.execute("""
            INSERT INTO Evaluation (Id, Note, Commentaire, IdResume)
            VALUES (%s, %s, %s, %s)
        """, (contribution_id, rating, comment, summary_id))

        cur.execute("""
            SELECT c.IdUtilisateur FROM Contribution c
            JOIN Resume r ON c.Id = r.Id WHERE r.Id = %s
        """, (summary_id,))

        award_points(user_id, 50, contribution_id, cur)
        update_level(user_id, cur)
        conn.commit()

        return True
    except Exception as e:
        print(f"ERROR add_evaluation: {e}", flush=True)
        conn.rollback()
        return False
    finally:
        conn.close()

def get_random_top_summary():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            WITH notes AS (
                SELECT r.Id, r.Titre AS title, r.Description,
                       c2.Nom AS course_name, c2.Code AS course_code,
                       u.Nom AS author,
                       ROUND(AVG(e.Note)::numeric, 2) AS avg_rating,
                       RANK() OVER (
                           PARTITION BY r.Code
                           ORDER BY AVG(e.Note) DESC
                       ) AS rank
                FROM Resume r
                JOIN Contribution c ON r.Id = c.Id
                JOIN Utilisateur u ON c.IdUtilisateur = u.IdUtilisateur
                JOIN Cours c2 ON r.Code = c2.Code
                JOIN Evaluation e ON e.IdResume = r.Id
                WHERE r.Visibilite = 'public' AND c.EstSupprime = FALSE
                GROUP BY r.Id, r.Titre, r.Description, c2.Nom, c2.Code, u.Nom
            )
            SELECT Id, title, Description, course_name, course_code, author, avg_rating
            FROM notes
            WHERE rank = 1
            ORDER BY RANDOM()
            LIMIT 1
        """)
        row = cur.fetchone()
        return row
    except Exception as e:
        print(f"Error get_random_top_summary: {e}")
        return None
    finally:
        conn.close()

def save_summary_file(summary_id, file_bytes):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE Resume SET Fichier = %s WHERE Id = %s",
                    (file_bytes, summary_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error save_summary_file: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_summary_file(summary_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT Fichier, Titre FROM Resume WHERE Id = %s", (summary_id,))
        row = cur.fetchone()
        return row
    except Exception as e:
        print(f"Error get_summary_file: {e}")
        return None
    finally:
        conn.close()
