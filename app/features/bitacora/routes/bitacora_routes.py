from flask import Blueprint, render_template, request, jsonify, send_file
import logging
from app.features.bitacora.services.procesar_bitacora_use_case import ProcesarBitacoraUseCase
from app.features.bitacora.services.listar_bitacora_use_case import ListarBitacoraUseCase
from app.features.bitacora.services.obtener_horario_asignado_use_case import ObtenerHorarioAsignadoUseCase
from app.features.bitacora.services.generar_pdf_bitacora_use_case import generar_pdf_bitacora_use_case

# Configurar logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

bitacora_bp = Blueprint('bitacora', __name__, url_prefix='/bitacora', template_folder='../templates')

logger.info(f"[BITACORA] Blueprint created")

@bitacora_bp.route('/')
def index():
    """Página principal de bitácora"""
    try:
        logger.info("[BITACORA] Accediendo a ruta /bitacora/")
        logger.debug(f"[BITACORA] Template folder: {bitacora_bp.template_folder}")
        logger.debug(f"[BITACORA] Renderizando: bitacora/index.html")
        return render_template('bitacora/index.html')
    except Exception as e:
        logger.error(f"[BITACORA] Error en index(): {str(e)}")
        logger.error(f"[BITACORA] Exception type: {type(e).__name__}")
        import traceback
        logger.error(f"[BITACORA] Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'message': f'Error al cargar bitácora: {str(e)}'
        }), 500

@bitacora_bp.route('/horario', methods=['POST'])
def obtener_horario():
    """Obtiene el horario asignado de un trabajador en un rango de fechas"""
    try:
        logger.info("[BITACORA] POST /bitacora/horario")
        data = request.get_json()
        num_trabajador = data.get('num_trabajador')
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        logger.debug(f"[BITACORA] Parámetros: trabajador={num_trabajador}, inicio={fecha_inicio}, fin={fecha_fin}")
        
        if not all([num_trabajador, fecha_inicio, fecha_fin]):
            logger.warning("[BITACORA] Datos incompletos")
            return jsonify({
                'success': False,
                'message': 'Datos incompletos'
            }), 400
        
        use_case = ObtenerHorarioAsignadoUseCase()
        logger.debug("[BITACORA] Ejecutando ObtenerHorarioAsignadoUseCase")
        horarios, error = use_case.ejecutar(num_trabajador, fecha_inicio, fecha_fin)
        
        if error:
            logger.error(f"[BITACORA] Error en caso de uso: {error}")
            return jsonify({
                'success': False,
                'message': error
            }), 404
        
        if not horarios:
            logger.warning("[BITACORA] No se encontró horario")
            return jsonify({
                'success': False,
                'message': 'No se encontró horario asignado para este trabajador en el rango de fechas'
            }), 404
        
        logger.info(f"[BITACORA] Horario obtenido exitosamente")
        return jsonify({
            'success': True,
            'horario': horarios[0] if horarios else None
        })
        
    except Exception as e:
        logger.error(f"[BITACORA] Error en obtener_horario(): {str(e)}")
        logger.error(f"[BITACORA] Traceback: {__import__('traceback').format_exc()}")
        return jsonify({
            'success': False,
            'message': f'Error al obtener horario: {str(e)}'
        }), 500

