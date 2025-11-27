"""
Rutas para el feature de trabajadores
Responsabilidad: CRUD de trabajadores
"""
from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for
from app.features.trabajadores.services.obtener_trabajadores_use_case import obtener_trabajadores_use_case
from app.features.trabajadores.services.importar_trabajadores_use_case import importar_trabajadores_use_case
from app.features.trabajadores.services.crear_trabajador_use_case import crear_trabajador_use_case
from app.features.trabajadores.services.actualizar_trabajador_use_case import actualizar_trabajador_use_case
from app.features.trabajadores.services.eliminar_trabajador_use_case import eliminar_trabajador_use_case
from app.features.trabajadores.services.cambiar_departamento_trabajador_use_case import cambiar_departamento_trabajador_use_case
from app.features.checadores.services.consultar_checadores_trabajador_use_case import consultar_checadores_trabajador_use_case
from app.core.database.query_executor import query_executor
import math

# Crear blueprint
trabajadores_bp = Blueprint('trabajadores', __name__, url_prefix='/trabajadores')


@trabajadores_bp.route('/')
def index():
    """Ver trabajadores con filtros y paginación"""
    
    # Obtener parámetros de query string
    num_trabajador = request.args.get('num_trabajador', type=int)
    tipoPlaza = request.args.get('tipoPlaza', type=str)
    departamento_id = request.args.get('departamento_id', type=int)
    orden_por = request.args.get('orden_por', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 50  # Registros por página
    
    # Usar caso de uso con filtros y paginación
    resultado, error = obtener_trabajadores_use_case.ejecutar(
        num_trabajador=num_trabajador,
        tipoPlaza=tipoPlaza,
        departamento_id=departamento_id,
        orden_por=orden_por,
        page=page,
        per_page=per_page
    )
    
    if error:
        flash(f'Error al consultar: {error}', 'error')
        resultado = {'trabajadores': [], 'total': 0, 'page': 1, 'per_page': per_page}
    
    # Calcular información de paginación
    total_pages = math.ceil(resultado['total'] / resultado['per_page']) if resultado['total'] > 0 else 1
    has_prev = resultado['page'] > 1
    has_next = resultado['page'] < total_pages
    
    # Obtener lista de departamentos para el filtro
    query_departamentos = """
        SELECT id, nombre 
        FROM departamentos 
        WHERE activo = 1 
        ORDER BY nombre ASC
    """
    departamentos, _ = query_executor.ejecutar(query_departamentos)
    
    return render_template(
        'trabajadores/index.html',
        trabajadores=resultado['trabajadores'],
        total=resultado['total'],
        page=resultado['page'],
        per_page=resultado['per_page'],
        total_pages=total_pages,
        has_prev=has_prev,
        has_next=has_next,
        num_trabajador_filter=num_trabajador,
        tipoPlaza_filter=tipoPlaza or '',
        departamento_id_filter=departamento_id,
        orden_por_filter=orden_por or '',
        departamentos=departamentos or []
    )


@trabajadores_bp.route('/importar', methods=['POST'])
def importar():
    """Importar trabajadores desde archivo CSV"""
    
    if 'archivo_csv' not in request.files:
        flash('No se seleccionó ningún archivo', 'error')
        return redirect(url_for('trabajadores.index'))
    
    archivo = request.files['archivo_csv']
    
    if archivo.filename == '':
        flash('No se seleccionó ningún archivo', 'error')
        return redirect(url_for('trabajadores.index'))
    
    if not archivo.filename.endswith('.csv'):
        flash('El archivo debe ser un CSV', 'error')
        return redirect(url_for('trabajadores.index'))
    
    # Ejecutar importación
    resultado, error = importar_trabajadores_use_case.ejecutar(archivo)
    
    if error:
        flash(f'Error al importar: {error}', 'error')
    else:
        flash(
            f'Importación completada: {resultado["insertados"]} trabajadores insertados, '
            f'{resultado["duplicados"]} duplicados ignorados de {resultado["total_leidos"]} registros leídos',
            'success'
        )
    
    return redirect(url_for('trabajadores.index'))


@trabajadores_bp.route('/checadores')
def checadores():
    """API: Consultar en qué checadores está registrado un trabajador"""
    
    num_trabajador = request.args.get('num_trabajador', type=int)
    
    if not num_trabajador:
        return jsonify({'error': 'Falta el parámetro num_trabajador'}), 400
    
    # Ejecutar caso de uso
    checadores_list, error = consultar_checadores_trabajador_use_case.ejecutar(num_trabajador)
    
    if error:
        return jsonify({'error': error}), 500
    
    return jsonify({'checadores': checadores_list})


@trabajadores_bp.route('/crear', methods=['POST'])
def crear():
    """Crear nuevo trabajador"""
    
    try:
        num_trabajador = int(request.form.get('num_trabajador'))
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip() or None
        departamento = request.form.get('departamento', '').strip() or None
        tipoPlaza = request.form.get('tipoPlaza', '').strip() or None
        ingresoSEPfecha = request.form.get('ingresoSEPfecha') or None
        activo = request.form.get('activo') == '1'
        movimiento = request.form.get('movimiento', '').strip() or None
        
        if not nombre:
            flash('El nombre es requerido', 'error')
            return redirect(url_for('trabajadores.index'))
        
        # Ejecutar caso de uso
        trabajador_id, error = crear_trabajador_use_case.ejecutar(
            num_trabajador=num_trabajador,
            nombre=nombre,
            email=email,
            departamento=departamento,
            tipoPlaza=tipoPlaza,
            ingresoSEPfecha=ingresoSEPfecha,
            activo=activo,
            movimiento=movimiento
        )
        
        if error:
            flash(f'Error al crear trabajador: {error}', 'error')
        else:
            flash(f'Trabajador creado exitosamente', 'success')
        
    except ValueError:
        flash('Número de trabajador inválido', 'error')
    except Exception as e:
        flash(f'Error al crear trabajador: {str(e)}', 'error')
    
    return redirect(url_for('trabajadores.index'))


@trabajadores_bp.route('/editar/<int:id>')
def editar(id):
    """API: Obtener datos de trabajador para editar"""
    
    query = "SELECT * FROM trabajadores WHERE id = %s"
    resultado, error = query_executor.ejecutar(query, (id,))
    
    if error:
        return jsonify({'error': error}), 500
    
    if not resultado:
        return jsonify({'error': 'Trabajador no encontrado'}), 404
    
    return jsonify(resultado[0])


@trabajadores_bp.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    """Actualizar trabajador existente"""
    
    try:
        num_trabajador = int(request.form.get('num_trabajador'))
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip() or None
        tipoPlaza = request.form.get('tipoPlaza', '').strip() or None
        ingresoSEPfecha = request.form.get('ingresoSEPfecha') or None
        activo = request.form.get('activo') == '1'
        movimiento = request.form.get('movimiento', '').strip() or None
        
        if not nombre:
            flash('El nombre es requerido', 'error')
            return redirect(url_for('trabajadores.index'))
        
        # Ejecutar caso de uso
        success, error = actualizar_trabajador_use_case.ejecutar(
            trabajador_id=id,
            num_trabajador=num_trabajador,
            nombre=nombre,
            email=email,
            tipoPlaza=tipoPlaza,
            ingresoSEPfecha=ingresoSEPfecha,
            activo=activo,
            movimiento=movimiento
        )
        
        if error:
            flash(f'Error al actualizar trabajador: {error}', 'error')
        else:
            flash(f'Trabajador actualizado exitosamente', 'success')
        
    except ValueError:
        flash('Número de trabajador inválido', 'error')
    except Exception as e:
        flash(f'Error al actualizar trabajador: {str(e)}', 'error')
    
    return redirect(url_for('trabajadores.index'))


@trabajadores_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    """Eliminar trabajador"""
    
    success, error = eliminar_trabajador_use_case.ejecutar(id)
    
    if error:
        flash(f'Error al eliminar trabajador: {error}', 'error')
    else:
        flash('Trabajador eliminado exitosamente', 'success')
    
    return redirect(url_for('trabajadores.index'))


@trabajadores_bp.route('/cambiar-departamento', methods=['POST'])
def cambiar_departamento():
    """Cambiar departamento de un trabajador"""
    try:
        data = request.get_json()
        trabajador_id = data.get('trabajador_id')
        departamento_id = data.get('departamento_id')
        
        if not trabajador_id:
            return jsonify({'error': 'trabajador_id es requerido'}), 400
        
        success, error = cambiar_departamento_trabajador_use_case.ejecutar(trabajador_id, departamento_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'success': True,
            'mensaje': 'Departamento actualizado exitosamente'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@trabajadores_bp.route('/departamentos-activos')
def departamentos_activos():
    """Obtener lista de departamentos activos para el selector"""
    query = """
        SELECT id, num_departamento, nombre, nomenclatura
        FROM departamentos
        WHERE activo = 1
        ORDER BY nombre ASC
    """
    resultado, error = query_executor.ejecutar(query)
    
    if error:
        return jsonify({'error': error}), 500
    
    return jsonify({'departamentos': resultado if resultado else []})


@trabajadores_bp.route('/listar')
def listar():
    """API: Listar trabajadores para selects y otras interfaces JSON"""
    activo = request.args.get('activo')
    num_trabajador = request.args.get('num_trabajador', type=int)
    nombre = request.args.get('nombre')
    departamento_id = request.args.get('departamento_id', type=int)
    
    # Construir query
    query = """
        SELECT 
            t.id,
            t.num_trabajador,
            t.nombre,
            t.email,
            t.departamento_id,
            t.tipoPlaza,
            t.activo,
            d.nombre as departamento_nombre
        FROM trabajadores t
        LEFT JOIN departamentos d ON t.departamento_id = d.id
    """
    
    params = []
    conditions = []
    
    # Aplicar filtro de activo si se especifica
    if activo is not None:
        # Convertir a 1 o 0 según el valor
        if activo.lower() in ['true', '1', 'si']:
            activo_valor = 1
        else:
            activo_valor = 0
        conditions.append("t.activo = %s")
        params.append(activo_valor)
        print(f"[LISTAR TRABAJADORES] Filtrando por activo={activo_valor}")
    
    # Aplicar filtro por número de trabajador
    if num_trabajador is not None:
        conditions.append("t.num_trabajador = %s")
        params.append(num_trabajador)
        print(f"[LISTAR TRABAJADORES] Filtrando por num_trabajador={num_trabajador}")
    
    # Aplicar filtro por nombre (búsqueda parcial)
    if nombre:
        conditions.append("t.nombre LIKE %s")
        params.append(f"%{nombre}%")
        print(f"[LISTAR TRABAJADORES] Filtrando por nombre LIKE '%{nombre}%'")
    
    # Aplicar filtro por departamento
    if departamento_id is not None:
        conditions.append("t.departamento_id = %s")
        params.append(departamento_id)
        print(f"[LISTAR TRABAJADORES] Filtrando por departamento_id={departamento_id}")
    
    # Agregar condiciones WHERE si hay filtros
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY t.nombre ASC"
    
    print(f"[LISTAR TRABAJADORES] Query: {query}")
    print(f"[LISTAR TRABAJADORES] Params: {params}")
    
    resultado, error = query_executor.ejecutar(query, tuple(params) if params else None)
    
    if error:
        print(f"[LISTAR TRABAJADORES] Error: {error}")
        return jsonify({'error': error}), 500
    
    print(f"[LISTAR TRABAJADORES] Encontrados: {len(resultado) if resultado else 0} trabajadores")
    
    return jsonify({'trabajadores': resultado if resultado else []})


