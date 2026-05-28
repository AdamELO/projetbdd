from database.db import get_connection
import bcrypt

#connexion
def login(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT IdUtilisateur AS user_id, Nom AS username, Email, Niveau AS level, Points, MotDePasse AS password_hash FROM Utilisateur WHERE Nom = %s", (username,))
    result = cur.fetchone()
    conn.close()
    if result and bcrypt.checkpw(password.encode(), result['password_hash'].encode()):
        return {
            'id': result['user_id'],
            'username': result['username'],
            'email': result['email'],
            'level': result['level'],
            'points': result['points'],
        }
    return None

def register(name, email, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cur.execute("""
            INSERT INTO Utilisateur (Nom, Email, MotDePasse)
            VALUES (%s, %s, %s)
            RETURNING IdUtilisateur AS user_id
        """, (name, email, password_hash))
        row = cur.fetchone()
        conn.commit()
        return {'id': row['user_id']}
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
        # Mettre à jour le leaderboard uniquement si c'est un gain
        if amount > 0:
            cur.execute("""
    INSERT INTO Leaderboard (IdUtilisateur, Annee, pointstotaux)
    VALUES (%s, EXTRACT(year FROM CURRENT_DATE)::INTEGER, %s)
    ON CONFLICT (IdUtilisateur, Annee) DO UPDATE
        SET pointstotaux = Leaderboard.pointstotaux + %s
""", (user_id, amount, amount))
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
            cur.close()
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

def get_user_transactions(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT
                t.Id,
                t.Date,
                t.Montant AS amount,
                o.Nom AS item_name,
                CASE
                    WHEN t.IdObjet IS NOT NULL THEN 'purchase'
                    WHEN e.Id IS NOT NULL THEN 'comment'
                    WHEN r.Id IS NOT NULL THEN 'summary'
                    ELSE 'other'
                END AS type
            FROM Transaction t
            LEFT JOIN Objet o ON t.IdObjet = o.Id
            LEFT JOIN Contribution c ON t.IdContribution = c.Id
            LEFT JOIN Resume r ON c.Id = r.Id
            LEFT JOIN Evaluation e ON c.Id = e.Id
            WHERE t.IdUtilisateur = %s
            ORDER BY t.Date DESC, t.Id DESC
        """, (user_id,))
        return cur.fetchall()
    except Exception as e:
        print(f"Erreur get_user_transactions: {e}")
        return []
    finally:
        conn.close()

def get_user_stats(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT Points, Niveau AS level
            FROM Utilisateur
            WHERE IdUtilisateur = %s
        """, (user_id,))
        
        result = cur.fetchone()
        return result
    except Exception as e:
        print(f"Erreur get_user_stats: {e}")
        return None
    finally:
        conn.close()