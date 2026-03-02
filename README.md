Matrimonios Divinos — Aplicación web (Flask)

Descripción

Proyecto de sitio para `Erica Guevara - Psicóloga Cristiana` con panel de administración, agenda, galería y gestión de servicios/precios.

Archivos importantes

- `psicologia_app.py` — app principal (Flask)
- `requirements.txt` — dependencias
- `Procfile` — comando para iniciar en plataformas como Render
- `templates/` y `static/` — frontend

Preparar y subir a GitHub

1. Crea un repositorio nuevo en GitHub (por ejemplo `matrimonios-divinos`).
2. En tu máquina, añade el remote y sube:

```bash
cd "c:/Users/KEVIN VIDES/Downloads/proyectojaa"
git remote add origin https://github.com/VIDES_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

(reemplaza `VIDES_USERNAME` y `REPO_NAME` por los tuyos).

Desplegar en Render (rápido)

1. Crea cuenta en https://render.com y conecta tu GitHub.
2. Click en "New" → "Web Service" → selecciona el repo.
3. En "Build Command" deja `pip install -r requirements.txt` (Render lo detecta automáticamente).
4. En "Start Command" escribe: `gunicorn psicologia_app:app`
5. Despliega. Render instalará dependencias y expondrá la app con HTTPS.

Notas útiles

- Admin por defecto: usuario `Erica`, contraseña `matrimoniosdivinos` (si actualizaste DB con `update_admin.py`).
- Si ya tienes datos en `psicologia.db`, no la borres.
- Para permitir uploads en producción asegúrate de usar un bucket (S3) o cambiar la configuración si prefieres mantener archivos en el servidor.

Si quieres, puedo ayudarte a:
- crear el repo en GitHub desde la CLI (si me das permiso para ejecutar comandos),
- conectar y desplegar en Render paso a paso.
