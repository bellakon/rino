# Instalación de TecnoTime como Servicio en Linux

## Instalación Rápida

1. **Dar permisos de ejecución al script:**
```bash
chmod +x instalar_servicio.sh
```

2. **Ejecutar el script de instalación:**
```bash
sudo ./instalar_servicio.sh
```

¡Listo! El servicio ya estará corriendo.

---

## Comandos Útiles

### Control del Servicio
```bash
# Ver estado del servicio
sudo systemctl status tecnotime

# Iniciar el servicio
sudo systemctl start tecnotime

# Detener el servicio
sudo systemctl stop tecnotime

# Reiniciar el servicio
sudo systemctl restart tecnotime

# Deshabilitar inicio automático
sudo systemctl disable tecnotime

# Habilitar inicio automático
sudo systemctl enable tecnotime
```

### Ver Logs
```bash
# Logs en tiempo real (systemd)
sudo journalctl -u tecnotime -f

# Logs de acceso (Gunicorn)
sudo tail -f /var/log/tecnotime/access.log

# Logs de error (Gunicorn)
sudo tail -f /var/log/tecnotime/error.log

# Ver los últimos 100 logs
sudo journalctl -u tecnotime -n 100

# Ver logs desde hoy
sudo journalctl -u tecnotime --since today
```

---

## Instalación Manual (Paso a Paso)

Si prefieres instalar manualmente sin el script:

### 1. Instalar Gunicorn
```bash
source .venv/bin/activate
pip install gunicorn
```

### 2. Crear directorio de logs
```bash
sudo mkdir -p /var/log/tecnotime
sudo chown ccomputo:ccomputo /var/log/tecnotime
```

### 3. Copiar archivo de servicio
```bash
sudo cp tecnotime.service /etc/systemd/system/
```

### 4. Recargar systemd
```bash
sudo systemctl daemon-reload
```

### 5. Habilitar e iniciar el servicio
```bash
sudo systemctl enable tecnotime
sudo systemctl start tecnotime
```

### 6. Verificar estado
```bash
sudo systemctl status tecnotime
```

---

## Configuración del Servicio

El archivo `tecnotime.service` contiene:

- **Usuario:** `ccomputo` (el servicio corre con tu usuario)
- **Puerto:** `5000` (puedes cambiarlo en el archivo)
- **Workers:** `4` (procesos simultáneos de Gunicorn)
- **Timeout:** `120` segundos
- **Reinicio automático:** Sí, si el servicio falla se reinicia solo
- **Variables de entorno:** Lee del archivo `.env`

### Modificar el Puerto o Workers

Edita el archivo de servicio:
```bash
sudo nano /etc/systemd/system/tecnotime.service
```

Cambia la línea `ExecStart`:
```ini
# Ejemplo: Cambiar puerto a 8080 con 8 workers
ExecStart=/home/ccomputo/projects/rino/.venv/bin/gunicorn --bind 0.0.0.0:8080 --workers 8 ...
```

Luego recarga y reinicia:
```bash
sudo systemctl daemon-reload
sudo systemctl restart tecnotime
```

---

## Acceso desde Otros Equipos

El servicio está configurado para escuchar en `0.0.0.0:5000`, lo que significa que es accesible desde cualquier equipo en tu red.

Para acceder desde otro equipo:
```
http://IP_DEL_SERVIDOR:5000
```

### Ejemplo:
Si tu servidor tiene IP `192.168.1.100`:
```
http://192.168.1.100:5000
```

### Configurar el Firewall
Si no puedes acceder, abre el puerto en el firewall:
```bash
sudo ufw allow 5000/tcp
sudo ufw reload
```

---

## Nginx como Proxy Reverso (Opcional)

Para producción, es recomendable usar Nginx delante de Gunicorn:

### 1. Instalar Nginx
```bash
sudo apt install nginx
```

### 2. Crear configuración
```bash
sudo nano /etc/nginx/sites-available/tecnotime
```

Contenido:
```nginx
server {
    listen 80;
    server_name tu-dominio.com;  # O tu IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts para archivos grandes
        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
        send_timeout 600;
    }

    # Aumentar límite de tamaño de archivo
    client_max_body_size 1G;
}
```

### 3. Activar configuración
```bash
sudo ln -s /etc/nginx/sites-available/tecnotime /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Modificar el servicio para escuchar solo en localhost
Edita `/etc/systemd/system/tecnotime.service`:
```ini
# Cambiar de:
ExecStart=... --bind 0.0.0.0:5000 ...
# A:
ExecStart=... --bind 127.0.0.1:5000 ...
```

Luego:
```bash
sudo systemctl daemon-reload
sudo systemctl restart tecnotime
```

Ahora la aplicación será accesible en el puerto 80 (HTTP estándar) a través de Nginx.

---

## Solución de Problemas

### El servicio no inicia
```bash
# Ver logs detallados
sudo journalctl -u tecnotime -n 50

# Verificar que el archivo .env existe
ls -la /home/ccomputo/projects/rino/.env

# Verificar permisos
sudo chown -R ccomputo:ccomputo /home/ccomputo/projects/rino
```

### Error de permisos en MySQL
Verifica que las credenciales en `.env` sean correctas:
```bash
cat .env | grep DB_
```

### El servicio se detiene solo
Revisa los logs de error:
```bash
sudo tail -100 /var/log/tecnotime/error.log
```

### Cambios en el código no se reflejan
Reinicia el servicio después de modificar código:
```bash
sudo systemctl restart tecnotime
```

---

## Actualización de la Aplicación

Después de hacer cambios en el código:

```bash
# 1. Asegúrate de estar en el directorio correcto
cd /home/ccomputo/projects/rino

# 2. Activa el entorno virtual (si instalas nuevas dependencias)
source .venv/bin/activate

# 3. Instala nuevas dependencias (si las hay)
pip install -r requirements.txt

# 4. Reinicia el servicio
sudo systemctl restart tecnotime

# 5. Verifica que inició correctamente
sudo systemctl status tecnotime
```

---

## Desinstalación

Si necesitas desinstalar el servicio:

```bash
# Detener y deshabilitar el servicio
sudo systemctl stop tecnotime
sudo systemctl disable tecnotime

# Eliminar archivo de servicio
sudo rm /etc/systemd/system/tecnotime.service

# Recargar systemd
sudo systemctl daemon-reload

# (Opcional) Eliminar logs
sudo rm -rf /var/log/tecnotime
```

---

## Ventajas de Usar Gunicorn + Systemd

✅ **Inicio automático:** El servicio inicia automáticamente al encender el servidor  
✅ **Reinicio automático:** Si falla, se reinicia solo  
✅ **Multiple workers:** Maneja múltiples peticiones simultáneas  
✅ **Logs centralizados:** Todos los logs en un solo lugar  
✅ **Gestión sencilla:** Comandos systemctl estándar de Linux  
✅ **Producción ready:** Gunicorn es el servidor WSGI recomendado para Flask  

---

## Monitoreo del Servicio

Para verificar que todo funciona correctamente:

```bash
# CPU y memoria usada
ps aux | grep gunicorn

# Conexiones activas
sudo netstat -tulpn | grep 5000

# Estado del servicio cada 2 segundos
watch -n 2 'sudo systemctl status tecnotime'
```
