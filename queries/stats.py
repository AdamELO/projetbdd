from database.db import get_connection, get_named_queries

_queries = get_named_queries()

def top_10_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Les 10 utilisateurs ayant le plus de points"])
    results = cur.fetchall()
    conn.close()
    return results

def users_min_3_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Les utilisateurs ayant publié des résumés dans au moins 3 cours différents"])
    results = cur.fetchall()
    conn.close()
    return results

def most_summarized_course():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Le cours ayant le plus de résumés publiés"])
    results = cur.fetchall()
    conn.close()
    return results

def best_rated_summaries():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Les résumés les mieux notés (note moyenne maximale) pour chaque cours"])
    results = cur.fetchall()
    conn.close()
    return results

def users_no_summary():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Les utilisateurs n'ayant jamais publié de résumé"])
    results = cur.fetchall()
    conn.close()
    return results

def most_bought_item():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["L'objet cosmétique le plus acheté"])
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result is None:
        return {"id": None, "name": "Aucun achat", "purchase_count": 0}
    return result

def users_overspent():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Les utilisateurs ayant dépensé plus de points qu'ils n'en ont disponibles"])
    results = cur.fetchall()
    conn.close()
    return results

def avg_summaries_per_user():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Le nombre moyen de résumés publiés par utilisateur"])
    result = cur.fetchone()
    conn.close()
    return result

def top_10_by_total_points():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT u.IdUtilisateur AS id, u.Nom AS name, u.Niveau AS level,
           l.pointstotaux AS points
    FROM Leaderboard l
    JOIN Utilisateur u ON l.IdUtilisateur = u.IdUtilisateur
    WHERE l.Annee = EXTRACT(year FROM CURRENT_DATE)::INTEGER
    ORDER BY l.pointstotaux DESC
    LIMIT 10
""")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def top_10_by_level():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT u.IdUtilisateur AS id, u.Nom AS name, u.Niveau AS level,
           l.pointstotaux AS points
    FROM Leaderboard l
    JOIN Utilisateur u ON l.IdUtilisateur = u.IdUtilisateur
    WHERE l.Annee = EXTRACT(year FROM CURRENT_DATE)::INTEGER
    ORDER BY u.Niveau DESC, l.pointstotaux DESC
    LIMIT 10
""")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results