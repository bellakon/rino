"""
Rutas para el feature de checadores
Responsabilidad: gestionar checadores y verificar conexiones
"""
from flask import Blueprint, render_template, jsonify, request
from app.features.checadores.services.verificar_conexion_use_case import verificar_conexion_use_case
from app.features.checadores.services.consultar_trabajadores_use_case import consultar_trabajadores_use_case

# Crear blueprint
checadores_bp = Blueprint('checadores', __name__, url_prefix='/checadores')


@checadores_bp.route('/')
def index():
    """Listar checadores disponibles"""
    checadores = verificar_conexion_use_case.obtener_checadores()
    return render_template(
        'checadores/index.html',
        checadores=checadores
    )


@checadores_bp.route('/verificar')
def verificar_conexion():
    """API: Verificar conexión de un checador"""
    checador_id = request.args.get('checador_id')
    
    if not checador_id:
        return jsonify({'error': 'ID de checador requerido'}), 400
    
    checador, conectado, info_dispositivo, error = verificar_conexion_use_case.verificar_conexion(checador_id)
    
    if checador is None:
        return jsonify({'error': error}), 404
    
    return jsonify({
        'checador': checador.to_dict(),
        'conectado': conectado,
        'info_dispositivo': info_dispositivo,
        'error_mensaje': error if not conectado else None
    })


@checadores_bp.route('/trabajadores')
def consultar_trabajadores():
    """API: Obtener trabajadores registrados en un checador"""
    checador_id = request.args.get('checador_id')
    
    if not checador_id:
        return jsonify({'error': 'ID de checador requerido'}), 400
    
    checador, trabajadores, error = consultar_trabajadores_use_case.ejecutar(checador_id)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'checador': checador.to_dict(),
        'trabajadores': trabajadores
    })
