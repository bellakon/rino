"""
Rutas para el módulo de movimientos
"""
from flask import Blueprint, render_template, request, jsonify, send_file
from app.features.movimientos.models.movimiento_models import TipoMovimiento, CampoPersonalizado, Movimiento
from app.features.movimientos.services.crear_tipo_movimiento_use_case import crear_tipo_movimiento_use_case
from app.features.movimientos.services.listar_tipos_movimientos_use_case import listar_tipos_movimientos_use_case
from app.features.movimientos.services.obtener_tipo_movimiento_use_case import obtener_tipo_movimiento_use_case
from app.features.movimientos.services.editar_tipo_movimiento_use_case import editar_tipo_movimiento_use_case
from app.features.movimientos.services.eliminar_tipo_movimiento_use_case import eliminar_tipo_movimiento_use_case
from app.features.movimientos.services.crear_movimiento_use_case import crear_movimiento_use_case
from app.features.movimientos.services.crear_movimiento_masivo_use_case import crear_movimiento_masivo_use_case
from app.features.movimientos.services.listar_movimientos_use_case import listar_movimientos_use_case
from app.features.movimientos.services.obtener_movimiento_use_case import obtener_movimiento_use_case
from app.features.movimientos.services.editar_movimiento_use_case import editar_movimiento_use_case
from app.features.movimientos.services.eliminar_movimiento_use_case import eliminar_movimiento_use_case
from app.features.movimientos.services.generar_plantilla_pdf_use_case import generar_plantilla_pdf_use_case
from app.config.movimientos_config import LETRAS_MOVIMIENTOS
from datetime import datetime
import io
import json

movimientos_bp = Blueprint('movimientos', __name__, url_prefix='/movimientos', template_folder='../templates')


@movimientos_bp.route('/')
def index():
    """Vista principal del módulo de movimientos"""
    return render_template('movimientos/index.html', letras=LETRAS_MOVIMIENTOS)


# ==================== TIPOS DE MOVIMIENTOS ====================

@movimientos_bp.route('/tipos/listar', methods=['GET'])
def listar_tipos():
    """Lista tipos de movimientos"""
    nomenclatura = request.args.get('nomenclatura')
    nombre = request.args.get('nombre')
    categoria = request.args.get('categoria')
    letra = request.args.get('letra')
    activo = request.args.get('activo')
    
    activo_bool = None
    if activo and activo.lower() in ['true', '1']:
        activo_bool = True
    elif activo and activo.lower() in ['false', '0']:
        activo_bool = False
    
    tipos = listar_tipos_movimientos_use_case.ejecutar(
        nomenclatura=nomenclatura,
        nombre=nombre,
        categoria=categoria,
        letra=letra,
        activo=activo_bool
    )
    
    return jsonify([{
        'id': t.id,
        'nomenclatura': t.nomenclatura,
        'nombre': t.nombre,
        'descripcion': t.descripcion,
        'categoria': t.categoria,
        'letra': t.letra,
        'campos_personalizados': [c.to_dict() for c in t.campos_personalizados],
        'activo': t.activo,
        'created_at': t.created_at.isoformat() if t.created_at else None
    } for t in tipos])


@movimientos_bp.route('/tipos/crear', methods=['POST'])
def crear_tipo():
    """Crea un nuevo tipo de movimiento"""
    try:
        data = request.get_json()
        
        campos = []
        if data.get('campos_personalizados'):
            campos_data = data['campos_personalizados']
            if isinstance(campos_data, str):
                campos_data = json.loads(campos_data)
            campos = [CampoPersonalizado.from_dict(c) for c in campos_data]
        
        tipo = TipoMovimiento(
            nomenclatura=data['nomenclatura'],
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            categoria=data['categoria'],
            letra=data['letra'],
            campos_personalizados=campos,
            activo=data.get('activo', True)
        )
        
        tipo_id, error = crear_tipo_movimiento_use_case.ejecutar(tipo)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'success': True, 'id': tipo_id}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@movimientos_bp.route('/tipos/obtener/<int:tipo_id>', methods=['GET'])
def obtener_tipo(tipo_id):
    """Obtiene un tipo de movimiento por ID"""
    tipo = obtener_tipo_movimiento_use_case.ejecutar(tipo_id)
    
    if not tipo:
        return jsonify({'error': 'Tipo de movimiento no encontrado'}), 404
    
    return jsonify({
        'id': tipo.id,
        'nomenclatura': tipo.nomenclatura,
        'nombre': tipo.nombre,
        'descripcion': tipo.descripcion,
        'categoria': tipo.categoria,
        'letra': tipo.letra,
        'campos_personalizados': [c.to_dict() for c in tipo.campos_personalizados],
        'activo': tipo.activo
    })


