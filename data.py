"""
Capa de acceso a datos: sustituye las antiguas listas en memoria por
consultas a Postgres (Supabase). Cada función devuelve dicts (o listas
de dicts) que las plantillas Jinja consumen igual que antes (c.nombre,
c.tramite, etc. funcionan también sobre dicts).
"""
from db import get_cursor


# ---------- clientes ----------

def listar_clientes(estado=None):
    with get_cursor() as cur:
        if estado and estado != "todos":
            cur.execute(
                "select * from clientes where estado = %s order by id desc", (estado,)
            )
        else:
            cur.execute("select * from clientes order by id desc")
        return cur.fetchall()


def clientes_recientes(limit=5):
    with get_cursor() as cur:
        cur.execute("select * from clientes order by id desc limit %s", (limit,))
        return cur.fetchall()


def obtener_cliente(cliente_id):
    with get_cursor() as cur:
        cur.execute("select * from clientes where id = %s", (cliente_id,))
        return cur.fetchone()


def crear_cliente(nombre, email, tel, dni, tramite, initials, color="blue"):
    with get_cursor() as cur:
        cur.execute(
            """
            insert into clientes (nombre, email, tel, dni, tramite, estado, progreso, alta, initials, color)
            values (%s, %s, %s, %s, %s, 'pendiente', 0, 'Hoy', %s, %s)
            returning *
            """,
            (nombre, email, tel, dni, tramite, initials, color),
        )
        return cur.fetchone()


def contar_clientes():
    with get_cursor() as cur:
        cur.execute("select count(*) as n from clientes")
        return cur.fetchone()["n"]


def contar_clientes_por_estado(estado):
    with get_cursor() as cur:
        cur.execute("select count(*) as n from clientes where estado = %s", (estado,))
        return cur.fetchone()["n"]


def buscar_clientes(query, limit=None):
    """Busca por nombre, email, DNI, teléfono o trámite (case-insensitive)."""
    patron = f"%{query}%"
    sql = """
        select * from clientes
        where nombre ilike %s
           or email ilike %s
           or dni ilike %s
           or tel ilike %s
           or tramite ilike %s
        order by id desc
    """
    params = [patron, patron, patron, patron, patron]
    if limit:
        sql += " limit %s"
        params.append(limit)
    with get_cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def clientes_por_tramite():
    with get_cursor() as cur:
        cur.execute(
            "select tramite, count(*) as n from clientes group by tramite order by n desc"
        )
        return cur.fetchall()


def progreso_medio():
    with get_cursor() as cur:
        cur.execute("select coalesce(avg(progreso), 0) as avg from clientes")
        return round(cur.fetchone()["avg"] or 0)


def estadisticas_clientes_por_estado():
    resultado = {"pendiente": 0, "en-curso": 0, "completado": 0}
    with get_cursor() as cur:
        cur.execute("select estado, count(*) as n from clientes group by estado")
        for fila in cur.fetchall():
            resultado[fila["estado"]] = fila["n"]
    return resultado


# ---------- documentos ----------

def listar_documentos():
    with get_cursor() as cur:
        cur.execute("select * from documentos order by id desc")
        return cur.fetchall()


def listar_documentos_por_cliente(cliente_id):
    with get_cursor() as cur:
        cur.execute(
            "select * from documentos where cliente_id = %s order by id desc",
            (cliente_id,),
        )
        return cur.fetchall()


def documentos_pendientes(limit=3):
    with get_cursor() as cur:
        cur.execute(
            "select * from documentos where estado = 'pendiente' order by id desc limit %s",
            (limit,),
        )
        return cur.fetchall()


def contar_documentos_pendientes():
    with get_cursor() as cur:
        cur.execute("select count(*) as n from documentos where estado = 'pendiente'")
        return cur.fetchone()["n"]


def contar_documentos():
    with get_cursor() as cur:
        cur.execute("select count(*) as n from documentos")
        return cur.fetchone()["n"]


def estadisticas_documentos_por_estado():
    resultado = {"pendiente": 0, "aprobado": 0, "rechazado": 0}
    with get_cursor() as cur:
        cur.execute("select estado, count(*) as n from documentos group by estado")
        for fila in cur.fetchall():
            resultado[fila["estado"]] = fila["n"]
    return resultado


def actualizar_estado_documento(doc_id, estado):
    with get_cursor() as cur:
        cur.execute(
            "update documentos set estado = %s where id = %s", (estado, doc_id)
        )


def crear_documento(nombre, cliente_id, cliente, tramite, tipo, fecha, size, estado="pendiente"):
    with get_cursor() as cur:
        cur.execute(
            """
            insert into documentos (nombre, cliente_id, cliente, tramite, tipo, fecha, estado, size)
            values (%s, %s, %s, %s, %s, %s, %s, %s)
            returning *
            """,
            (nombre, cliente_id, cliente, tramite, tipo, fecha, estado, size),
        )
        return cur.fetchone()


# ---------- actividad ----------

def listar_actividad():
    with get_cursor() as cur:
        cur.execute("select * from actividad order by id desc")
        return cur.fetchall()


def registrar_actividad(texto, tiempo, tipo="blue"):
    with get_cursor() as cur:
        cur.execute(
            "insert into actividad (texto, tiempo, tipo) values (%s, %s, %s)",
            (texto, tiempo, tipo),
        )
