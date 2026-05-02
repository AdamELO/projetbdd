import csv
import json
import xml.etree.ElementTree as ET
import psycopg2
import bcrypt
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
cur = conn.cursor()

# COURS 
with open("data/cours.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute("""
    INSERT INTO Cours (Code, Nom, Faculte, Credits)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT DO NOTHING
""", (row["code_cours"], row["nom"], row["faculte"], int(row["credits"])))

# ── 2. ANNÉE ACADÉMIQUE ───────────────────────────────────────────────────────
print("Insertion des années académiques...")
cur.execute("""
    INSERT INTO AnneeAcademique (PeriodeAcademique)
    VALUES ('2025-2026')
    ON CONFLICT DO NOTHING
""")

# ── 3. OBJETS COSMÉTIQUES ─────────────────────────────────────────────────────
tree = ET.parse("data/recompenses.xml")
root = tree.getroot()

for objet in root.findall("objet"):
    obj_id = int(objet.get("id"))
    nom = objet.find("nom").text
    type_ = objet.find("type").text
    description = objet.find("description").text
    prix = int(objet.find("prix").text)

    cur.execute("""
        INSERT INTO ObjetCosmetique (Id, Nom, Description, Prix)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (obj_id, nom, description, prix))

    if type_ == "badge":
        image = objet.find("image")
        cur.execute("""
            INSERT INTO Badge (Id, Image)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (obj_id, image.text if image is not None else None))
    elif type_ == "titre":
        cur.execute("""
            INSERT INTO Titre (Id)
            VALUES (%s)
            ON CONFLICT DO NOTHING
        """, (obj_id,))
    elif type_ == "theme":
        image = objet.find("image")
        cur.execute("""
            INSERT INTO Theme (Id, Image)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (obj_id, image.text if image is not None else None))
    elif type_ == "cosmetique":
        icone = objet.find("icone")
        cur.execute("""
            INSERT INTO Cosmetique (Id, Icone)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (obj_id, icone.text if icone is not None else None))

# ── 4. UTILISATEURS ───────────────────────────────────────────────────────────
print("Insertion des utilisateurs...")
tree_u = ET.parse("data/utilisateurs.xml")
root_u = tree_u.getroot()

nom_to_id = {}  # pour retrouver l'id par nom d'utilisateur plus tard

for utilisateur in root_u.findall("utilisateur"):
    uid = int(utilisateur.get("id"))
    nom = utilisateur.find("nomUtilisateur").text
    email = utilisateur.find("email").text
    date_inscription = utilisateur.find("dateInscription").text
    points_el = utilisateur.find("points")
    niveau_el = utilisateur.find("niveau")
    points = int(points_el.text) if points_el is not None and points_el.text else 0
    niveau = int(niveau_el.text) if niveau_el is not None and niveau_el.text else 1
    
    password_hash = bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode()
    cur.execute("""
    INSERT INTO Utilisateur (IdUtilisateur, Nom, Email, MotDePasse, DateInscription, Points, Niveau)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
    """, (uid, nom, email, password_hash, date_inscription, points, niveau))
    
    nom_to_id[nom] = uid

# ── 5. RÉSUMÉS ────────────────────────────────────────────────────────────────
print("Insertion des résumés...")
contribution_id = 1

for utilisateur in root_u.findall("utilisateur"):
    uid = int(utilisateur.get("id"))
    resumes = utilisateur.find("resumes")
    if resumes is None:
        continue
    for resume in resumes.findall("resume"):
        cours_el = resume.find("cours")
        titre_el = resume.find("titre")
        date_el = resume.find("datePublication")

        cours_code = cours_el.text if cours_el is not None and cours_el.text and cours_el.text.strip() else None
        titre = titre_el.text if titre_el is not None and titre_el.text else None
        date_pub = date_el.text if date_el is not None and date_el.text else None

        # Ignorer si données manquantes
        if not cours_code or not titre or not date_pub:
            continue

        cur.execute("SELECT Code FROM Cours WHERE Code = %s", (cours_code,))
        if cur.fetchone() is None:
            cur.execute("""
                INSERT INTO Cours (Code, Nom, Faculte)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (cours_code, cours_code, "Inconnu"))

        cur.execute("""
            INSERT INTO Contribution (Id, Date, IdUtilisateur)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (contribution_id, date_pub, uid))

        cur.execute("""
            INSERT INTO Resume (Id, Titre, Description, Version, Visibilite, Code)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (contribution_id, titre, "", 1, "public", cours_code))

        contribution_id += 1
# ── 6. ÉVALUATIONS ────────────────────────────────────────────────────────────
print("Insertion des évaluations...")
with open("data/commentaires.json", encoding="utf-8") as f:
    data = json.load(f)

