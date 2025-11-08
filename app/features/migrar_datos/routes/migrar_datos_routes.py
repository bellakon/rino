"""
Rutas: Migrar Datos a RinoTime
"""
from flask import Blueprint, render_template, request, jsonify, Response, stream_with_context
from app.features.migrar_datos.services.verificar_conexion_rinotime_use_case import verificar_conexion_rinotime_use_case
from app.features.migrar_datos.services.migrar_asistencias_rinotime_use_case import migrar_asistencias_rinotime_use_case
from app.config.checadores_config import CheckadoresConfig
import json


migrar_datos_bp = Blueprint(
    'migrar_datos',
    __name__,
    url_prefix='/migrar-datos',
    template_folder='../templates'
)


@migrar_datos_bp.route('/')
def index():
    """Página principal de migración de datos"""
    return render_template('migrar_datos/index.html')


@migrar_datos_bp.route('/checadores-disponibles')
def checadores_disponibles():
    """Obtiene la lista de checadores únicos desde la BD de asistencias con info adicional"""
    from app.core.database.query_executor import QueryExecutor
    from app.core.database.connection import db_connection
    
    query_executor = QueryExecutor(db_connection)
    
    # Obtener checadores únicos con conteo de asistencias
    query = """
        SELECT 
            checador,
            COUNT(*) as total_asistencias,
            MIN(fecha) as primera_fecha,
            MAX(fecha) as ultima_fecha
        FROM asistencias 
        WHERE checador IS NOT NULL 
        GROUP BY checador
        ORDER BY checador
    """
    
    result, error = query_executor.ejecutar(query)
    
    if error:
        return jsonify({'error': error}), 500
    
    # Enriquecer con información de la configuración si existe
    checadores_info = []
    if result:
        for row in result:
            checador_serial = row['checador']
            
            # Buscar en la configuración si existe un checador con este serial o IP
            checador_config = None
            for config in CheckadoresConfig.get_checadores_activos():
                # Comparar por serial number obtenido o por IP
                if config.get('ip') == checador_serial or config.get('nombre', '').upper() in checador_serial.upper():
                    checador_config = config
                    break
            
            checadores_info.append({
                'serial': checador_serial,
                'nombre': checador_config['nombre'] if checador_config else 'Sin nombre',
                'ubicacion': checador_config['ubicacion'] if checador_config else 'Sin ubicación',
                'total_asistencias': row['total_asistencias'],
                'primera_fecha': str(row['primera_fecha']),
                'ultima_fecha': str(row['ultima_fecha'])
            })
    
    return jsonify({'checadores': checadores_info})


@migrar_datos_bp.route('/verificar-conexion')
def verificar_conexion():
    """Verifica la conexión a RinoTime"""
    info, error = verificar_conexion_rinotime_use_case.ejecutar()
    
    if error:
        return jsonify({'error': error}), 500
    
    return jsonify(info)


@migrar_datos_bp.route('/contar-asistencias')
def contar_asistencias():
    """Cuenta las asistencias a migrar según filtros"""
    checador = request.args.get('checador')
    
    total, error = migrar_asistencias_rinotime_use_case.contar_asistencias(
        checador=checador
    )
    
    if error:
        return jsonify({'error': error}), 500
    
    return jsonify({'total': total})


@migrar_datos_bp.route('/migrar', methods=['POST'])
def migrar():
    """Migra asistencias a RinoTime (streaming)"""
    data = request.get_json()
    
    terminal_sn = data.get('terminal_sn')
    checador = data.get('checador')
    
    if not terminal_sn:
        return jsonify({'error': 'Debe seleccionar un terminal'}), 400
    
    def generate():
        """Genera eventos SSE con el progreso"""
        for progreso in migrar_asistencias_rinotime_use_case.ejecutar(
            terminal_sn=terminal_sn,
            checador=checador
        ):
            yield f"data: {json.dumps(progreso)}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )
