import psycopg2
from psycopg2.extras import RealDictCursor
import config
from contextlib import contextmanager


def get_connection():
    try:
        return psycopg2.connect(
            host=config.DB_HOST,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            port=config.DB_PORT,
            cursor_factory=RealDictCursor
        )
    except psycopg2.OperationalError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise

@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()