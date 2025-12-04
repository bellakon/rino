"""
Rutas para configuración de correos electrónicos
Permite editar plantillas, subir imágenes y configurar textos
"""
import os
import json
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pathlib import Path

from app.config.email_templates import (
    EMAIL_RESOURCES_PATH,
    REPORTE_ASISTENCIA_EMAIL,
    BITACORA_EMAIL,
    cargar_configuracion,
    guardar_configuracion,
    obtener_config
)
from app.config.smtp_config import SMTP_CONFIG

configuracion_bp = Blueprint('configuracion', __name__, url_prefix='/configuracion')

# Extensiones permitidas para imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@configuracion_bp.route('/')
def index():
    """Página principal de configuración"""
    return render_template('configuracion/index.html')


@configuracion_bp.route('/email')
def email_config():
    """Página de configuración de correos electrónicos"""
    # Obtener lista de imágenes disponibles
    imagenes = []
    if EMAIL_RESOURCES_PATH.exists():
        for archivo in EMAIL_RESOURCES_PATH.iterdir():
            if archivo.is_file() and allowed_file(archivo.name):
                imagenes.append({
                    'nombre': archivo.name,
                    'ruta': str(archivo),
                    'tamano': archivo.stat().st_size
                })
    
    # Configuración actual (cargada del archivo JSON)
    config = cargar_configuracion()
    
    # Agregar SMTP desde .env (solo lectura)
    config['smtp'] = SMTP_CONFIG
    
    return render_template(
        'configuracion/email.html',
        config=config,
        imagenes=imagenes,
        plantilla_html=REPORTE_ASISTENCIA_EMAIL.get('cuerpo_html', ''),
        plantilla_texto=BITACORA_EMAIL.get('cuerpo_texto', '')
    )


