import os

from dotenv import load_dotenv
from psycopg2 import pool

# Le fichier .env est à la racine du projet (deux niveaux au-dessus de ce fichier).
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(os.path.join(ROOT_DIR, ".env"))

INSERT_QUERY = """
    INSERT INTO metadata
    (machine_id, temperature, vibration, rpm, status, measured_at)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

# Le pool est créé à la première utilisation (et non à l'import) :
# importer ce module ne doit pas ouvrir de connexion ni échouer si la base est arrêtée.
_conn_pool = None


def get_pool():
    """Retourne le pool de connexions PostgreSQL, en le créant si nécessaire."""
    global _conn_pool
    if _conn_pool is None:
        _conn_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host=os.getenv("PG_HOST", "localhost"),
            port=int(os.getenv("PG_PORT", "5432")),
            database=os.getenv("PG_DATABASE", "postgres"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
        )
        print("Connexion réussie à PostgreSQL !")
    return _conn_pool


def close_pool():
    """Ferme toutes les connexions du pool."""
    global _conn_pool
    if _conn_pool is not None:
        _conn_pool.closeall()
        _conn_pool = None


def insert_measurement(measurement):
    """Insère une mesure dans la table metadata. Lève l'exception en cas d'échec."""
    conn_pool = get_pool()
    conn = conn_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(INSERT_QUERY, (
                measurement["machine_id"],
                measurement["temperature"],
                measurement["vibration"],
                measurement["rpm"],
                measurement["status"],
                measurement["timestamp"],
            ))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn_pool.putconn(conn)
