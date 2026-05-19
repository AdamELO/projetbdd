from db import get_connection, get_named_queries

_queries = get_named_queries()

def top_10_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Les 10 utilisateurs ayant le plus de points"])
    results = cur.fetchall()
    conn.close()
    return [dict(r) for r in results]

def users_min_3_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Les utilisateurs ayant publié des résumés dans au moins 3 cours différents"])
    results = cur.fetchall()
    conn.close()
    return [dict(r) for r in results]

def most_summarized_course():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Le cours ayant le plus de résumés publiés"])
    results = cur.fetchall()
    conn.close()
    return [dict(r) for r in results]

def best_rated_resumes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Les résumés les mieux notés (note moyenne maximale) pour chaque cours"])
    results = cur.fetchall()
    conn.close()
    return [dict(r) for r in results]

def users_no_resume():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Les utilisateurs n'ayant jamais publié de résumé"])
    results = cur.fetchall()
    conn.close()
    return [dict(r) for r in results]

def most_bought_item():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["L'objet cosmétique le plus acheté"])
    result = cur.fetchone()
    conn.close()
    return dict(result) if result else None

def users_overspent():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Les utilisateurs ayant dépensé plus de points qu'ils n'en ont disponibles"])
    results = cur.fetchall()
    conn.close()
    return [dict(r) for r in results]

def avg_resumes_per_user():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_queries["Le nombre moyen de résumés publiés par utilisateur"])
    result = cur.fetchone()
    conn.close()
    return dict(result) if result else None

def top_10_by_level():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT IdUtilisateur as id, Nom as nom, Niveau as niveau, Points as points
        FROM Utilisateur
        ORDER BY Niveau DESC, Points DESC
        LIMIT 10
    """)
    results = cur.fetchall()
    conn.close()
    return [dict(r) for r in results]