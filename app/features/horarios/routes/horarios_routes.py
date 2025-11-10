"""
Rutas: Horarios
Endpoints para gestión de horarios y asignaciones
"""
from flask import Blueprint, render_template, request, jsonify, send_file
import io
import csv
from app.features.horarios.services.crear_plantilla_horario_use_case import crear_plantilla_horario_use_case
from app.features.horarios.services.listar_plantillas_horarios_use_case import listar_plantillas_horarios_use_case
from app.features.horarios.services.eliminar_plantilla_horario_use_case import eliminar_plantilla_horario_use_case
from app.features.horarios.services.editar_plantilla_horario_use_case import editar_plantilla_horario_use_case
from app.features.horarios.services.obtener_plantilla_horario_use_case import obtener_plantilla_horario_use_case
from app.features.horarios.services.asignar_horario_trabajador_use_case import asignar_horario_trabajador_use_case
from app.features.horarios.services.listar_horarios_trabajadores_use_case import listar_horarios_trabajadores_use_case
from app.features.horarios.services.obtener_asignacion_use_case import obtener_asignacion_use_case
from app.features.horarios.services.editar_asignacion_use_case import editar_asignacion_use_case
from app.features.horarios.services.eliminar_asignacion_use_case import eliminar_asignacion_use_case
from app.features.horarios.services.importar_horarios_csv_use_case import importar_horarios_csv_use_case
from app.features.horarios.models.plantilla_horario import PlantillaHorario
from app.features.horarios.models.horario_trabajador import HorarioTrabajador
from app.config.semestres import obtener_semestres


# Crear blueprint
horarios_bp = Blueprint(
    'horarios',
    __name__,
    url_prefix='/horarios',
    template_folder='../templates'
)


@horarios_bp.route('/')
def index():
    """Página principal de horarios"""
    semestres = obtener_semestres()
    return render_template('horarios/index.html', semestres=semestres)


@horarios_bp.route('/plantillas/listar')
def listar_plantillas():
    """Lista todas las plantillas de horarios"""
    activo = request.args.get('activo')
    buscar = request.args.get('buscar')
    
    if activo is not None:
        activo = activo.lower() in ['true', '1', 'si']
    
    plantillas, error = listar_plantillas_horarios_use_case.ejecutar(activo, buscar)
    
    if error:
        return jsonify({'error': error}), 500
    
    # Convertir TIME a string para JSON
    for p in plantillas:
        for key, value in p.items():
            if value is not None and 'entrada' in key or 'salida' in key:
                p[key] = str(value) if value else None
    
    return jsonify({'plantillas': plantillas})


@horarios_bp.route('/plantillas/crear', methods=['POST'])
def crear_plantilla():
    """Crea una nueva plantilla de horario"""
    try:
        data = request.get_json()
        
        plantilla = PlantillaHorario(
            nombre_horario=data['nombre_horario'],
            descripcion_horario=data.get('descripcion_horario', ''),
            lunes_entrada_1=data.get('lunes_entrada_1'),
            lunes_salida_1=data.get('lunes_salida_1'),
            lunes_entrada_2=data.get('lunes_entrada_2'),
            lunes_salida_2=data.get('lunes_salida_2'),
            martes_entrada_1=data.get('martes_entrada_1'),
            martes_salida_1=data.get('martes_salida_1'),
            martes_entrada_2=data.get('martes_entrada_2'),
            martes_salida_2=data.get('martes_salida_2'),
            miercoles_entrada_1=data.get('miercoles_entrada_1'),
            miercoles_salida_1=data.get('miercoles_salida_1'),
            miercoles_entrada_2=data.get('miercoles_entrada_2'),
            miercoles_salida_2=data.get('miercoles_salida_2'),
            jueves_entrada_1=data.get('jueves_entrada_1'),
            jueves_salida_1=data.get('jueves_salida_1'),
            jueves_entrada_2=data.get('jueves_entrada_2'),
            jueves_salida_2=data.get('jueves_salida_2'),
            viernes_entrada_1=data.get('viernes_entrada_1'),
            viernes_salida_1=data.get('viernes_salida_1'),
            viernes_entrada_2=data.get('viernes_entrada_2'),
            viernes_salida_2=data.get('viernes_salida_2'),
            sabado_entrada_1=data.get('sabado_entrada_1'),
            sabado_salida_1=data.get('sabado_salida_1'),
            sabado_entrada_2=data.get('sabado_entrada_2'),
            sabado_salida_2=data.get('sabado_salida_2'),
            domingo_entrada_1=data.get('domingo_entrada_1'),
            domingo_salida_1=data.get('domingo_salida_1'),
            domingo_entrada_2=data.get('domingo_entrada_2'),
            domingo_salida_2=data.get('domingo_salida_2'),
            activo=data.get('activo', True)
        )
        
        id_insertado, error = crear_plantilla_horario_use_case.ejecutar(plantilla)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'success': True,
            'id': id_insertado,
            'mensaje': 'Plantilla creada exitosamente'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@horarios_bp.route('/plantillas/eliminar/<int:id>', methods=['POST'])
