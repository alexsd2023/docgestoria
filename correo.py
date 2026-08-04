"""
Envío de emails vía Resend (https://resend.com), usado para las
solicitudes de documentos a clientes.

Credenciales en variables de entorno (ver .env.example):
  RESEND_API_KEY    -> API key de Resend (resend.com > API Keys)
  RESEND_FROM_EMAIL -> remitente. Con el dominio de pruebas
                       (onboarding@resend.dev) Resend solo entrega al email
                       con el que te registraste en Resend; para enviar a
                       clientes reales hace falta verificar un dominio propio.
"""
import os

import requests
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
RESEND_FROM_EMAIL = os.environ.get("RESEND_FROM_EMAIL", "onboarding@resend.dev")
GESTORIA_NOMBRE = os.environ.get("GESTORIA_NOMBRE", "DocGestoría")


def email_configurado():
    return bool(RESEND_API_KEY)


def enviar_email(destinatario, asunto, html):
    if not email_configurado():
        return False, "Email no configurado (falta RESEND_API_KEY en .env)"
    if not destinatario:
        return False, "El cliente no tiene email registrado"

    resp = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": RESEND_FROM_EMAIL,
            "to": [destinatario],
            "subject": asunto,
            "html": html,
        },
        timeout=15,
    )
    if resp.status_code in (200, 201):
        return True, None
    return False, f"Error enviando email ({resp.status_code}): {resp.text[:300]}"


def email_solicitud_documento(cliente_nombre, cliente_email, tramite, tipo_documento):
    asunto = f"Solicitud de documento: {tipo_documento}"
    html = f"""
    <div style="font-family:Arial,Helvetica,sans-serif;max-width:520px;margin:0 auto;color:#1a1a1a">
      <h2 style="margin-bottom:4px">{GESTORIA_NOMBRE}</h2>
      <p>Hola {cliente_nombre},</p>
      <p>Para continuar con tu trámite de <strong>{tramite}</strong> necesitamos que nos envíes el siguiente documento:</p>
      <p style="background:#f3f4f6;padding:12px 16px;border-radius:8px;font-weight:600;margin:16px 0">
        {tipo_documento}
      </p>
      <p>Puedes responder a este correo adjuntándolo, o entregárnoslo por cualquier otro medio habitual.</p>
      <p>Gracias,<br>{GESTORIA_NOMBRE}</p>
    </div>
    """
    return enviar_email(cliente_email, asunto, html)
