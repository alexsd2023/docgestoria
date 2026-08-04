"""
Cliente mínimo para Supabase Storage (bucket "Tramites"), vía su API REST.

No usamos el SDK oficial para no añadir una dependencia pesada: con
`requests` basta para subir archivos y generar URLs firmadas de
descarga/vista previa.

Credenciales en variables de entorno (ver .env.example):
  SUPABASE_URL          -> https://<project-ref>.supabase.co
  SUPABASE_SERVICE_KEY   -> service_role key (Project Settings > API). Secreta,
                            nunca debe exponerse al navegador.
"""
import os
import mimetypes

import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
BUCKET = os.environ.get("SUPABASE_STORAGE_BUCKET", "Tramites")


def _headers(content_type=None):
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    }
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def storage_configurado():
    return bool(SUPABASE_URL and SUPABASE_SERVICE_KEY)


def subir_archivo(path, contenido, nombre_archivo):
    """Sube (o sobrescribe) un archivo en el bucket. `path` es la ruta dentro
    del bucket, p. ej. "12/34_pasaporte.pdf". Devuelve (ok, error)."""
    if not storage_configurado():
        return False, "Storage no configurado (faltan SUPABASE_URL / SUPABASE_SERVICE_KEY en .env)"

    content_type = mimetypes.guess_type(nombre_archivo)[0] or "application/octet-stream"
    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET}/{path}"
    headers = _headers(content_type)
    headers["x-upsert"] = "true"

    resp = requests.post(url, headers=headers, data=contenido, timeout=30)
    if resp.status_code in (200, 201):
        return True, None
    return False, f"Error subiendo archivo ({resp.status_code}): {resp.text[:300]}"


def url_firmada(path, expira_segundos=3600, forzar_descarga=False, nombre_descarga=None):
    """Genera una URL temporal para ver/descargar un archivo privado.
    Devuelve (url, error)."""
    if not storage_configurado():
        return None, "Storage no configurado (faltan SUPABASE_URL / SUPABASE_SERVICE_KEY en .env)"

    url = f"{SUPABASE_URL}/storage/v1/object/sign/{BUCKET}/{path}"
    body = {"expiresIn": expira_segundos}
    resp = requests.post(url, headers=_headers("application/json"), json=body, timeout=15)
    if resp.status_code != 200:
        return None, f"Error firmando URL ({resp.status_code}): {resp.text[:300]}"

    signed_path = resp.json().get("signedURL")
    if not signed_path:
        return None, "Respuesta de Supabase sin signedURL"

    firmada = f"{SUPABASE_URL}/storage/v1{signed_path}"
    if forzar_descarga:
        separador = "&" if "?" in firmada else "?"
        firmada += f"{separador}download={nombre_descarga or 'true'}"
    return firmada, None


def eliminar_archivo(path):
    if not storage_configurado():
        return False, "Storage no configurado"
    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET}/{path}"
    resp = requests.delete(url, headers=_headers(), timeout=15)
    if resp.status_code in (200, 204):
        return True, None
    return False, f"Error eliminando archivo ({resp.status_code}): {resp.text[:300]}"