for eval_ in data["evaluations"]:
    auteur = eval_["auteur"]
    cours_code = eval_["resume"]["cours"]
    titre_resume = eval_["resume"]["titre"]
    note = eval_["note"]
    commentaire = eval_["commentaire"]

    if auteur not in nom_to_id:
        continue

    uid_auteur = nom_to_id[auteur]

    # Trouver l'id du résumé correspondant
    cur.execute("""
        SELECT r.Id FROM Resume r
        JOIN Contribution c ON r.Id = c.Id
        WHERE r.Titre = %s AND r.Code = %s
        LIMIT 1
    """, (titre_resume, cours_code))
    row = cur.fetchone()
    if row is None:
        continue
    id_resume = row[0]

    cur.execute("""
        INSERT INTO Contribution (Id, Date, IdUtilisateur)
        VALUES (%s, CURRENT_DATE, %s)
        ON CONFLICT DO NOTHING
    """, (contribution_id, uid_auteur))

    cur.execute("""
        INSERT INTO Evaluation (Id, Note, Commentaire, IdResume)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (contribution_id, note, commentaire, id_resume))

    contribution_id += 1

# ── 7. LEADERBOARD ────────────────────────────────────────────────────────────
print("Insertion du leaderboard...")
cur.execute("""
    INSERT INTO Leaderboard (Periode, IdUtilisateur, PointsTotal)
    SELECT '2025-2026', IdUtilisateur, Points
    FROM Utilisateur
    ON CONFLICT DO NOTHING
""")

# ── 8. TRANSACTIONS (ACHATS) ──────────────────────────────────────────────────
print("Insertion des transactions (achats)...")

# Charger tous les objets cosmétiques depuis la DB
cur.execute("SELECT Id, Nom FROM ObjetCosmetique")
objets_db = cur.fetchall()

import unicodedata

def normaliser(texte):
    """Enlève accents et met en minuscules pour comparaison"""
    if texte is None:
        return ""
    texte = texte.strip().lower()
    texte = unicodedata.normalize('NFD', texte)
    texte = ''.join(c for c in texte if unicodedata.category(c) != 'Mn')
    return texte

# Dictionnaire nom normalisé -> id
objets_map = {normaliser(nom): id_ for id_, nom in objets_db}

for utilisateur in root_u.findall("utilisateur"):
    uid = int(utilisateur.get("id"))
    achats = utilisateur.find("achats")
    if achats is None:
        continue
    for objet in achats.findall("objet"):
        if objet.text is None:
            continue
        nom_normalise = normaliser(objet.text)
        id_objet = objets_map.get(nom_normalise)
        if id_objet is None:
            print(f"  ⚠️  Objet non trouvé : '{objet.text}' (normalisé: '{nom_normalise}')")
            continue

        # Récupérer le prix de l'objet
        cur.execute("SELECT Prix FROM ObjetCosmetique WHERE Id = %s", (id_objet,))
        prix = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO Transaction (Date, Montant, IdObjetCosmetique, IdUtilisateur)
            VALUES (CURRENT_DATE, %s, %s, %s)
        """, (-prix, id_objet, uid))

        # Ajouter dans ObjetUtilisateur
        cur.execute("""
            INSERT INTO ObjetUtilisateur (IdObjetCosmetique, IdUtilisateur, EstActif)
            VALUES (%s, %s, FALSE)
            ON CONFLICT DO NOTHING
        """, (id_objet, uid))

# ── 9. ACTIVER LE TITRE ACTIF ─────────────────────────────────────────────────
print("Activation des titres actifs...")
for utilisateur in root_u.findall("utilisateur"):
    uid = int(utilisateur.get("id"))
    titre_actif_el = utilisateur.find("titreActif")
    if titre_actif_el is None or not titre_actif_el.text:
        continue
    titre_actif = titre_actif_el.text.strip()
    
    cur.execute("""
        UPDATE ObjetUtilisateur ou
        SET EstActif = TRUE
        FROM ObjetCosmetique obj
        JOIN Titre t ON obj.Id = t.Id
        WHERE ou.IdObjetCosmetique = obj.Id
        AND ou.IdUtilisateur = %s
        AND obj.Nom = %s
    """, (uid, titre_actif))
print("Resynchronisation des séquences...")
cur.execute("SELECT setval(pg_get_serial_sequence('Utilisateur', 'idutilisateur'), (SELECT MAX(IdUtilisateur) FROM Utilisateur));")
cur.execute("SELECT setval(pg_get_serial_sequence('Contribution', 'id'), (SELECT MAX(Id) FROM Contribution));")
      
conn.commit()
cur.close()
conn.close()
print("Base de données initialisée avec succès !")