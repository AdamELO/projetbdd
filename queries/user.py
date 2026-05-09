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

def award_points(user_id, amount, contribution_id=None):
    print("AWARD_POINTS APPELÉ")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE Utilisateur 
            SET Points = Points + %s,
                Niveau = ((Points + %s) / 300) + 1
            WHERE IdUtilisateur = %s
        """, (amount, amount, user_id))
        cur.execute("""
            INSERT INTO Transaction (Montant, IdUtilisateur, IdContribution)
            VALUES (%s, %s, %s)
        """, (amount, user_id, contribution_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"ERREUR AWARD_POINTS: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