@movimientos_bp.route('/tipos/editar/<int:tipo_id>', methods=['POST'])
def editar_tipo(tipo_id):
    """Edita un tipo de movimiento"""
    try:
        data = request.get_json()
        
        campos = []
        if data.get('campos_personalizados'):
            campos_data = data['campos_personalizados']
            if isinstance(campos_data, str):
                campos_data = json.loads(campos_data)
            campos = [CampoPersonalizado.from_dict(c) for c in campos_data]
        
        tipo = TipoMovimiento(
            nomenclatura=data['nomenclatura'],
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            categoria=data['categoria'],
            letra=data['letra'],
            campos_personalizados=campos,
            activo=data.get('activo', True)
        )
        
        success, error = editar_tipo_movimiento_use_case.ejecutar(tipo_id, tipo)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@movimientos_bp.route('/tipos/eliminar/<int:tipo_id>', methods=['POST'])
def eliminar_tipo(tipo_id):
    """Elimina un tipo de movimiento"""
    success, mensaje = eliminar_tipo_movimiento_use_case.ejecutar(tipo_id)
    
    if not success:
        return jsonify({'error': mensaje}), 400
    
    return jsonify({
        'success': True,
        'mensaje': mensaje if mensaje else 'Tipo de movimiento eliminado exitosamente'
    })


@movimientos_bp.route('/tipos/importar', methods=['POST'])
def importar_tipos_csv():
    """Importa tipos desde CSV"""
    # TODO: Implementar caso de uso para importar CSV
    return jsonify({'error': 'Funcionalidad de importación CSV pendiente de implementar'}), 501


@movimientos_bp.route('/tipos/plantilla-csv', methods=['GET'])
def descargar_plantilla_tipos_csv():
    """Descarga plantilla CSV"""
    # TODO: Implementar generación de plantilla CSV
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['id', 'nomenclatura', 'nombre', 'descripcion', 'categoria', 'letra', 'campos_personalizados', 'activo'])
    writer.writerow(['', 'COM999', 'Comisión Ejemplo', 'Descripción', 'Comisión', 'A', '[{"nombre":"archivo_pdf","tipo":"file","requerido":true,"label":"Documento PDF"}]', '1'])
    writer.writerow(['', 'PER999', 'Permiso Ejemplo', 'Permiso de ejemplo', 'Permiso', 'B', '', '1'])
    
    csv_content = output.getvalue()
    
    buffer = io.BytesIO()
    buffer.write(csv_content.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name='plantilla_tipos_movimientos.csv'
    )


# ==================== MOVIMIENTOS ====================

@movimientos_bp.route('/movimientos/listar', methods=['GET'])
def listar_movs():
    """Lista movimientos"""
    num_trabajador = request.args.get('num_trabajador', type=int)
    tipo_movimiento_id = request.args.get('tipo_movimiento_id', type=int)
    fecha_inicio_str = request.args.get('fecha_inicio')
    fecha_fin_str = request.args.get('fecha_fin')
    nombre_trabajador = request.args.get('nombre_trabajador')
    
    fecha_inicio = None
    fecha_fin = None
    
    if fecha_inicio_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    movimientos = listar_movimientos_use_case.ejecutar(
        num_trabajador=num_trabajador,
        tipo_movimiento_id=tipo_movimiento_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        nombre_trabajador=nombre_trabajador
    )
    
    return jsonify([{
        'id': m.id,
        'num_trabajador': m.num_trabajador,
        'trabajador_nombre': m.trabajador_nombre,
        'tipo_movimiento_id': m.tipo_movimiento_id,
        'tipo_nomenclatura': m.tipo_nomenclatura,
        'tipo_nombre': m.tipo_nombre,
        'fecha_inicio': m.fecha_inicio.isoformat(),
        'fecha_fin': m.fecha_fin.isoformat(),
        'observaciones': m.observaciones,
        'datos_personalizados': m.datos_personalizados,
        'usuario_registro': m.usuario_registro,
        'created_at': m.created_at.isoformat() if m.created_at else None
    } for m in movimientos])


@movimientos_bp.route('/movimientos/crear', methods=['POST'])
def crear_mov():
    """Crea un nuevo movimiento"""
    try:
        data = request.get_json()
        
        fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date()
        
        datos_personalizados = {}
        if data.get('datos_personalizados'):
            datos_personalizados = data['datos_personalizados']
            if isinstance(datos_personalizados, str):
                datos_personalizados = json.loads(datos_personalizados)
        
        movimiento = Movimiento(
            num_trabajador=int(data['num_trabajador']),
            tipo_movimiento_id=int(data['tipo_movimiento_id']),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            observaciones=data.get('observaciones'),
            datos_personalizados=datos_personalizados,
            usuario_registro=data.get('usuario_registro', 'sistema')
        )
        
        movimiento_id, error = crear_movimiento_use_case.ejecutar(movimiento)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'success': True, 'id': movimiento_id}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@movimientos_bp.route('/movimientos/crear-masivo', methods=['POST'])
