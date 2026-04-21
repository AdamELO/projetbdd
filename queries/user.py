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

#inscription
def register(username, email, password):
    try:
        conn = get_connection()
        cur = conn.cursor()
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cur.execute(
            "INSERT INTO Utilisateur (nom, email, motdepasse) VALUES (%s, %s, %s)",
            (username, email, password_hash)
        )
        conn.commit()
        conn.close()
        return True
    except:
        return False
