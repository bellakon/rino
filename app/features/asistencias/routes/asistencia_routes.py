"""
Rutas para el feature de asistencias
Responsabilidad: mostrar asistencias de la base de datos
"""
from flask import Blueprint, render_template, flash, request
from app.features.asistencias.services.obtener_asistencias_use_case import obtener_asistencias_use_case
import math

# Crear blueprint
asistencias_bp = Blueprint('asistencias', __name__, url_prefix='/asistencias')


@asistencias_bp.route('/')
def index():
    """Ver asistencias guardadas en la base de datos con filtros y paginación"""
    
    # Obtener parámetros de query string
    num_trabajador = request.args.get('num_trabajador', type=int)
    checador = request.args.get('checador', type=str)
    fecha_inicio = request.args.get('fecha_inicio', type=str)
    fecha_fin = request.args.get('fecha_fin', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 50  # Registros por página
    
    # Usar caso de uso con filtros y paginación
    resultado, error = obtener_asistencias_use_case.ejecutar(
        num_trabajador=num_trabajador,
        checador=checador,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        page=page,
        per_page=per_page
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
        fecha_fin_filter=fecha_fin or ''
    )

