"""
Conexión a la base de datos Postgres (Supabase).

La cadena de conexión se lee de la variable de entorno DATABASE_URL
(ver .env.example). Nunca hardcodees aquí usuario/contraseña.
"""
import os
from contextlib import contextmanager

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "Falta la variable de entorno DATABASE_URL. "
        "Copia .env.example a .env y rellena tu contraseña de Supabase."
    )


@contextmanager
def get_conn():
    """Devuelve una conexión psycopg2 (se cierra sola al salir del with)."""
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@contextmanager
def get_cursor():
    """Cursor que devuelve filas como dict (compatible con las plantillas Jinja)."""
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            yield cur
