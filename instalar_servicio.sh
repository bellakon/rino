#!/bin/bash
# Script para instalar TecnoTime como servicio systemd

echo "=========================================="
echo "Instalación de TecnoTime como Servicio"
echo "=========================================="

# Verificar que se ejecuta como root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ ERROR: Este script debe ejecutarse como root (sudo)"
    exit 1
fi

# Crear directorios de logs
echo "📁 Creando directorio de logs..."
mkdir -p /var/log/tecnotime
chown ccomputo:ccomputo /var/log/tecnotime

# Instalar gunicorn si no está instalado
echo "📦 Instalando gunicorn..."
/home/ccomputo/projects/rino/.venv/bin/pip install gunicorn

# Copiar archivo de servicio
echo "📄 Copiando archivo de servicio..."
cp /home/ccomputo/projects/rino/tecnotime.service /etc/systemd/system/

# Recargar systemd
echo "🔄 Recargando systemd..."
systemctl daemon-reload

# Habilitar el servicio para que inicie automáticamente
echo "✅ Habilitando servicio..."
systemctl enable tecnotime.service

# Iniciar el servicio
echo "🚀 Iniciando servicio..."
systemctl start tecnotime.service

# Mostrar estado
echo ""
echo "=========================================="
echo "Estado del Servicio"
echo "=========================================="
systemctl status tecnotime.service --no-pager

echo ""
echo "=========================================="
echo "✅ Instalación Completada"
echo "=========================================="
echo ""
echo "Comandos útiles:"
echo "  • Ver estado:      sudo systemctl status tecnotime"
echo "  • Iniciar:         sudo systemctl start tecnotime"
echo "  • Detener:         sudo systemctl stop tecnotime"
echo "  • Reiniciar:       sudo systemctl restart tecnotime"
echo "  • Ver logs:        sudo journalctl -u tecnotime -f"
echo "  • Logs de acceso:  sudo tail -f /var/log/tecnotime/access.log"
echo "  • Logs de error:   sudo tail -f /var/log/tecnotime/error.log"
echo ""
echo "La aplicación está corriendo en: http://localhost:5000"
echo "=========================================="