def eliminar_plantilla(id):
    """Elimina una plantilla de horario"""
    success, error = eliminar_plantilla_horario_use_case.ejecutar(id)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'success': True,
        'mensaje': 'Plantilla eliminada exitosamente'
    })


@horarios_bp.route('/plantillas/obtener/<int:id>')
def obtener_plantilla(id):
    """Obtiene una plantilla de horario por ID"""
    plantilla, error = obtener_plantilla_horario_use_case.ejecutar(id)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify({'plantilla': plantilla})


@horarios_bp.route('/plantillas/editar/<int:id>', methods=['POST'])
def editar_plantilla(id):
    """Edita una plantilla de horario"""
    try:
        data = request.get_json()
        
        plantilla = PlantillaHorario(
            nombre_horario=data['nombre_horario'],
            descripcion_horario=data.get('descripcion_horario', ''),
            lunes_entrada_1=data.get('lunes_entrada_1'),
            lunes_salida_1=data.get('lunes_salida_1'),
            lunes_entrada_2=data.get('lunes_entrada_2'),
            lunes_salida_2=data.get('lunes_salida_2'),
            martes_entrada_1=data.get('martes_entrada_1'),
            martes_salida_1=data.get('martes_salida_1'),
            martes_entrada_2=data.get('martes_entrada_2'),
            martes_salida_2=data.get('martes_salida_2'),
            miercoles_entrada_1=data.get('miercoles_entrada_1'),
            miercoles_salida_1=data.get('miercoles_salida_1'),
            miercoles_entrada_2=data.get('miercoles_entrada_2'),
            miercoles_salida_2=data.get('miercoles_salida_2'),
            jueves_entrada_1=data.get('jueves_entrada_1'),
            jueves_salida_1=data.get('jueves_salida_1'),
            jueves_entrada_2=data.get('jueves_entrada_2'),
            jueves_salida_2=data.get('jueves_salida_2'),
            viernes_entrada_1=data.get('viernes_entrada_1'),
            viernes_salida_1=data.get('viernes_salida_1'),
            viernes_entrada_2=data.get('viernes_entrada_2'),
            viernes_salida_2=data.get('viernes_salida_2'),
            sabado_entrada_1=data.get('sabado_entrada_1'),
            sabado_salida_1=data.get('sabado_salida_1'),
            sabado_entrada_2=data.get('sabado_entrada_2'),
            sabado_salida_2=data.get('sabado_salida_2'),
            domingo_entrada_1=data.get('domingo_entrada_1'),
            domingo_salida_1=data.get('domingo_salida_1'),
            domingo_entrada_2=data.get('domingo_entrada_2'),
            domingo_salida_2=data.get('domingo_salida_2'),
            activo=data.get('activo', True)
        )
        
        success, error = editar_plantilla_horario_use_case.ejecutar(id, plantilla)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'success': True,
            'mensaje': 'Plantilla actualizada exitosamente'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@horarios_bp.route('/asignaciones/listar')
def listar_asignaciones():
    """Lista asignaciones de horarios"""
    semestre = request.args.get('semestre')
    num_trabajador = request.args.get('num_trabajador', type=int)
    estado = request.args.get('estado')
    
    horarios, error = listar_horarios_trabajadores_use_case.ejecutar(semestre, num_trabajador, estado)
    
    if error:
        return jsonify({'error': error}), 500
    
    return jsonify({'horarios': horarios})


@horarios_bp.route('/asignaciones/crear', methods=['POST'])
def crear_asignacion():
    """Asigna un horario a un trabajador"""
    try:
        data = request.get_json()
        
        horario = HorarioTrabajador(
            num_trabajador=int(data['num_trabajador']),
            plantilla_horario_id=int(data['plantilla_horario_id']),
            fecha_inicio_asignacion=data['fecha_inicio_asignacion'],
            fecha_fin_asignacion=data.get('fecha_fin_asignacion'),
            semestre=data['semestre'],
            estado_asignacion=data.get('estado_asignacion', 'activo'),
            activo_asignacion=data.get('activo_asignacion', True)
        )
        
        id_insertado, error = asignar_horario_trabajador_use_case.ejecutar(horario)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'success': True,
            'id': id_insertado,
            'mensaje': 'Horario asignado exitosamente'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@horarios_bp.route('/asignaciones/obtener/<int:id>')
