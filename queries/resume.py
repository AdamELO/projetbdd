from db import get_connection
from queries.user import award_points, update_level

def add_resume(titre, description, code_cours, id_utilisateur):
    print("ADD_RESUME APPELÉ")
    conn = get_connection()
    cur = conn.cursor()
    try:
        # D'abord insérer dans Contribution
        cur.execute("""
            INSERT INTO Contribution (IdUtilisateur)
            VALUES (%s)
            RETURNING Id
        """, (id_utilisateur,))
        id_contribution = cur.fetchone()['id']

        # Puis insérer dans Resume
        cur.execute("""
            INSERT INTO Resume (Id, Titre, Description, Code)
            VALUES (%s, %s, %s, %s)
        """, (id_contribution, titre, description, code_cours))

        award_points(id_utilisateur, 300, id_contribution, cur)
        update_level(id_utilisateur, cur)
        conn.commit()
        return True
    except Exception as e:
        print(f"ERREUR add_resume: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_resume(resume_id, titre, description):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE Resume SET Titre = %s, Description = %s
            WHERE Id = %s
        """, (titre, description, resume_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"ERREUR update_resume: {e}", flush=True)
        conn.rollback()
        return False
    finally:
        conn.close()

def delete_resume(resume_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Resume WHERE Id = %s", (resume_id,))
        cur.execute("DELETE FROM Contribution WHERE Id = %s", (resume_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"ERREUR delete_resume: {e}", flush=True)
        conn.rollback()
        return False
    finally:
        conn.close()

def add_evaluation(note, commentaire, id_resume, id_utilisateur):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Contribution (IdUtilisateur)
            VALUES (%s)
            RETURNING Id
        """, (id_utilisateur,))
        id_contribution = cur.fetchone()['id']

        cur.execute("""
            INSERT INTO Evaluation (Id, Note, Commentaire, IdResume)
            VALUES (%s, %s, %s, %s)
        """, (id_contribution, note, commentaire, id_resume))

        cur.execute("""
            SELECT c.IdUtilisateur FROM Contribution c
            JOIN Resume r ON c.Id = r.Id WHERE r.Id = %s
        """, (id_resume,))

        award_points(id_utilisateur, 50, id_contribution, cur)
        update_level(id_utilisateur, cur)
        conn.commit()

        return True
    except Exception as e:
        print(f"ERREUR add_evaluation: {e}", flush=True)
        conn.rollback()
        return False
    finally:
        conn.close()

def get_random_top_resume():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            WITH notes AS (
                SELECT r.Id, r.Titre, r.Description,
                       c2.Nom AS cours_nom, c2.Code AS cours_code,
                       u.Nom AS auteur,
                       ROUND(AVG(e.Note)::numeric, 2) AS note_moyenne,
                       RANK() OVER (
                           PARTITION BY r.Code
                           ORDER BY AVG(e.Note) DESC
                       ) AS rang
                FROM Resume r
                JOIN Contribution c ON r.Id = c.Id
                JOIN Utilisateur u ON c.IdUtilisateur = u.IdUtilisateur
                JOIN Cours c2 ON r.Code = c2.Code
                JOIN Evaluation e ON e.IdResume = r.Id
                GROUP BY r.Id, r.Titre, r.Description, c2.Nom, c2.Code, u.Nom
            )
            SELECT Id, Titre, Description, cours_nom, cours_code, auteur, note_moyenne
            FROM notes
            WHERE rang = 1
            ORDER BY RANDOM()
            LIMIT 1
        """)
        row = cur.fetchone()
        return dict(row) if row else None
    except Exception as e:
        print(f"Erreur get_random_top_resume: {e}")
        return None
    finally:
        conn.close()

def save_fichier_resume(resume_id, fichier_bytes):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE Resume SET Fichier = %s WHERE Id = %s", 
                    (fichier_bytes, resume_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur save_fichier_resume: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_fichier_resume(resume_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT Fichier, Titre FROM Resume WHERE Id = %s", (resume_id,))
        row = cur.fetchone()
        return dict(row) if row else None
    except Exception as e:
        print(f"Erreur get_fichier_resume: {e}")
        return None
    finally:
        conn.close()