@configuracion_bp.route('/email/guardar', methods=['POST'])
def guardar_config_email():
    """Guarda la configuración de plantillas de correo electrónico"""
    try:
        data = request.get_json()
        
        # Cargar configuración actual
        config = cargar_configuracion()
        
        # Actualizar solo plantillas (SMTP no se edita, viene de .env)
        if 'imagen_encabezado' in data:
            config['imagen_encabezado'] = data['imagen_encabezado']
        if 'imagen_secundaria' in data:
            config['imagen_secundaria'] = data['imagen_secundaria']
        if 'remitente_nombre' in data:
            config['remitente_nombre'] = data['remitente_nombre']
        if 'remitente_departamento' in data:
            config['remitente_departamento'] = data['remitente_departamento']
        if 'usar_plantilla_html' in data:
            config['usar_plantilla_html'] = data['usar_plantilla_html']
        
        # Guardar
        exito, error = guardar_configuracion(config)
        
        if not exito:
            return jsonify({'success': False, 'error': error}), 500
        
        return jsonify({
            'success': True, 
            'mensaje': 'Configuración guardada correctamente',
            'config': config
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/email/obtener', methods=['GET'])
def obtener_config_email():
    """Obtiene la configuración actual de correo"""
    config = cargar_configuracion()
    return jsonify({'success': True, 'config': config})


@configuracion_bp.route('/email/probar', methods=['POST'])
def probar_correo():
    """Envía un correo de prueba con la plantilla configurada"""
    try:
        from app.config.email_templates import formatear_plantilla, REPORTE_ASISTENCIA_EMAIL, obtener_ruta_imagen
        from app.config.smtp_config import SMTP_CONFIG
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.image import MIMEImage
        import mimetypes
        from datetime import datetime
        
        data = request.get_json()
        email_destino = data.get('email')
        
        if not email_destino:
            return jsonify({'success': False, 'error': 'Email destino requerido'}), 400
        
        # Cargar configuración
        config = cargar_configuracion()
        usar_html = config.get('usar_plantilla_html', True)
        
        # Variables de ejemplo
        variables = {
            'nombre': 'USUARIO DE PRUEBA',
            'num_trabajador': '999',
            'periodo_inicio': '01/12/2025',
            'periodo_fin': '15/12/2025',
            'total_dias': '15',
            'descripcion_quincena': 'Primera quincena de Diciembre',
            'quincena': '1',
            'mes': 'Diciembre',
            'anio': '2025',
            'fecha_limite_justificaciones': '22 de Diciembre del presente año',
            'departamento': 'Recursos Humanos'
        }
        
        # Crear mensaje
        if usar_html:
            plantilla_formateada = formatear_plantilla(REPORTE_ASISTENCIA_EMAIL, variables)
            
            mensaje = MIMEMultipart('mixed')
            mensaje['From'] = f"{SMTP_CONFIG['from_name']} <{SMTP_CONFIG['from_email']}>"
            mensaje['To'] = email_destino
            mensaje['Subject'] = f"[PRUEBA] {plantilla_formateada['asunto']}"
            
            # Contenedor related para HTML + imágenes
            mensaje_related = MIMEMultipart('related')
            mensaje_alt = MIMEMultipart('alternative')
            
            # Texto plano
            if plantilla_formateada.get('cuerpo_texto'):
                texto_plano = MIMEText(plantilla_formateada['cuerpo_texto'], 'plain', 'utf-8')
                mensaje_alt.attach(texto_plano)
            
            # HTML
            if plantilla_formateada.get('cuerpo_html'):
                texto_html = MIMEText(plantilla_formateada['cuerpo_html'], 'html', 'utf-8')
                mensaje_alt.attach(texto_html)
            
            mensaje_related.attach(mensaje_alt)
            
            # Adjuntar imágenes
            for clave_imagen in ['imagen_encabezado', 'imagen_secundaria']:
                nombre_archivo = config.get(clave_imagen)
                if nombre_archivo:
                    ruta_imagen = obtener_ruta_imagen(nombre_archivo)
                    if ruta_imagen.exists():
                        mime_type, _ = mimetypes.guess_type(str(ruta_imagen))
                        if not mime_type or not mime_type.startswith('image/'):
                            mime_type = 'image/png'
                        subtype = mime_type.split('/')[1]
                        
                        with open(ruta_imagen, 'rb') as f:
                            imagen = MIMEImage(f.read(), _subtype=subtype)
                            imagen.add_header('Content-ID', f'<{clave_imagen}>')
                            imagen.add_header('Content-Disposition', 'inline', filename=nombre_archivo)
                            mensaje_related.attach(imagen)
            
            mensaje.attach(mensaje_related)
        else:
            # Texto plano simple
            from app.config.email_templates import BITACORA_EMAIL
            plantilla_formateada = formatear_plantilla(BITACORA_EMAIL, variables)
            
            mensaje = MIMEMultipart()
            mensaje['From'] = f"{SMTP_CONFIG['from_name']} <{SMTP_CONFIG['from_email']}>"
            mensaje['To'] = email_destino
            mensaje['Subject'] = f"[PRUEBA] {plantilla_formateada['asunto']}"
            mensaje.set_charset('utf-8')
            mensaje.attach(MIMEText(plantilla_formateada['cuerpo_texto'], 'plain', 'utf-8'))
        
        # Enviar
        with smtplib.SMTP(SMTP_CONFIG['host'], SMTP_CONFIG['port']) as servidor:
            if SMTP_CONFIG['use_tls']:
                servidor.starttls()
            servidor.login(SMTP_CONFIG['username'], SMTP_CONFIG['password'])
            servidor.send_message(mensaje)
        
        return jsonify({'success': True, 'mensaje': f'Correo de prueba enviado a {email_destino}'})
        
    except smtplib.SMTPAuthenticationError:
        return jsonify({'success': False, 'error': 'Error de autenticación SMTP. Verifica credenciales en .env'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error al enviar correo: {str(e)}'}), 500


@configuracion_bp.route('/email/subir-imagen', methods=['POST'])
def subir_imagen():
    """Subir una imagen para usar en correos"""
    if 'imagen' not in request.files:
        return jsonify({'success': False, 'error': 'No se seleccionó archivo'}), 400
    
    archivo = request.files['imagen']
    
    if archivo.filename == '':
        return jsonify({'success': False, 'error': 'No se seleccionó archivo'}), 400
    
    if not allowed_file(archivo.filename):
        return jsonify({'success': False, 'error': 'Tipo de archivo no permitido. Use PNG, JPG o GIF'}), 400
    
    try:
        # Crear directorio si no existe
        EMAIL_RESOURCES_PATH.mkdir(parents=True, exist_ok=True)
        
        # Guardar archivo
        filename = secure_filename(archivo.filename)
        ruta_destino = EMAIL_RESOURCES_PATH / filename
        archivo.save(str(ruta_destino))
        
        return jsonify({
            'success': True,
            'mensaje': f'Imagen {filename} subida correctamente',
            'nombre': filename
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/email/eliminar-imagen', methods=['POST'])
def eliminar_imagen():
    """Eliminar una imagen de los recursos de correo"""
    nombre = request.json.get('nombre')
    
    if not nombre:
        return jsonify({'success': False, 'error': 'Nombre de archivo requerido'}), 400
    
    try:
        ruta = EMAIL_RESOURCES_PATH / secure_filename(nombre)
        
        if ruta.exists():
            ruta.unlink()
            return jsonify({'success': True, 'mensaje': f'Imagen {nombre} eliminada'})
        else:
            return jsonify({'success': False, 'error': 'Archivo no encontrado'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@configuracion_bp.route('/email/listar-imagenes')
def listar_imagenes():
    """Listar imágenes disponibles"""
    imagenes = []
    
    if EMAIL_RESOURCES_PATH.exists():
        for archivo in EMAIL_RESOURCES_PATH.iterdir():
            if archivo.is_file() and allowed_file(archivo.name):
                imagenes.append({
                    'nombre': archivo.name,
                    'tamano': archivo.stat().st_size,
                    'url': f'/configuracion/email/imagen/{archivo.name}'
                })
    
    return jsonify({'imagenes': imagenes})


@configuracion_bp.route('/email/imagen/<nombre>')
def ver_imagen(nombre):
    """Servir una imagen de recursos de correo"""
    from flask import send_from_directory
    
    nombre_seguro = secure_filename(nombre)
    return send_from_directory(str(EMAIL_RESOURCES_PATH), nombre_seguro)


@configuracion_bp.route('/email/preview')
def preview_email():
    """Vista previa de la plantilla de correo HTML"""
    from app.config.email_templates import formatear_plantilla, REPORTE_ASISTENCIA_EMAIL, cargar_configuracion
    
    # Variables de ejemplo para preview
    variables_ejemplo = {
        'nombre': 'JUAN PÉREZ GONZÁLEZ',
        'num_trabajador': '123',
        'periodo_inicio': '01/12/2025',
        'periodo_fin': '15/12/2025',
        'total_dias': '15',
        'descripcion_quincena': 'Primera quincena de Diciembre',
        'quincena': '1',
        'mes': 'Diciembre',
        'anio': '2025',
        'fecha_limite_justificaciones': '22 de Diciembre del presente año',
        'departamento': 'Recursos Humanos'
    }
    
    plantilla_formateada = formatear_plantilla(REPORTE_ASISTENCIA_EMAIL, variables_ejemplo)
    
    # Cargar configuración actual
    config = cargar_configuracion()
    
    # Buscar imágenes disponibles en el directorio
    imagenes_disponibles = []
    if EMAIL_RESOURCES_PATH.exists():
        imagenes_disponibles = [f.name for f in EMAIL_RESOURCES_PATH.iterdir() 
                                if f.is_file() and allowed_file(f.name)]
    
    # Usar las imágenes configuradas o las primeras disponibles
    imagen_encabezado = config.get('imagen_encabezado', '')
    imagen_secundaria = config.get('imagen_secundaria', '')
    
    # Si la imagen configurada no existe, usar la primera disponible
    if imagen_encabezado not in imagenes_disponibles and imagenes_disponibles:
        imagen_encabezado = imagenes_disponibles[0]
    if imagen_secundaria not in imagenes_disponibles and len(imagenes_disponibles) > 1:
        imagen_secundaria = imagenes_disponibles[1]
    elif imagen_secundaria not in imagenes_disponibles and imagenes_disponibles:
        imagen_secundaria = imagenes_disponibles[0]
    
    # Reemplazar los CID de imágenes con URLs para preview (con cache busting)
    import time
    cache_bust = int(time.time())
    html = plantilla_formateada.get('cuerpo_html', '')
    
    if imagen_encabezado:
        html = html.replace('cid:imagen_encabezado', f'/configuracion/email/imagen/{imagen_encabezado}?t={cache_bust}')
    else:
        # Remover la etiqueta img si no hay imagen
        html = html.replace('<img src="cid:imagen_encabezado" alt="Logo Institucional">', '<!-- Sin logo -->')
    
    if imagen_secundaria:
        html = html.replace('cid:imagen_secundaria', f'/configuracion/email/imagen/{imagen_secundaria}?t={cache_bust}')
    else:
        html = html.replace('<img src="cid:imagen_secundaria" alt="Banner">', '<!-- Sin banner -->')
    
    return html