def obtener_asignacion(id):
    """Obtiene una asignación por ID"""
    asignacion, error = obtener_asignacion_use_case.ejecutar(id)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify(asignacion)


@horarios_bp.route('/asignaciones/editar/<int:id>', methods=['POST'])
def editar_asignacion(id):
    """Edita una asignación de horario"""
    try:
        data = request.get_json()
        
        success, error = editar_asignacion_use_case.ejecutar(
            id_asignacion=id,
            fecha_inicio=data['fecha_inicio_asignacion'],
            fecha_fin=data['fecha_fin_asignacion'],
            semestre=data['semestre'],
            estado=data.get('estado_asignacion', 'activo')
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'success': True,
            'mensaje': 'Asignación actualizada exitosamente'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@horarios_bp.route('/asignaciones/eliminar/<int:id>', methods=['POST'])
def eliminar_asignacion(id):
    """Elimina una asignación de horario"""
    success, error = eliminar_asignacion_use_case.ejecutar(id)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'success': True,
        'mensaje': 'Asignación eliminada exitosamente'
    })


@horarios_bp.route('/importar', methods=['POST'])
def importar_horarios():
    """Importa horarios desde CSV"""
    try:
        if 'archivo' not in request.files:
            return jsonify({'error': 'No se proporcionó archivo'}), 400
        
        archivo = request.files['archivo']
        
        if archivo.filename == '':
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        if not archivo.filename.endswith('.csv'):
            return jsonify({'error': 'El archivo debe ser CSV'}), 400
        
        resultados, error = importar_horarios_csv_use_case.ejecutar(archivo)
        
        if error:
            return jsonify({'error': error}), 500
        
        return jsonify({
            'success': True,
            'resultados': resultados
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@horarios_bp.route('/descargar-plantilla-csv')
def descargar_plantilla_csv():
    """Descarga CSV con asignaciones existentes"""
    try:
        # Obtener todas las asignaciones activas
        query = """
            SELECT 
                ht.num_trabajador,
                ph.nombre_horario,
                ph.descripcion_horario,
                ph.lunes_entrada_1, ph.lunes_salida_1, ph.lunes_entrada_2, ph.lunes_salida_2,
                ph.martes_entrada_1, ph.martes_salida_1, ph.martes_entrada_2, ph.martes_salida_2,
                ph.miercoles_entrada_1, ph.miercoles_salida_1, ph.miercoles_entrada_2, ph.miercoles_salida_2,
                ph.jueves_entrada_1, ph.jueves_salida_1, ph.jueves_entrada_2, ph.jueves_salida_2,
                ph.viernes_entrada_1, ph.viernes_salida_1, ph.viernes_entrada_2, ph.viernes_salida_2,
                ph.sabado_entrada_1, ph.sabado_salida_1, ph.sabado_entrada_2, ph.sabado_salida_2,
                ph.domingo_entrada_1, ph.domingo_salida_1, ph.domingo_entrada_2, ph.domingo_salida_2,
                ht.fecha_inicio_asignacion,
                ht.fecha_fin_asignacion,
                ht.semestre
            FROM horarios_trabajadores ht
            INNER JOIN plantillas_horarios ph ON ht.plantilla_horario_id = ph.id
            WHERE ht.activo_asignacion = 1
            ORDER BY ht.num_trabajador, ht.fecha_inicio_asignacion
        """
        
        from app.core.database.query_executor import QueryExecutor
        from app.core.database.connection import db_connection
        
        query_executor = QueryExecutor(db_connection)
        asignaciones, error = query_executor.ejecutar(query)
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Encabezados
        writer.writerow([
            'num_trabajador', 'nombre_horario', 'descripcion_horario',
            'lunes_entrada_1', 'lunes_salida_1', 'lunes_entrada_2', 'lunes_salida_2',
            'martes_entrada_1', 'martes_salida_1', 'martes_entrada_2', 'martes_salida_2',
            'miercoles_entrada_1', 'miercoles_salida_1', 'miercoles_entrada_2', 'miercoles_salida_2',
            'jueves_entrada_1', 'jueves_salida_1', 'jueves_entrada_2', 'jueves_salida_2',
            'viernes_entrada_1', 'viernes_salida_1', 'viernes_entrada_2', 'viernes_salida_2',
            'sabado_entrada_1', 'sabado_salida_1', 'sabado_entrada_2', 'sabado_salida_2',
            'domingo_entrada_1', 'domingo_salida_1', 'domingo_entrada_2', 'domingo_salida_2',
            'fecha_inicio_asignacion', 'fecha_fin_asignacion', 'semestre'
        ])
        
        # Si hay asignaciones, exportarlas
        if asignaciones:
            for asig in asignaciones:
                writer.writerow([
                    asig['num_trabajador'],
                    asig['nombre_horario'],
                    asig['descripcion_horario'] or '',
                    str(asig['lunes_entrada_1']) if asig['lunes_entrada_1'] else '',
                    str(asig['lunes_salida_1']) if asig['lunes_salida_1'] else '',
                    str(asig['lunes_entrada_2']) if asig['lunes_entrada_2'] else '',
                    str(asig['lunes_salida_2']) if asig['lunes_salida_2'] else '',
                    str(asig['martes_entrada_1']) if asig['martes_entrada_1'] else '',
                    str(asig['martes_salida_1']) if asig['martes_salida_1'] else '',
                    str(asig['martes_entrada_2']) if asig['martes_entrada_2'] else '',
                    str(asig['martes_salida_2']) if asig['martes_salida_2'] else '',
                    str(asig['miercoles_entrada_1']) if asig['miercoles_entrada_1'] else '',
                    str(asig['miercoles_salida_1']) if asig['miercoles_salida_1'] else '',
                    str(asig['miercoles_entrada_2']) if asig['miercoles_entrada_2'] else '',
                    str(asig['miercoles_salida_2']) if asig['miercoles_salida_2'] else '',
                    str(asig['jueves_entrada_1']) if asig['jueves_entrada_1'] else '',
                    str(asig['jueves_salida_1']) if asig['jueves_salida_1'] else '',
                    str(asig['jueves_entrada_2']) if asig['jueves_entrada_2'] else '',
                    str(asig['jueves_salida_2']) if asig['jueves_salida_2'] else '',
                    str(asig['viernes_entrada_1']) if asig['viernes_entrada_1'] else '',
                    str(asig['viernes_salida_1']) if asig['viernes_salida_1'] else '',
                    str(asig['viernes_entrada_2']) if asig['viernes_entrada_2'] else '',
                    str(asig['viernes_salida_2']) if asig['viernes_salida_2'] else '',
                    str(asig['sabado_entrada_1']) if asig['sabado_entrada_1'] else '',
                    str(asig['sabado_salida_1']) if asig['sabado_salida_1'] else '',
                    str(asig['sabado_entrada_2']) if asig['sabado_entrada_2'] else '',
                    str(asig['sabado_salida_2']) if asig['sabado_salida_2'] else '',
                    str(asig['domingo_entrada_1']) if asig['domingo_entrada_1'] else '',
                    str(asig['domingo_salida_1']) if asig['domingo_salida_1'] else '',
                    str(asig['domingo_entrada_2']) if asig['domingo_entrada_2'] else '',
                    str(asig['domingo_salida_2']) if asig['domingo_salida_2'] else '',
                    str(asig['fecha_inicio_asignacion']),
                    str(asig['fecha_fin_asignacion']) if asig['fecha_fin_asignacion'] else '',
                    asig['semestre']
                ])
        else:
            # Si no hay datos, agregar ejemplo
            writer.writerow([
                '1', 'Horario Administrativo', 'Lunes a Viernes 9-17',
                '09:00', '17:00', '', '',
                '09:00', '17:00', '', '',
                '09:00', '17:00', '', '',
                '09:00', '17:00', '', '',
                '09:00', '17:00', '', '',
                '', '', '', '',
                '', '', '', '',
                '2024-08-01', '2024-12-31', 'AGOSTO_DICIEMBRE_2024'
            ])
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='horarios_asignados.csv'
        )
        
    except Exception as e:
        # Si hay error, retornar plantilla vacía
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'num_trabajador', 'nombre_horario', 'descripcion_horario',
            'lunes_entrada_1', 'lunes_salida_1', 'lunes_entrada_2', 'lunes_salida_2',
            'martes_entrada_1', 'martes_salida_1', 'martes_entrada_2', 'martes_salida_2',
            'miercoles_entrada_1', 'miercoles_salida_1', 'miercoles_entrada_2', 'miercoles_salida_2',
            'jueves_entrada_1', 'jueves_salida_1', 'jueves_entrada_2', 'jueves_salida_2',
            'viernes_entrada_1', 'viernes_salida_1', 'viernes_entrada_2', 'viernes_salida_2',
            'sabado_entrada_1', 'sabado_salida_1', 'sabado_entrada_2', 'sabado_salida_2',
            'domingo_entrada_1', 'domingo_salida_1', 'domingo_entrada_2', 'domingo_salida_2',
            'fecha_inicio_asignacion', 'fecha_fin_asignacion', 'semestre'
        ])
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='plantilla_horarios.csv'
        )

