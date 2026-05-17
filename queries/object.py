from db import get_connection
from contextlib import contextmanager


# ──────────────────────────────────────────────
# Context manager – connexion + commit/rollback
# ──────────────────────────────────────────────

@contextmanager
def db_cursor(commit=False):
    conn = get_connection()
    cur = conn.cursor()
    try:
        yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ──────────────────────────────────────────────
# Lecture – objets possédés par l'utilisateur
# ──────────────────────────────────────────────

def user_titles(user_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Id AS id, obj.Nom AS name, obju.EstActif AS actif
            FROM ObjetCosmetique obj
            JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjetCosmetique
            JOIN Titre t ON obj.Id = t.Id
            WHERE obju.IdUtilisateur = %s
            ORDER BY obju.EstActif DESC, obj.Nom
        """, (user_id,))
        return cur.fetchall()


def user_themes(user_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Id AS id, obj.Nom AS name, t.Image AS image, obju.EstActif AS actif
            FROM ObjetCosmetique obj
            JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjetCosmetique
            JOIN Theme t ON obj.Id = t.Id
            WHERE obju.IdUtilisateur = %s
            ORDER BY obju.EstActif DESC, obj.Nom
        """, (user_id,))
        return cur.fetchall()


def user_active_title(user_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Nom AS name
            FROM ObjetCosmetique obj
            JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjetCosmetique
            JOIN Titre t ON obj.Id = t.Id
            WHERE obju.IdUtilisateur = %s AND obju.EstActif = TRUE
            LIMIT 1
        """, (user_id,))
        return cur.fetchone()


def user_active_theme(user_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Nom AS name, t.Image
            FROM ObjetUtilisateur obju
            JOIN ObjetCosmetique obj ON obju.IdObjetCosmetique = obj.Id
            JOIN Theme t ON obj.Id = t.Id
            WHERE obju.IdUtilisateur = %s AND obju.EstActif = TRUE
        """, (user_id,))
        return cur.fetchone()


def user_badges(user_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Id AS id, obj.Nom AS name, obj.Description AS description,
                   b.Image AS image, obju.EstActif AS actif
            FROM ObjetCosmetique obj
            JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjetCosmetique
            JOIN Badge b ON obj.Id = b.Id
            WHERE obju.IdUtilisateur = %s
            ORDER BY obj.Id
        """, (user_id,))
        return cur.fetchall()


def user_cosmetiques(user_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Id AS id, obj.Nom AS name, obj.Description AS description,
                   c.Icone AS icone, obju.EstActif AS actif
            FROM ObjetCosmetique obj
            JOIN ObjetUtilisateur obju ON obj.Id = obju.IdObjetCosmetique
            JOIN Cosmetique c ON obj.Id = c.Id
            WHERE obju.IdUtilisateur = %s
            ORDER BY obj.Id
        """, (user_id,))
        return cur.fetchall()


# ──────────────────────────────────────────────
# Lecture – catalogue complet
# ──────────────────────────────────────────────

def get_all_titles():
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Id, obj.Nom AS name, obj.Description, obj.Prix AS price
            FROM ObjetCosmetique obj
            JOIN Titre t ON obj.Id = t.Id
        """)
        return cur.fetchall()


def get_all_badges():
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Id, obj.Nom AS name, obj.Description, obj.Prix AS price, b.Image
            FROM ObjetCosmetique obj
            JOIN Badge b ON obj.Id = b.Id
        """)
        return cur.fetchall()


def get_all_themes():
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Id, obj.Nom AS name, obj.Description, obj.Prix AS price, t.Image
            FROM ObjetCosmetique obj
            JOIN Theme t ON obj.Id = t.Id
        """)
        return cur.fetchall()


def get_all_cosmetic():
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Id, obj.Nom AS name, obj.Description, obj.Prix AS price, c.Icone
            FROM ObjetCosmetique obj
            JOIN Cosmetique c ON obj.Id = c.Id
        """)
        return cur.fetchall()


# ──────────────────────────────────────────────
# Lecture – objets non possédés
# ──────────────────────────────────────────────

def get_badges_not_owned(user_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Id, obj.Nom AS name, obj.Description, obj.Prix AS price, b.Image
            FROM ObjetCosmetique obj
            JOIN Badge b ON obj.Id = b.Id
            LEFT JOIN ObjetUtilisateur obju
                ON obj.Id = obju.IdObjetCosmetique AND obju.IdUtilisateur = %s
            WHERE obju.IdObjetCosmetique IS NULL
        """, (user_id,))
        return cur.fetchall()


def get_themes_not_owned(user_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Id, obj.Nom AS name, obj.Description, obj.Prix AS price, t.Image
            FROM ObjetCosmetique obj
            JOIN Theme t ON obj.Id = t.Id
            LEFT JOIN ObjetUtilisateur obju
                ON obj.Id = obju.IdObjetCosmetique AND obju.IdUtilisateur = %s
            WHERE obju.IdObjetCosmetique IS NULL
        """, (user_id,))
        return cur.fetchall()


