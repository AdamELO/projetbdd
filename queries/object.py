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