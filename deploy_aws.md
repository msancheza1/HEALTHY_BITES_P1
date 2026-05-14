# Deployment en AWS

## 1. Preparar estáticos en el servidor

Después de hacer deploy, conecta al servidor EC2 y ejecuta:

```bash
cd /path/to/healthybites
python manage.py collectstatic --noinput
```

Esto reunirá todos los archivos estáticos en `staticfiles/`.

## 2. Variables de entorno en AWS

En tu servidor EC2, crea o actualiza el archivo `.env`:

```bash
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,tu-ip-elastica.compute.amazonaws.com
```

## 3. Configurar Nginx (si usas Nginx como proxy)

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    # Estáticos (servidos por Nginx directamente)
    location /static/ {
        alias /path/to/healthybites/staticfiles/;
        expires 30d;
    }

    # Media (recetas e imágenes)
    location /media/ {
        alias /path/to/healthybites/media/;
        expires 30d;
    }

    # Django app (Gunicorn)
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 4. Ejecutar con Gunicorn

```bash
gunicorn healthybites.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## 5. Asegurar permisos de archivos

```bash
# Permisos para estáticos
chmod -R 755 /path/to/healthybites/staticfiles/
chmod -R 755 /path/to/healthybites/media/

# Usuario que ejecuta la app
sudo chown -R appuser:appuser /path/to/healthybites/
```

## Resumen de cambios

✅ **WhiteNoise** - Sirve estáticos automáticamente en producción
✅ **DEBUG variable** - Controla modo debug desde `.env`
✅ **ALLOWED_HOSTS variable** - Configurable por entorno
✅ **Media siempre servida** - Funciona en local y producción
✅ **Seguridad HTTPS** - Habilitado en producción automáticamente
