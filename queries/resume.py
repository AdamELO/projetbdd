from db import get_connection

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

        conn.commit()
        return True
    except Exception as e:
        print(f"ERREUR add_evaluation: {e}", flush=True)
        conn.rollback()
        return False
    finally:
        conn.close()

def get_best_resume_of_month():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.Id as id, r.Titre as titre, r.Code as code_cours,
               co.Nom as nom_cours, u.Nom as auteur,
               ROUND(AVG(e.Note), 1) as note,
               COUNT(DISTINCT e.Id) as nb_commentaires
        FROM Resume r
        JOIN Cours co ON r.Code = co.Code
        JOIN Contribution c ON r.Id = c.Id
        JOIN Utilisateur u ON c.IdUtilisateur = u.IdUtilisateur
        JOIN Evaluation e ON r.Id = e.IdResume
        WHERE DATE_TRUNC('month', c.Date) = DATE_TRUNC('month', CURRENT_DATE)
        GROUP BY r.Id, r.Titre, r.Code, co.Nom, u.Nom
        HAVING AVG(e.Note) = (
            SELECT MAX(avg_note) FROM (
                SELECT AVG(e2.Note) as avg_note
                FROM Resume r2
                JOIN Contribution c2 ON r2.Id = c2.Id
                JOIN Evaluation e2 ON r2.Id = e2.IdResume
                WHERE DATE_TRUNC('month', c2.Date) = DATE_TRUNC('month', CURRENT_DATE)
                GROUP BY r2.Id
            ) AS sous_requete
        )
        ORDER BY RANDOM()
        LIMIT 1
    """)
    result = cur.fetchone()
    conn.close()
    return dict(result) if result else None