def crear_mov_masivo():
    """Crea el mismo movimiento para múltiples trabajadores"""
    try:
        data = request.get_json()
        
        # Validar que nums_trabajadores sea una lista
        nums_trabajadores = data.get('nums_trabajadores', [])
        if isinstance(nums_trabajadores, str):
            nums_trabajadores = json.loads(nums_trabajadores)
        
        if not isinstance(nums_trabajadores, list):
            return jsonify({'error': 'nums_trabajadores debe ser una lista'}), 400
        
        # Convertir a enteros
        try:
            nums_trabajadores = [int(n) for n in nums_trabajadores]
        except (ValueError, TypeError):
            return jsonify({'error': 'Todos los números de trabajador deben ser válidos'}), 400
        
        fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date()
        
        datos_personalizados = {}
        if data.get('datos_personalizados'):
            datos_personalizados = data['datos_personalizados']
            if isinstance(datos_personalizados, str):
                datos_personalizados = json.loads(datos_personalizados)
        
        ids_creados, error = crear_movimiento_masivo_use_case.ejecutar(
            nums_trabajadores=nums_trabajadores,
            tipo_movimiento_id=int(data['tipo_movimiento_id']),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            observaciones=data.get('observaciones'),
            datos_personalizados=datos_personalizados,
            usuario_registro=data.get('usuario_registro', 'sistema')
        )
        
        if error and not ids_creados:
            return jsonify({'error': error}), 400
        
        response = {
            'success': True,
            'ids': ids_creados,
            'total_creados': len(ids_creados) if ids_creados else 0
        }
        
        if error:
            response['warning'] = error
        
        return jsonify(response), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@movimientos_bp.route('/movimientos/obtener/<int:movimiento_id>', methods=['GET'])
def obtener_mov(movimiento_id):
    """Obtiene un movimiento por ID"""
    movimiento = obtener_movimiento_use_case.ejecutar(movimiento_id)
    
    if not movimiento:
        return jsonify({'error': 'Movimiento no encontrado'}), 404
    
    return jsonify({
        'id': movimiento.id,
        'num_trabajador': movimiento.num_trabajador,
        'trabajador_nombre': movimiento.trabajador_nombre,
        'tipo_movimiento_id': movimiento.tipo_movimiento_id,
        'tipo_nomenclatura': movimiento.tipo_nomenclatura,
        'tipo_nombre': movimiento.tipo_nombre,
        'fecha_inicio': movimiento.fecha_inicio.isoformat(),
        'fecha_fin': movimiento.fecha_fin.isoformat(),
        'observaciones': movimiento.observaciones,
        'datos_personalizados': movimiento.datos_personalizados,
        'usuario_registro': movimiento.usuario_registro
    })


@movimientos_bp.route('/movimientos/editar/<int:movimiento_id>', methods=['POST'])
def editar_mov(movimiento_id):
    """Edita un movimiento"""
    try:
        data = request.get_json()
        
        fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date()
        
        datos_personalizados = {}
        if data.get('datos_personalizados'):
            datos_personalizados = data['datos_personalizados']
            if isinstance(datos_personalizados, str):
                datos_personalizados = json.loads(datos_personalizados)
        
        movimiento = Movimiento(
            num_trabajador=int(data['num_trabajador']),
            tipo_movimiento_id=int(data['tipo_movimiento_id']),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            observaciones=data.get('observaciones'),
            datos_personalizados=datos_personalizados
        )
        
        success, error = editar_movimiento_use_case.ejecutar(movimiento_id, movimiento)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@movimientos_bp.route('/movimientos/eliminar/<int:movimiento_id>', methods=['POST'])
def eliminar_mov(movimiento_id):
    """Elimina un movimiento"""
    success, error = eliminar_movimiento_use_case.ejecutar(movimiento_id)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({'success': True})


@movimientos_bp.route('/movimientos/importar', methods=['POST'])
def importar_movimientos_csv():
    """Importa movimientos desde CSV"""
    # TODO: Implementar caso de uso para importar movimientos CSV
    return jsonify({'error': 'Funcionalidad de importación CSV pendiente de implementar'}), 501


@movimientos_bp.route('/movimientos/plantilla-csv', methods=['GET'])
def descargar_plantilla_movimientos_csv():
    """Descarga plantilla CSV"""
    # TODO: Implementar generación de plantilla CSV para movimientos
    import csv
    import io
    from datetime import date
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    hoy = date.today()
    writer.writerow(['id', 'num_trabajador', 'tipo_movimiento_id', 'fecha_inicio', 'fecha_fin', 'observaciones', 'datos_personalizados'])
    writer.writerow(['', '1001', '1', hoy, hoy, 'Ejemplo de movimiento', '{}'])
    
    csv_content = output.getvalue()
    
    buffer = io.BytesIO()
    buffer.write(csv_content.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name='plantilla_movimientos.csv'
    )


@movimientos_bp.route('/plantilla/pdf', methods=['GET'])
def descargar_plantilla_pdf():
    """Descarga PDF con códigos de movimientos y resumen del sistema"""
    buffer, error = generar_plantilla_pdf_use_case.ejecutar()
    
    if error:
        return jsonify({'error': error}), 500
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'TecnoTime_Codigos_Movimientos_{datetime.now().strftime("%Y%m%d")}.pdf'
    )
