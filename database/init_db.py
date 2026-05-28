import csv
import json
import xml.etree.ElementTree as ET
import unicodedata
import psycopg2
import bcrypt
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
cur = conn.cursor()

def normalize(text):
    """Remove accents and lowercase for comparison."""
    if text is None:
        return ""
    text = text.strip().lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text

try:
    # COURS
    print("Insertion des cours...")
    with open("data/cours.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = row.get("annee_academique", None)
            cur.execute("""
                INSERT INTO Cours (Code, Nom, Faculte, Credits, AnneeAcademique)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (row["code_cours"], row["nom"], row["faculte"], int(row["credits"]), year))

    # OBJETS COSMÉTIQUES
    print("Insertion des objets cosmétiques...")
    tree = ET.parse("data/recompenses.xml")
    root = tree.getroot()

    for obj in root.findall("objet"):
        obj_id = int(obj.get("id"))
        name = obj.find("nom").text
        type_ = obj.find("type").text
        description = obj.find("description").text
        price = int(obj.find("prix").text)

        cur.execute("""
            INSERT INTO Objet (Id, Nom, Description, Prix)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (obj_id, name, description, price))

        if type_ == "badge":
            cur.execute("""
                INSERT INTO Badge (Id) VALUES (%s)
                ON CONFLICT DO NOTHING
            """, (obj_id,))
        elif type_ == "titre":
            cur.execute("""
                INSERT INTO Titre (Id) VALUES (%s)
                ON CONFLICT DO NOTHING
            """, (obj_id,))
        elif type_ == "theme":
            cur.execute("""
                INSERT INTO Theme (Id) VALUES (%s)
                ON CONFLICT DO NOTHING
            """, (obj_id,))
        elif type_ == "cosmetique":
            icon = obj.find("icone")
            cur.execute("""
                INSERT INTO Cosmetique (Id, Icone) VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (obj_id, icon.text if icon is not None else None))

    cur.execute("""
        SELECT setval(
            pg_get_serial_sequence('Objet', 'id'),
            (SELECT MAX(Id) FROM Objet)
        )
    """)

    # ── 3. UTILISATEURS ───────────────────────────────────────────────────────
    print("Insertion des utilisateurs...")
    tree_u = ET.parse("data/utilisateurs.xml")
    root_u = tree_u.getroot()

    name_to_id = {}

    for user in root_u.findall("utilisateur"):
        uid = int(user.get("id"))
        name = user.find("nomUtilisateur").text
        email = user.find("email").text
        registration_date = user.find("dateInscription").text
        points_el = user.find("points")
        level_el = user.find("niveau")
        points = int(points_el.text) if points_el is not None and points_el.text else 0
        level = int(level_el.text) if level_el is not None and level_el.text else 1

        password_hash = bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode()
        cur.execute("""
            INSERT INTO Utilisateur (IdUtilisateur, Nom, Email, MotDePasse, DateInscription, Points, Niveau)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (uid, name, email, password_hash, registration_date, points, level))

        name_to_id[name] = uid

    # Resynchroniser la séquence Utilisateur
    cur.execute("""
        SELECT setval(
            pg_get_serial_sequence('Utilisateur', 'idutilisateur'),
            (SELECT MAX(IdUtilisateur) FROM Utilisateur)
        )
    """)

        # ── 4. RÉSUMÉS ────────────────────────────────────────────────────────────────
    print("Insertion des résumés...")

    # Construire un index titre → code_cours depuis le JSON
    with open("data/commentaires.json", encoding="utf-8") as f:
        data_json = json.load(f)

    title_to_course = {}
    for eval_ in data_json["evaluations"]:
        title = eval_["resume"]["titre"]
        course = eval_["resume"]["cours"]
        title_to_course[title] = course

    for user in root_u.findall("utilisateur"):
        uid = int(user.get("id"))
        summaries = user.find("resumes")
        if summaries is None:
            continue

        for summary in summaries.findall("resume"):
            course_el = summary.find("cours")
            title_el  = summary.find("titre")
            date_el   = summary.find("datePublication")

            course_code = course_el.text.strip() if course_el is not None and course_el.text and course_el.text.strip() else None
            title       = title_el.text           if title_el  is not None and title_el.text  else None
            date_pub    = date_el.text            if date_el   is not None and date_el.text   else None

            if not title or not date_pub:
                print(f"  Résumé ignoré (données manquantes) : uid={uid}, titre={title}")
                continue

            # Toujours vérifier via le JSON d'abord si le titre y est référencé
            valid_json_code = title_to_course.get(title)

            if valid_json_code:
                # Le JSON fait autorité sur le code cours
                cur.execute("SELECT Code FROM Cours WHERE Code = %s", (valid_json_code,))
                if cur.fetchone() is not None:
                    if course_code != valid_json_code:
                        print(f"  Code corrigé : '{course_code}' → '{valid_json_code}' (via titre '{title}')")
                    course_code = valid_json_code
                else:
                    print(f"  Résumé ignoré — code JSON introuvable en DB : {valid_json_code} / '{title}'")
                    continue
            elif course_code:
                # Pas dans le JSON, vérifier que le code XML existe
                cur.execute("SELECT Code FROM Cours WHERE Code = %s", (course_code,))
                if cur.fetchone() is None:
                    print(f"  Résumé ignoré — code inconnu et titre absent du JSON : {course_code} / '{title}'")
                    continue
            else:
                print(f"  Résumé ignoré — code vide et titre absent du JSON : titre='{title}'")
                continue

            cur.execute("""
                SELECT r.Id FROM Resume r
                JOIN Contribution c ON r.Id = c.Id
                WHERE r.Titre = %s AND r.Code = %s AND c.IdUtilisateur = %s
                LIMIT 1
            """, (title, course_code, uid))
            if cur.fetchone() is not None:
                continue

            cur.execute("""
                INSERT INTO Contribution (Date, IdUtilisateur)
                VALUES (%s, %s)
                RETURNING Id
            """, (date_pub, uid))
            contribution_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO Resume (Id, Titre, Description, Version, Visibilite, Code)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (contribution_id, title, "", 1, "public", course_code))


    # ── 5. ÉVALUATIONS ────────────────────────────────────────────────────────
    print("Insertion des évaluations...")
    with open("data/commentaires.json", encoding="utf-8") as f:
        data = json.load(f)

    for eval_ in data["evaluations"]:
        author      = eval_["auteur"]
        course_code = eval_["resume"]["cours"]
        summary_title = eval_["resume"]["titre"]
        note        = eval_["note"]
        comment     = eval_["commentaire"]

        if author not in name_to_id:
            print(f"  Auteur inconnu ignoré : {author}")
            continue

        author_uid = name_to_id[author]

        cur.execute("""
            SELECT r.Id FROM Resume r
            JOIN Contribution c ON r.Id = c.Id
            WHERE r.Titre = %s AND r.Code = %s
            LIMIT 1
        """, (summary_title, course_code))
        row = cur.fetchone()
        if row is None:
            print(f"  Résumé non trouvé pour évaluation : '{summary_title}' ({course_code})")
            continue
        summary_id = row[0]

        cur.execute("""
            SELECT e.Id FROM Evaluation e
            JOIN Contribution c ON e.Id = c.Id
            WHERE e.IdResume = %s AND c.IdUtilisateur = %s AND e.Commentaire = %s
            LIMIT 1
        """, (summary_id, author_uid, comment))
        if cur.fetchone() is not None:
            continue

        cur.execute("""
            INSERT INTO Contribution (Date, IdUtilisateur)
            VALUES (CURRENT_DATE, %s)
            RETURNING Id
        """, (author_uid,))
        contribution_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO Evaluation (Id, Note, Commentaire, IdResume)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (contribution_id, note, comment, summary_id))

    # ── 6. TRANSACTIONS ET ACHATS ─────────────────────────────────────────────
    print("Insertion des transactions (achats)...")
    cur.execute("SELECT Id, Nom FROM Objet")
    objects_db = cur.fetchall()
    objects_map = {normalize(name): id_ for id_, name in objects_db}

    for user in root_u.findall("utilisateur"):
        uid = int(user.get("id"))
        purchases = user.find("achats")
        if purchases is None:
            continue

        for obj in purchases.findall("objet"):
            if obj.text is None:
                continue

            normalized_name = normalize(obj.text)
            object_id = objects_map.get(normalized_name)
            if object_id is None:
                print(f"  Objet non trouvé : '{obj.text}'")
                continue

            # Vérifier si l'achat existe déjà pour éviter les doublons au re-run
            cur.execute("""
                SELECT 1 FROM ObjetUtilisateur
                WHERE IdObjet = %s AND IdUtilisateur = %s
            """, (object_id, uid))
            if cur.fetchone() is not None:
                continue

            cur.execute("SELECT Prix FROM Objet WHERE Id = %s", (object_id,))
            price = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO Transaction (Date, Montant, IdObjet, IdUtilisateur)
                VALUES (CURRENT_DATE, %s, %s, %s)
            """, (-price, object_id, uid))

            cur.execute("""
                INSERT INTO ObjetUtilisateur (IdObjet, IdUtilisateur, EstActif)
                VALUES (%s, %s, FALSE)
                ON CONFLICT DO NOTHING
            """, (object_id, uid))

    # ── 7. ACTIVATION DES TITRES ──────────────────────────────────────────────
    print("Activation des titres actifs...")
    for user in root_u.findall("utilisateur"):
        uid = int(user.get("id"))
        active_title_el = user.find("titreActif")
        if active_title_el is None or not active_title_el.text:
            continue

        active_title = active_title_el.text.strip()
        cur.execute("""
            UPDATE ObjetUtilisateur ou
            SET EstActif = TRUE
            FROM Objet obj
            JOIN Titre t ON obj.Id = t.Id
            WHERE ou.IdObjet = obj.Id
            AND ou.IdUtilisateur = %s
            AND obj.Nom = %s
        """, (uid, active_title))

    # ── 8. RESYNCHRONISATION DES SÉQUENCES ───────────────────────────────────
    print("Resynchronisation des séquences...")
    cur.execute("""
        SELECT setval(
            pg_get_serial_sequence('Contribution', 'id'),
            (SELECT MAX(Id) FROM Contribution)
        )
    """)

    conn.commit()
    print("Base de données initialisée avec succès !")

    # ── 9. LEADERBOARD ────────────────────────────────────────────────────────────
    print("Initialisation du leaderboard...")
    cur.execute("""
    INSERT INTO Leaderboard (IdUtilisateur, Annee, PointsTotaux)
    SELECT IdUtilisateur, EXTRACT(year FROM CURRENT_DATE)::INTEGER, Points
    FROM Utilisateur
    ON CONFLICT (IdUtilisateur, Annee) DO UPDATE
        SET PointsTotaux = EXCLUDED.PointsTotaux
    """)
    conn.commit()


except Exception as e:
    conn.rollback()
    print(f" Erreur durant l'initialisation : {e}")
    raise

finally:
    cur.close()
    conn.close()
