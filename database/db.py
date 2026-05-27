import psycopg2
from psycopg2.extras import RealDictCursor
import config
import os

def get_connection():
    return psycopg2.connect(
        host=config.DB_HOST,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        port=config.DB_PORT,
        cursor_factory=RealDictCursor
    )
def get_named_queries():
    queries = {}
    current_name = None
    current_sql = []
    
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sql", "queries.sql")
    print("=== CHARGEMENT QUERIES ===")
    print("Chemin :", path)
    print("Existe :", os.path.exists(path))
    
    with open(path, encoding="utf-8") as f:
        for line in f:
            line_stripped = line.strip()
            if line_stripped.startswith("-- "):
                if current_name and current_sql:
                    queries[current_name] = "\n".join(current_sql).strip()
                current_name = line_stripped[3:].strip()
                current_sql = []
            elif current_name:
                current_sql.append(line.rstrip())
        if current_name and current_sql:
            queries[current_name] = "\n".join(current_sql).strip()
    
    print("Clés trouvées :", list(queries.keys()))
    print("=========================")
    return queries