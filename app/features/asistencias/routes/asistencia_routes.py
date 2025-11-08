"""
Rutas para el feature de asistencias
Responsabilidad: mostrar asistencias de la base de datos
"""
from flask import Blueprint, render_template, flash
from app.features.asistencias.services.obtener_asistencias_use_case import obtener_asistencias_use_case

# Crear blueprint
asistencias_bp = Blueprint('asistencias', __name__, url_prefix='/asistencias')


@asistencias_bp.route('/')
def index():
    """Ver asistencias guardadas en la base de datos usando modelos"""
    
    # Usar caso de uso que retorna lista de objetos Asistencia
    asistencias, error = obtener_asistencias_use_case.ejecutar()
    
    if error:
        flash(f'Error al consultar: {error}', 'error')
        asistencias = []
    
    return render_template(
        'asistencias/index.html',
        asistencias=asistencias
    )

