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
        SELECT obj.Nom
        FROM ObjetCosmetique obj
        JOIN ObjetUtilisateur obju ON obj.id = obju.IdObjetCosmetique
        JOIN Titre t ON obj.Id = t.Id
        WHERE obju.IdUtilisateur = %s AND obju.EstActif = TRUE;
       """, (user_id,))
    results = cur.fetchall()
    conn.close()
    # print(results)
    return results

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