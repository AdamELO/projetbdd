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
        return {'id': row[0]}
    except Exception as e:
        print(f"ERREUR REGISTER: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()
