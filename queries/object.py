from db import get_connection

#tous les titres de l'utilisateur
def user_titles(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id as id, obj.Nom as name, obju.EstActif as actif
        FROM ObjetCosmetique obj
        JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjetCosmetique
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
        SELECT obj.Id as id, obj.Nom as name, t.Image as image, obju.EstActif as actif
        FROM ObjetCosmetique obj
        JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjetCosmetique
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
        FROM ObjetCosmetique obj
        JOIN ObjetUtilisateur obju ON obj.id = obju.IdObjetCosmetique
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
        SELECT obj.Nom as name, t.Image
        FROM ObjetUtilisateur obju
        JOIN ObjetCosmetique obj ON obju.IdObjetCosmetique = obj.Id
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
        SELECT obj.Id as id, obj.Nom as name, obj.Description as description, 
               b.Image as image, obju.EstActif as actif
        FROM ObjetCosmetique obj
        JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjetCosmetique
        JOIN Badge b ON obj.Id = b.Id
        WHERE obju.IdUtilisateur = %s
        ORDER BY obj.Id
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

def user_cosmetiques(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id as id, obj.Nom as name, obj.Description as description,
               c.Icone as icone, obju.EstActif as actif
        FROM ObjetCosmetique obj
        JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjetCosmetique
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
            WHERE IdUtilisateur = %s AND IdObjetCosmetique IN (
                SELECT Id FROM Titre
            )
        """, (user_id,))
        # Activer le titre choisi
        cur.execute("""
            UPDATE ObjetUtilisateur 
            SET EstActif = TRUE
            WHERE IdUtilisateur = %s AND IdObjetCosmetique = %s
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
            WHERE IdUtilisateur = %s AND IdObjetCosmetique IN (
                SELECT Id FROM Theme
            )
        """, (user_id,))
        cur.execute("""
            UPDATE ObjetUtilisateur 
            SET EstActif = TRUE
            WHERE IdUtilisateur = %s AND IdObjetCosmetique = %s
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
            WHERE IdUtilisateur = %s AND IdObjetCosmetique IN (
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
        FROM ObjetCosmetique obj
        JOIN Titre t ON obj.Id = t.Id
    """)
    results = cur.fetchall()
    conn.close()
    return results

def get_all_badges():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price, b.Image
        FROM ObjetCosmetique obj
        JOIN Badge b ON obj.Id = b.Id
    """)
    results = cur.fetchall()
    conn.close()
    return results

def get_all_themes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price, t.Image
        FROM ObjetCosmetique obj
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
        FROM ObjetCosmetique obj
        JOIN Cosmetique c ON obj.Id = c.Id
    """)
    results = cur.fetchall()
    conn.close()
    return results



def get_badges_not_owned(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price, b.Image
        FROM ObjetCosmetique obj
        JOIN Badge b ON obj.Id = b.Id
        LEFT JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjetCosmetique AND obju.IdUtilisateur = %s
        WHERE obju.IdObjetCosmetique IS NULL
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

def get_themes_not_owned(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price, t.Image
        FROM ObjetCosmetique obj
        JOIN Theme t ON obj.Id = t.Id
        LEFT JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjetCosmetique AND obju.IdUtilisateur = %s
        WHERE obju.IdObjetCosmetique IS NULL
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

def get_titles_not_owned(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price
        FROM ObjetCosmetique obj
        JOIN Titre t ON obj.Id = t.Id
        LEFT JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjetCosmetique AND obju.IdUtilisateur = %s
        WHERE obju.IdObjetCosmetique IS NULL
    """, (user_id,))
    results = cur.fetchall()
    conn.close()
    return results

def get_cosmetic_not_owned(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price, c.Icone
        FROM ObjetCosmetique obj
        JOIN Cosmetique c ON obj.Id = c.Id
        LEFT JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjetCosmetique AND obju.IdUtilisateur = %s
        WHERE obju.IdObjetCosmetique IS NULL
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
            WHERE IdObjetCosmetique = %s AND IdUtilisateur = %s
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
            INSERT INTO ObjetUtilisateur (IdObjetCosmetique, IdUtilisateur)
            VALUES (%s, %s)
        """, (object_id, user_id))

        cur.execute("""
            INSERT INTO Transaction (Montant, IdObjetCosmetique, IdUtilisateur, IdContribution)
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
        SELECT obj.Id, obj.Nom as name, obj.Description, obj.Prix as price, EXISTS (SELECT * FROM ObjetUtilisateur obju WHERE obju.IdObjetCosmetique = obj.Id AND obju.IdUtilisateur = %s) as is_bought
        FROM ObjetCosmetique obj
        JOIN Cosmetique c ON obj.Id = c.Id
        ORDER BY obj.Id DESC
        LIMIT %s
    """, (user_id, n))
    results = cur.fetchall()
    conn.close()
    return results