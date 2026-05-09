from db import get_connection
from queries.user import award_points

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

        award_points(id_utilisateur, 500, id_contribution)
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
        auteur_resume = cur.fetchone()['idutilisateur']
        conn.commit()

        award_points(id_utilisateur, 100, id_contribution)
        award_points(auteur_resume, int(note) * 50, id_contribution)
        return True
    except Exception as e:
        print(f"ERREUR add_evaluation: {e}", flush=True)
        conn.rollback()
        return False
    finally:
        conn.close()