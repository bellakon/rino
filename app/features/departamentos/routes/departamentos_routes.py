"""
Rutas: Departamentos
Endpoints para gestión de departamentos
"""
from flask import Blueprint, render_template, request, jsonify, send_file
import io
import csv
from app.features.departamentos.services.crear_departamento_use_case import crear_departamento_use_case
from app.features.departamentos.services.listar_departamentos_use_case import listar_departamentos_use_case
from app.features.departamentos.services.actualizar_departamento_use_case import actualizar_departamento_use_case
from app.features.departamentos.services.eliminar_departamento_use_case import eliminar_departamento_use_case
from app.features.departamentos.services.importar_departamentos_csv_use_case import importar_departamentos_csv_use_case
from app.features.departamentos.models.departamento import Departamento


# Crear blueprint
departamentos_bp = Blueprint(
    'departamentos',
    __name__,
    url_prefix='/departamentos',
    template_folder='../templates'
)


@departamentos_bp.route('/')
def index():
    """Página principal de departamentos"""
    return render_template('departamentos/index.html')


@departamentos_bp.route('/listar')
def listar():
    """Lista todos los departamentos"""
    activo = request.args.get('activo')
    buscar = request.args.get('buscar')
    
    # Convertir activo a boolean si viene
    if activo is not None:
        activo = activo.lower() in ['true', '1', 'si']
    
    departamentos, error = listar_departamentos_use_case.ejecutar(activo, buscar)
    
    if error:
        return jsonify({'error': error}), 500
    
    return jsonify({'departamentos': departamentos})


@departamentos_bp.route('/crear', methods=['POST'])
def crear():
    """Crea un nuevo departamento"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('num_departamento') or not data.get('nombre'):
            return jsonify({'error': 'num_departamento y nombre son obligatorios'}), 400
        
        # Crear objeto Departamento
        departamento = Departamento(
            num_departamento=int(data['num_departamento']),
            nombre=data['nombre'],
            nomenclatura=data.get('nomenclatura', ''),
            activo=data.get('activo', True)
        )
        
        id_insertado, error = crear_departamento_use_case.ejecutar(departamento)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'success': True,
            'id': id_insertado,
            'mensaje': 'Departamento creado exitosamente'
        })
        
    except ValueError:
        return jsonify({'error': 'num_departamento debe ser un número'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@departamentos_bp.route('/editar/<int:id>', methods=['PUT'])
def editar(id):
    """Edita un departamento existente"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('num_departamento') or not data.get('nombre'):
            return jsonify({'error': 'num_departamento y nombre son obligatorios'}), 400
        
        # Crear objeto Departamento
        departamento = Departamento(
            num_departamento=int(data['num_departamento']),
            nombre=data['nombre'],
            nomenclatura=data.get('nomenclatura', ''),
            activo=data.get('activo', True)
        )
        
        success, error = actualizar_departamento_use_case.ejecutar(id, departamento)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'success': True,
            'mensaje': 'Departamento actualizado exitosamente'
        })
        
    except ValueError:
        return jsonify({'error': 'num_departamento debe ser un número'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@departamentos_bp.route('/eliminar/<int:id>', methods=['DELETE'])
def eliminar(id):
    """Elimina un departamento"""
    try:
        success, error = eliminar_departamento_use_case.ejecutar(id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'success': True,
            'mensaje': 'Departamento eliminado exitosamente'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@departamentos_bp.route('/importar-csv', methods=['POST'])
def importar_csv():
    """Importa departamentos desde CSV"""
    try:
        if 'archivo' not in request.files:
            return jsonify({'error': 'No se proporcionó archivo'}), 400
        
        archivo = request.files['archivo']
        
        if archivo.filename == '':
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        if not archivo.filename.endswith('.csv'):
            return jsonify({'error': 'El archivo debe ser CSV'}), 400
        
        resultado, error = importar_departamentos_csv_use_case.ejecutar(archivo)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'success': True,
            'resultado': resultado,
            'mensaje': f'Importación completada. {resultado["insertados"]} insertados, {resultado["duplicados"]} duplicados, {resultado["error_count"]} errores'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@departamentos_bp.route('/descargar-plantilla')
def descargar_plantilla():
    """Descarga plantilla CSV para importar departamentos"""
    # Crear CSV en memoria
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(['num_departamento', 'nombre', 'nomenclatura', 'activo'])
    
    # Filas de ejemplo
    writer.writerow(['1', 'DIRECCIÓN GENERAL', 'DG', '1'])
    writer.writerow(['2', 'SUBDIRECCIÓN ADMINISTRATIVA', 'SA', '1'])
    writer.writerow(['3', 'RECURSOS HUMANOS', 'RH', '1'])
    writer.writerow(['4', 'FINANZAS', 'FIN', '1'])
    writer.writerow(['5', 'SISTEMAS', 'SIS', '1'])
    
    # Convertir a bytes
    output.seek(0)
    bytes_output = io.BytesIO(output.getvalue().encode('utf-8'))
    bytes_output.seek(0)
    
    return send_file(
        bytes_output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='plantilla_departamentos.csv'
    )
