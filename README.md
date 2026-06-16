# DocGestoría · Panel web

Panel de gestión documental para gestorías. Flask + Jinja2, listo para Vercel.

## Estructura

```
docgestoria/
├── app.py              # Rutas Flask
├── data.py             # Datos de ejemplo (reemplazar por BD)
├── requirements.txt
├── vercel.json
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── clientes.html
│   ├── detalle.html
│   ├── documentos.html
│   ├── expedientes.html
│   ├── notificaciones.html
│   ├── ajustes.html
│   └── partials/
│       └── badge.html
└── static/
    ├── css/main.css
    └── js/main.js
```

## Correr en local

```bash
pip install -r requirements.txt
python app.py
# Abre http://localhost:5000
```

## Desplegar en Vercel

1. Instala Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Desde la carpeta del proyecto:
   ```bash
   vercel
   ```

3. Sigue los pasos del asistente. En la primera vez te pedirá login.

4. Para producción:
   ```bash
   vercel --prod
   ```

## Próximos pasos

- Reemplazar `data.py` por PostgreSQL (con SQLAlchemy o psycopg2)
- Añadir autenticación (Flask-Login)
- Conectar Stripe para pagos
- Añadir subida real de archivos (AWS S3 o Supabase Storage)
