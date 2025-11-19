"""
Rutas para el feature de asistencias
Responsabilidad: mostrar asistencias de la base de datos
"""
from flask import Blueprint, render_template, flash, request, Response, jsonify, stream_with_context, session
from app.features.asistencias.services.obtener_asistencias_use_case import obtener_asistencias_use_case
from app.features.asistencias.services.importar_checadas_use_case import importar_checadas_use_case
import math
import json
import uuid

# Crear blueprint
asistencias_bp = Blueprint('asistencias', __name__, url_prefix='/asistencias')

# Cache temporal para guardar checadas entre requests (mejor que sesión)
# Key: session_id, Value: checadas_pendientes
_checadas_cache = {}


@asistencias_bp.route('/')
def index():
    """Ver asistencias guardadas en la base de datos con filtros, ordenación y paginación"""
    
    # Obtener parámetros de query string
    num_trabajador = request.args.get('num_trabajador', type=int)
    checador = request.args.get('checador', type=str)
    fecha_inicio = request.args.get('fecha_inicio', type=str)
    fecha_fin = request.args.get('fecha_fin', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 50  # Registros por página
    
    # Ordenación
    order_by = request.args.get('order_by', 'id')  # Campo por el cual ordenar
    order_dir = request.args.get('order_dir', 'desc')  # Dirección: asc o desc
    
    # Validar columnas permitidas para ordenar
    columnas_permitidas = ['id', 'num_trabajador', 'nombre', 'fecha', 'hora', 'checador']
    if order_by not in columnas_permitidas:
        order_by = 'id'
    
    if order_dir not in ['asc', 'desc']:
        order_dir = 'desc'
    
    # Usar caso de uso con filtros, ordenación y paginación
    resultado, error = obtener_asistencias_use_case.ejecutar(
        num_trabajador=num_trabajador,
        checador=checador,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        page=page,
        per_page=per_page,
        order_by=order_by,
        order_dir=order_dir
    )
    
    if error:
        flash(f'Error al consultar: {error}', 'error')
        resultado = {'asistencias': [], 'total': 0, 'page': 1, 'per_page': per_page}
    
    # Calcular información de paginación
    total_pages = math.ceil(resultado['total'] / resultado['per_page']) if resultado['total'] > 0 else 1
    has_prev = resultado['page'] > 1
    has_next = resultado['page'] < total_pages
    
    return render_template(
        'asistencias/index.html',
        asistencias=resultado['asistencias'],
        total=resultado['total'],
        page=resultado['page'],
        per_page=resultado['per_page'],
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next,
        num_trabajador_filter=num_trabajador,
        checador_filter=checador or '',
        fecha_inicio_filter=fecha_inicio or '',
        fecha_fin_filter=fecha_fin or '',
        order_by=order_by,
        order_dir=order_dir
    )


@asistencias_bp.route('/importar', methods=['POST'])
def importar_checadas():
    """
    Analiza archivo .res y retorna preview para confirmación
    NO inserta datos todavía
    """
    
    # Validar que se envió un archivo
    if 'archivo' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo'}), 400
    
    archivo = request.files['archivo']
    
    if archivo.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    # Validar extensión .res
    if not archivo.filename.endswith('.res'):
        return jsonify({'error': 'El archivo debe tener extensión .res'}), 400
    
    # Leer contenido del archivo
    try:
        archivo_contenido = archivo.read().decode('utf-8')
    except UnicodeDecodeError:
        try:
            # Intentar con latin-1 si UTF-8 falla
            archivo.seek(0)
            archivo_contenido = archivo.read().decode('latin-1')
        except Exception as e:
            return jsonify({'error': f'Error al leer archivo: {str(e)}'}), 400
    
    # Crear nueva instancia del caso de uso para este request
    from app.features.asistencias.services.importar_checadas_use_case import ImportarChecadasUseCase
    caso_uso = ImportarChecadasUseCase()
    
    # Generar ID único para esta sesión de importación
    import_session_id = str(uuid.uuid4())
    
    # Función generadora para SSE (análisis solamente)
    def generar_eventos():
        """Genera eventos SSE con progreso de análisis"""
        try:
            for progreso in caso_uso.ejecutar(archivo_contenido):
                # Si llegamos a la fase de preview, guardar en cache
                if progreso.get('requiere_confirmacion'):
                    # Guardar checadas en cache temporal
                    _checadas_cache[import_session_id] = caso_uso.checadas_pendientes
                    # Enviar session_id al frontend
                    progreso['import_session_id'] = import_session_id
                
                yield f"data: {json.dumps(progreso)}\n\n"
        except Exception as e:
            # Error no capturado en el caso de uso
            yield f"data: {json.dumps({'error': str(e), 'finalizado': True})}\n\n"
    
    # Retornar respuesta SSE
    return Response(
        stream_with_context(generar_eventos()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'  # Desactivar buffering en nginx
        }
    )


@asistencias_bp.route('/importar-confirmar', methods=['POST'])
def importar_confirmar():
    """
    Confirma e inserta checadas después del preview
    Obtiene las checadas desde el cache (no desde el frontend)
    """
    
    # Obtener import_session_id del body
    data = request.get_json()
    if not data or 'import_session_id' not in data:
        return jsonify({'error': 'No se proporcionó import_session_id'}), 400
    
    import_session_id = data['import_session_id']
    
    # Obtener checadas desde cache
    if import_session_id not in _checadas_cache:
        return jsonify({'error': 'No hay checadas pendientes. Por favor analice el archivo nuevamente.'}), 400
    
    checadas_nuevas = _checadas_cache[import_session_id]
    
    if not isinstance(checadas_nuevas, list) or len(checadas_nuevas) == 0:
        return jsonify({'error': 'Lista de checadas inválida o vacía'}), 400
    
    # Función generadora para SSE (inserción)
    def generar_eventos():
        """Genera eventos SSE con progreso de inserción"""
        try:
            for progreso in importar_checadas_use_case.ejecutar_insercion(checadas_nuevas):
                yield f"data: {json.dumps(progreso)}\n\n"
            
            # Limpiar cache después de insertar
            _checadas_cache.pop(import_session_id, None)
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e), 'finalizado': True})}\n\n"
    
    # Retornar respuesta SSE
    return Response(
        stream_with_context(generar_eventos()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )


