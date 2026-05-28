import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

SQL_FILE = os.path.join(os.path.dirname(__file__), "sql", "create.sql")

conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
conn.autocommit = True
cur = conn.cursor()

try:
    with open(SQL_FILE, encoding="utf-8") as f:
        sql = f.read()
    cur.execute(sql)
    print("Tables créées avec succès !")
except Exception as e:
    print(f"Erreur : {e}")
    raise
finally:
    cur.close()
    conn.close()