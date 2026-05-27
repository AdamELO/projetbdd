from db import get_connection
import bcrypt

#connexion
def login(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT idutilisateur, nom, email, niveau, points, motdepasse FROM Utilisateur WHERE Nom = %s", (username,))
    result = cur.fetchone()
    conn.close()
    if result and bcrypt.checkpw(password.encode(), result['motdepasse'].encode()):
        #print(result)
        return {
            'id': result['idutilisateur'],
            'username': result['nom'],
            'email': result['email'],
            'level': result['niveau'],
            'points': result['points'],
        }
    return None

def register(nom, email, mot_de_passe):
    conn = get_connection()
    cur = conn.cursor()
    try:
        password_hash = bcrypt.hashpw(mot_de_passe.encode(), bcrypt.gensalt()).decode()
        cur.execute("""
            INSERT INTO Utilisateur (Nom, Email, MotDePasse)
            VALUES (%s, %s, %s)
            RETURNING IdUtilisateur
        """, (nom, email, password_hash))
        row = cur.fetchone()
        conn.commit()
        return {'id': row['idutilisateur']}
    except Exception as e:
        print(f"ERREUR REGISTER: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def award_points(user_id, amount, contribution_id=None, cur=None):
    local_conn = None
    if cur is None:
        local_conn = get_connection()
        cur = local_conn.cursor()
    try:
        cur.execute("UPDATE Utilisateur SET Points = Points + %s WHERE IdUtilisateur = %s", (amount, user_id))
        cur.execute("INSERT INTO Transaction (Montant, IdUtilisateur, IdContribution) VALUES (%s, %s, %s)", 
                    (amount, user_id, contribution_id))
        if local_conn:
            local_conn.commit()
        return True
    except Exception as e:
        print(f"Erreur award_points: {e}")
        if local_conn:
            local_conn.rollback()
        raise e
    finally:
        if local_conn:
            local_conn.close()

def update_level(user_id, cur=None):
    local_conn = None
    if cur is None:
        local_conn = get_connection()
        cur = local_conn.cursor()
    try:
        cur.execute("""
            UPDATE Utilisateur 
            SET Niveau = 1 + (
                SELECT 
                    (SELECT COUNT(*) FROM Resume r JOIN Contribution c ON r.Id = c.Id WHERE c.IdUtilisateur = %(uid)s) +
                    ((SELECT COUNT(*) FROM Evaluation e JOIN Contribution c ON e.Id = c.Id WHERE c.IdUtilisateur = %(uid)s) / 5)
            )
            WHERE IdUtilisateur = %(uid)s
        """, {'uid': user_id})
        if local_conn:
            local_conn.commit()
        return True
    except Exception as e:
        print(f"Erreur update_level: {e}")
        if local_conn:
            local_conn.rollback()
        raise e
    finally:
        if local_conn:
            local_conn.close()

def get_user_stats(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT Points as points, Niveau as niveau 
            FROM Utilisateur 
            WHERE IdUtilisateur = %s
        """, (user_id,))
        
        result = cur.fetchone()
        return dict(result) if result else None
    except Exception as e:
        print(f"Erreur get_user_stats: {e}")
        return None
    finally:
        conn.close()