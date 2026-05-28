from database.db import get_connection

#tous les titres de l'utilisateur
def user_titles(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obju.EstActif as actif
        FROM Objet obj
        JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjet
        JOIN Titre t ON obj.Id = t.Id
        WHERE obju.IdUtilisateur = %s
        ORDER BY obju.EstActif DESC, obj.Nom
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

#tous les themes de l'utilisateur
def user_themes(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obju.EstActif as actif
        FROM Objet obj
        JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjet
        JOIN Theme t ON obj.Id = t.Id
        WHERE obju.IdUtilisateur = %s
        ORDER BY obju.EstActif DESC, obj.Nom
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

#titre actif de l'utilisateur
def user_active_title(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Nom as name
        FROM Objet obj
        JOIN ObjetUtilisateur obju ON obj.id = obju.IdObjet
        JOIN Titre t ON obj.Id = t.Id
        WHERE obju.IdUtilisateur = %s AND obju.EstActif = TRUE
        LIMIT 1
    """, (user_id,))
    result = cur.fetchone()
    conn.close()
    return result

#theme actif de l'utilisateur
def user_active_theme(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Nom as name
        FROM ObjetUtilisateur obju
        JOIN Objet obj ON obju.IdObjet = obj.Id
        JOIN Theme t ON obj.Id = t.Id
        WHERE obju.IdUtilisateur = %s AND obju.EstActif = TRUE
    """, (user_id,))
    result = cur.fetchone()
    # print(result)
    conn.close()
    return result

def user_badges(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obju.EstActif as actif
        FROM Objet obj
        JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjet
        JOIN Badge b ON obj.Id = b.Id
        WHERE obju.IdUtilisateur = %s
        ORDER BY obj.Id
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

def user_cosmetics(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description,
               c.Icone as icon, obju.EstActif as actif
        FROM Objet obj
        JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjet
        JOIN Cosmetique c ON obj.Id = c.Id
        WHERE obju.IdUtilisateur = %s
        ORDER BY obj.Id
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results
def activate_title(user_id, title_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Désactiver tous les titres
        cur.execute("""
            UPDATE ObjetUtilisateur 
            SET EstActif = FALSE
            WHERE IdUtilisateur = %s AND IdObjet IN (
                SELECT Id FROM Titre
            )
        """, (user_id,))
        # Activer le titre choisi
        cur.execute("""
            UPDATE ObjetUtilisateur 
            SET EstActif = TRUE
            WHERE IdUtilisateur = %s AND IdObjet = %s
        """, (user_id, title_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"ERREUR activate_title: {e}", flush=True)
        conn.rollback()
        return False
    finally:
        conn.close()

def activate_theme(user_id, theme_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE ObjetUtilisateur 
            SET EstActif = FALSE
            WHERE IdUtilisateur = %s AND IdObjet IN (
                SELECT Id FROM Theme
            )
        """, (user_id,))
        cur.execute("""
            UPDATE ObjetUtilisateur 
            SET EstActif = TRUE
            WHERE IdUtilisateur = %s AND IdObjet = %s
        """, (user_id, theme_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"ERREUR activate_theme: {e}", flush=True)
        conn.rollback()
        return False
    finally:
        conn.close()

def deactivate_theme(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE ObjetUtilisateur 
            SET EstActif = FALSE
            WHERE IdUtilisateur = %s AND IdObjet IN (
                SELECT Id FROM Theme
            )
        """, (user_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"ERREUR deactivate_theme: {e}", flush=True)
        conn.rollback()
        return False
    finally:
        conn.close()

def get_all_titles():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price
        FROM Objet obj
        JOIN Titre t ON obj.Id = t.Id
    """)
    results = cur.fetchall()
    conn.close()
    return results

def get_all_badges():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price
        FROM Objet obj
        JOIN Badge b ON obj.Id = b.Id
    """)
    results = cur.fetchall()
    conn.close()
    return results

def get_all_themes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price
        FROM Objet obj
        JOIN Theme t ON obj.Id = t.Id
    """)
    results = cur.fetchall()
    conn.close()
    return results


def get_all_cosmetic():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price, c.Icone
        FROM Objet obj
        JOIN Cosmetique c ON obj.Id = c.Id
    """)
    results = cur.fetchall()
    conn.close()
    return results



def get_badges_not_owned(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price
        FROM Objet obj
        JOIN Badge b ON obj.Id = b.Id
        LEFT JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjet AND obju.IdUtilisateur = %s
        WHERE obju.IdObjet IS NULL
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

def get_themes_not_owned(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price
        FROM Objet obj
        JOIN Theme t ON obj.Id = t.Id
        LEFT JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjet AND obju.IdUtilisateur = %s
        WHERE obju.IdObjet IS NULL
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

def get_titles_not_owned(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price
        FROM Objet obj
        JOIN Titre t ON obj.Id = t.Id
        LEFT JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjet AND obju.IdUtilisateur = %s
        WHERE obju.IdObjet IS NULL
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

def get_cosmetics_not_owned(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price, c.Icone
        FROM Objet obj
        JOIN Cosmetique c ON obj.Id = c.Id
        LEFT JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjet AND obju.IdUtilisateur = %s
        WHERE obju.IdObjet IS NULL
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

def buy_object(object_id, user_id, price):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT * FROM ObjetUtilisateur
            WHERE IdObjet = %s AND IdUtilisateur = %s
        """, (object_id, user_id))
        if cur.fetchone():
            return False

        cur.execute("""
            UPDATE Utilisateur SET Points = Points - %s
            WHERE IdUtilisateur = %s AND Points >= %s
        """, (price, user_id, price))

        if cur.rowcount == 0:
            conn.rollback()
            return False

        cur.execute("""
            INSERT INTO ObjetUtilisateur (IdObjet, IdUtilisateur)
            VALUES (%s, %s)
        """, (object_id, user_id))

        cur.execute("""
            INSERT INTO Transaction (Montant, IdObjet, IdUtilisateur, IdContribution)
            VALUES (%s, %s, %s, NULL)
        """, (-price, object_id, user_id))

        conn.commit()
        return True
    except :
        conn.rollback()
        return False
    finally:
        conn.close()

def get_lasts_items(user_id=None, n=3):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price, EXISTS (SELECT * FROM ObjetUtilisateur obju WHERE obju.IdObjet = obj.Id AND obju.IdUtilisateur = %s) as is_bought
        FROM Objet obj
        JOIN Cosmetique c ON obj.Id = c.Id
        ORDER BY obj.Id DESC
        LIMIT %s
    """, (user_id, n))
    results = cur.fetchall()
    conn.close()
    return results