def get_titles_not_owned(user_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Id, obj.Nom AS name, obj.Description, obj.Prix AS price
            FROM ObjetCosmetique obj
            JOIN Titre t ON obj.Id = t.Id
            LEFT JOIN ObjetUtilisateur obju
                ON obj.Id = obju.IdObjetCosmetique AND obju.IdUtilisateur = %s
            WHERE obju.IdObjetCosmetique IS NULL
        """, (user_id,))
        return cur.fetchall()


def get_cosmetic_not_owned(user_id):
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Id, obj.Nom AS name, obj.Description, obj.Prix AS price, c.Icone
            FROM ObjetCosmetique obj
            JOIN Cosmetique c ON obj.Id = c.Id
            LEFT JOIN ObjetUtilisateur obju
                ON obj.Id = obju.IdObjetCosmetique AND obju.IdUtilisateur = %s
            WHERE obju.IdObjetCosmetique IS NULL
        """, (user_id,))
        return cur.fetchall()


def get_lasts_items(user_id=None, n=3):
    with db_cursor() as cur:
        cur.execute("""
            SELECT obj.Id AS id, obj.Nom AS name, obj.Description AS description,
                   obj.Prix AS price,
                   EXISTS (
                       SELECT 1 FROM ObjetUtilisateur obju
                       WHERE obju.IdObjetCosmetique = obj.Id AND obju.IdUtilisateur = %s
                   ) AS is_bought
            FROM ObjetCosmetique obj
            ORDER BY RANDOM()
            LIMIT %s
        """, (user_id, n))
        return [dict(row) for row in cur.fetchall()]


# ──────────────────────────────────────────────
# Écriture – activation
# ──────────────────────────────────────────────

def activate_title(user_id, title_id):
    try:
        with db_cursor(commit=True) as cur:
            cur.execute("""
                UPDATE ObjetUtilisateur
                SET EstActif = FALSE
                WHERE IdUtilisateur = %s AND IdObjetCosmetique IN (
                    SELECT Id FROM Titre
                )
            """, (user_id,))
            cur.execute("""
                UPDATE ObjetUtilisateur
                SET EstActif = TRUE
                WHERE IdUtilisateur = %s AND IdObjetCosmetique = %s
            """, (user_id, title_id))
        return True
    except Exception as e:
        print(f"ERREUR activate_title: {e}", flush=True)
        return False


def activate_theme(user_id, theme_id):
    try:
        with db_cursor(commit=True) as cur:
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
        return True
    except Exception as e:
        print(f"ERREUR activate_theme: {e}", flush=True)
        return False


def deactivate_theme(user_id):
    try:
        with db_cursor(commit=True) as cur:
            cur.execute("""
                UPDATE ObjetUtilisateur
                SET EstActif = FALSE
                WHERE IdUtilisateur = %s AND IdObjetCosmetique IN (
                    SELECT Id FROM Theme
                )
            """, (user_id,))
        return True
    except Exception as e:
        print(f"ERREUR deactivate_theme: {e}", flush=True)
        return False


# ──────────────────────────────────────────────
# Écriture – achat
# ──────────────────────────────────────────────

def buy_object(object_id, user_id, price):
    try:
        with db_cursor(commit=True) as cur:
            # Vérifier si l'objet est déjà possédé
            cur.execute("""
                SELECT 1 FROM ObjetUtilisateur
                WHERE IdObjetCosmetique = %s AND IdUtilisateur = %s
            """, (object_id, user_id))
            if cur.fetchone():
                return False

            # Déduire les points (échoue si solde insuffisant grâce au WHERE)
            cur.execute("""
                UPDATE Utilisateur SET Points = Points - %s
                WHERE IdUtilisateur = %s AND Points >= %s
            """, (price, user_id, price))
            if cur.rowcount == 0:
                raise ValueError("Points insuffisants")

            # Enregistrer la possession
            cur.execute("""
                INSERT INTO ObjetUtilisateur (IdObjetCosmetique, IdUtilisateur)
                VALUES (%s, %s)
            """, (object_id, user_id))

            # Enregistrer la transaction
            cur.execute("""
                INSERT INTO Transaction (Montant, IdObjetCosmetique, IdUtilisateur, IdContribution)
                VALUES (%s, %s, %s, NULL)
            """, (-price, object_id, user_id))

        return True
    except Exception as e:
        print(f"ERREUR buy_object: {e}", flush=True)
        return False