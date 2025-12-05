#!/bin/bash
# Script para configurar TecnoTime con Tailscale Funnel

echo "=========================================="
echo "Configuración de Tailscale para TecnoTime"
echo "=========================================="

# Verificar que se ejecuta como root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ ERROR: Este script debe ejecutarse como root (sudo)"
    exit 1
fi

# Verificar si Tailscale ya está instalado
if command -v tailscale &> /dev/null; then
    echo "✅ Tailscale ya está instalado"
else
    echo "📦 Instalando Tailscale..."
    curl -fsSL https://tailscale.com/install.sh | sh
fi

# Verificar si ya está autenticado
if tailscale status &> /dev/null; then
    echo "✅ Tailscale ya está autenticado"
    echo ""
    tailscale status | head -5
else
    echo ""
    echo "🔐 Iniciando autenticación de Tailscale..."
    echo "Se abrirá un navegador para autenticar tu cuenta"
    echo ""
    tailscale up
fi

echo ""
echo "=========================================="
echo "Configuración de Tailscale Funnel"
echo "=========================================="
echo ""
echo "Tailscale Funnel permite acceso público desde Internet"
echo ""
echo "Opciones disponibles:"
echo "  1) Serve (solo usuarios de tu Tailnet - privado)"
echo "  2) Funnel (acceso público desde Internet)"
echo ""
read -p "Selecciona una opción (1 o 2): " opcion

if [ "$opcion" = "1" ]; then
    echo ""
    echo "🔒 Configurando Tailscale Serve (solo tu red Tailscale)..."
    tailscale serve --bg 5000
    
    echo ""
    echo "=========================================="
    echo "✅ Tailscale Serve Configurado"
    echo "=========================================="
    echo ""
    echo "Tu aplicación es accesible SOLO para usuarios de tu Tailnet en:"
    HOSTNAME=$(tailscale status --json | grep -o '"HostName":"[^"]*"' | cut -d'"' -f4 | head -1)
    echo "  • https://${HOSTNAME}"
    echo ""
    echo "Los usuarios necesitan:"
    echo "  1. Tener Tailscale instalado"
    echo "  2. Estar conectados a tu misma red Tailscale"
    echo ""

elif [ "$opcion" = "2" ]; then
    echo ""
    echo "🌐 Configurando Tailscale Funnel (acceso público)..."
    echo ""
    echo "IMPORTANTE: Funnel requiere que tu cuenta Tailscale tenga la función habilitada"
    echo "Visita: https://login.tailscale.com/admin/settings/features"
    echo ""
    read -p "¿Continuar? (s/n): " continuar
    
    if [ "$continuar" != "s" ] && [ "$continuar" != "S" ]; then
        echo "❌ Configuración cancelada"
        exit 1
    fi
    
    tailscale funnel --bg 5000
    
    echo ""
    echo "=========================================="
    echo "✅ Tailscale Funnel Configurado"
    echo "=========================================="
    echo ""
    HOSTNAME=$(tailscale status --json | grep -o '"HostName":"[^"]*"' | cut -d'"' -f4 | head -1)
    echo "Tu aplicación es accesible públicamente en:"
    echo "  • https://${HOSTNAME}"
    echo ""
    echo "⚠️  IMPORTANTE:"
    echo "  • Esta URL es accesible desde CUALQUIER parte de Internet"
    echo "  • Asegúrate de tener autenticación en tu aplicación"
    echo "  • Tailscale proporciona certificado SSL automáticamente"
    echo ""
else
    echo "❌ Opción inválida"
    exit 1
fi

echo "Comandos útiles:"
echo "  • Ver estado:           tailscale status"
echo "  • Ver configuración:    tailscale serve status"
echo "  • Detener Serve/Funnel: tailscale serve reset"
echo "  • Desconectar:          tailscale down"
echo "  • Logs:                 journalctl -u tailscaled -f"
echo ""
echo "Para acceder desde otros dispositivos:"
echo "  • Instala Tailscale: https://tailscale.com/download"
echo "  • Inicia sesión con la misma cuenta"
echo "=========================================="