@bitacora_bp.route('/procesar', methods=['POST'])
def procesar_bitacora():
    """Procesa la bitácora de un trabajador en un rango de fechas"""
    try:
        logger.info("[BITACORA] POST /bitacora/procesar")
        data = request.get_json()
        num_trabajador = data.get('num_trabajador')
        fecha_inicio_str = data.get('fecha_inicio')
        fecha_fin_str = data.get('fecha_fin')
        
        logger.debug(f"[BITACORA] Parámetros: trabajador={num_trabajador}, inicio={fecha_inicio_str}, fin={fecha_fin_str}")
        
        if not all([num_trabajador, fecha_inicio_str, fecha_fin_str]):
            logger.warning("[BITACORA] Datos incompletos en procesar")
            return jsonify({
                'success': False,
                'message': 'Datos incompletos'
            }), 400
        
        # Convertir strings a objetos date
        from datetime import datetime
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
        except ValueError as e:
            logger.error(f"[BITACORA] Error al parsear fechas: {e}")
            return jsonify({
                'success': False,
                'message': 'Formato de fecha inválido. Use YYYY-MM-DD'
            }), 400
        
        use_case = ProcesarBitacoraUseCase()
        logger.debug("[BITACORA] Ejecutando ProcesarBitacoraUseCase")
        resultado, error = use_case.ejecutar(num_trabajador, fecha_inicio, fecha_fin)
        
        if error:
            logger.error(f"[BITACORA] Error en procesar: {error}")
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        # Desempaquetar resultado (registros, stats)
        registros, stats = resultado
        
        # Convertir BitacoraRecord a dict si es necesario
        registros_dict = []
        for reg in (registros or []):
            if hasattr(reg, 'to_dict'):
                registros_dict.append(reg.to_dict())
            else:
                registros_dict.append(reg if isinstance(reg, dict) else {})
        
        # Construir mensaje informativo
        mensaje_partes = []
        if stats['insertados'] > 0:
            mensaje_partes.append(f"{stats['insertados']} nuevos registros creados")
        if stats['actualizados'] > 0:
            mensaje_partes.append(f"{stats['actualizados']} registros actualizados")
        if stats['errores'] > 0:
            mensaje_partes.append(f"{stats['errores']} errores")
        
        mensaje = "Bitácora procesada exitosamente. " + ", ".join(mensaje_partes) + "."
        
        logger.info(f"[BITACORA] {mensaje}")
        return jsonify({
            'success': True,
            'message': mensaje,
            'registros': registros_dict,
            'stats': stats
        })
        
    except ValueError as e:
        logger.error(f"[BITACORA] ValueError en procesar: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        logger.error(f"[BITACORA] Error en procesar_bitacora(): {str(e)}")
        logger.error(f"[BITACORA] Traceback: {__import__('traceback').format_exc()}")
        return jsonify({
            'success': False,
            'message': f'Error al procesar bitácora: {str(e)}'
        }), 500

@bitacora_bp.route('/listar', methods=['GET'])
def listar_bitacora():
    """Lista registros de bitácora con filtros opcionales"""
    try:
        logger.info("[BITACORA] GET /bitacora/listar")
        # Obtener parámetros de la query string
        num_trabajador = request.args.get('num_trabajador')
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        codigo_incidencia = request.args.get('codigo_incidencia')
        
        logger.debug(f"[BITACORA] Filtros: trabajador={num_trabajador}, inicio={fecha_inicio}, fin={fecha_fin}, codigo={codigo_incidencia}")
        
        use_case = ListarBitacoraUseCase()
        logger.debug("[BITACORA] Ejecutando ListarBitacoraUseCase")
        registros, error = use_case.ejecutar(
            num_trabajador=num_trabajador,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            codigo_incidencia=codigo_incidencia
        )
        
        if error:
            logger.error(f"[BITACORA] Error en listar: {error}")
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        logger.info(f"[BITACORA] Listado obtenido: {len(registros or [])} registros")
        return jsonify({
            'success': True,
            'registros': registros or []
        })
        
    except Exception as e:
        logger.error(f"[BITACORA] Error en listar_bitacora(): {str(e)}")
        logger.error(f"[BITACORA] Traceback: {__import__('traceback').format_exc()}")
        return jsonify({
            'success': False,
            'message': f'Error al listar bitácora: {str(e)}'
        }), 500

@bitacora_bp.route('/generar-pdf', methods=['POST'])
def generar_pdf():
    """Genera PDF de bitácora procesada"""
    try:
        logger.info("[BITACORA] POST /bitacora/generar-pdf")
        data = request.get_json()
        registros_dict = data.get('registros', [])
        nombre_trabajador = data.get('nombre_trabajador', '')
        num_trabajador = data.get('num_trabajador', '')
        fecha_inicio = data.get('fecha_inicio', '')
        fecha_fin = data.get('fecha_fin', '')
        
        logger.debug(f"[BITACORA] Generando PDF para {len(registros_dict)} registros")
        
        if not registros_dict:
            return jsonify({
                'success': False,
                'message': 'No hay registros para generar PDF'
            }), 400
        
        # Convertir dict a BitacoraRecord
        from app.features.bitacora.models.bitacora_models import BitacoraRecord
        from datetime import datetime
        from decimal import Decimal
        
        registros = []
        for reg_dict in registros_dict:
            # Parsear fecha si es string
            fecha = reg_dict.get('fecha')
            if isinstance(fecha, str):
                fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            
            registro = BitacoraRecord(
                id=reg_dict.get('id'),
                num_trabajador=reg_dict.get('num_trabajador'),
                departamento=reg_dict.get('departamento'),
                nombre_trabajador=reg_dict.get('nombre_trabajador'),
                fecha=fecha,
                turno_id=reg_dict.get('turno_id'),
                horario_texto=reg_dict.get('horario_texto'),
                codigo_incidencia=reg_dict.get('codigo_incidencia'),
                tipo_movimiento=reg_dict.get('tipo_movimiento'),
                movimiento_id=reg_dict.get('movimiento_id'),
                checada1=reg_dict.get('checada1'),
                checada2=reg_dict.get('checada2'),
                checada3=reg_dict.get('checada3'),
                checada4=reg_dict.get('checada4'),
                minutos_retardo=reg_dict.get('minutos_retardo', 0),
                horas_trabajadas=Decimal(str(reg_dict.get('horas_trabajadas', 0))),
                descripcion_incidencia=reg_dict.get('descripcion_incidencia')
            )
            registros.append(registro)
        
        # Generar PDF
        buffer, error = generar_pdf_bitacora_use_case.ejecutar(
            registros=registros,
            nombre_trabajador=nombre_trabajador,
            num_trabajador=num_trabajador,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
        if error:
            logger.error(f"[BITACORA] Error generando PDF: {error}")
            return jsonify({
                'success': False,
                'message': error
            }), 500
        
        # Enviar PDF
        logger.info("[BITACORA] PDF generado exitosamente")
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'bitacora_{num_trabajador}_{fecha_inicio}_{fecha_fin}.pdf'
        )
        
    except Exception as e:
        logger.error(f"[BITACORA] Error en generar_pdf(): {str(e)}")
        logger.error(f"[BITACORA] Traceback: {__import__('traceback').format_exc()}")
        return jsonify({
            'success': False,
            'message': f'Error al generar PDF: {str(e)}'
        }), 500
