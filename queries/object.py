from db import get_connection

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