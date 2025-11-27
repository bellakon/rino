"""
Caso de uso: Procesar Bitácora
Procesa asistencias de un trabajador en un rango de fechas
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.bitacora.services.obtener_horario_asignado_use_case import obtener_horario_asignado_use_case
from app.features.bitacora.services.obtener_checadas_dia_use_case import obtener_checadas_dia_use_case
from app.features.bitacora.services.obtener_movimiento_dia_use_case import obtener_movimiento_dia_use_case
from app.features.bitacora.services.calcular_incidencias_use_case import calcular_incidencias_use_case
from app.features.bitacora.models.bitacora_models import BitacoraRecord
from datetime import date, timedelta
from typing import List, Optional


class ProcesarBitacoraUseCase:
    """Procesa bitácora de asistencias completa"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(
        self,
        num_trabajador: int,
        fecha_inicio: date,
        fecha_fin: date,
        procesado_por: Optional[str] = None
    ) -> tuple[Optional[List[BitacoraRecord]], Optional[str]]:
        """
        Procesa la bitácora día por día
        
        Args:
            num_trabajador: Número del trabajador
            fecha_inicio: Fecha inicio del rango
            fecha_fin: Fecha fin del rango
            procesado_por: Usuario que procesa
            
        Returns:
            tuple: (lista de registros procesados, error)
        """
        try:
            # 1. Obtener información del trabajador
            trabajador_info, error = self._obtener_info_trabajador(num_trabajador)
            if error:
                return None, error
            
            # 2. Obtener horario asignado en el rango
            horarios, error = obtener_horario_asignado_use_case.ejecutar(
                num_trabajador, fecha_inicio, fecha_fin
            )
            if error:
                return None, error
            
            horario_asignado = horarios[0]
            
            # 3. Procesar día por día
            registros = []
            stats = {'insertados': 0, 'actualizados': 0, 'errores': 0, 'saltados_descanso': 0}
            fecha_actual = fecha_inicio
            
            print(f"[INFO] Iniciando procesamiento de bitácora del trabajador {num_trabajador}")
            print(f"[INFO] Rango de fechas: {fecha_inicio} a {fecha_fin}")
            
            while fecha_actual <= fecha_fin:
                # Obtener horario del día de la semana
                dia_semana = fecha_actual.weekday()  # 0=Lunes, 6=Domingo
                dia_nombre = ['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'][dia_semana]
                horario_dia = horario_asignado['horarios_por_dia'].get(dia_semana)
                
                # Verificar si hay movimiento PRIMERO (antes de saltar por descanso)
                movimiento, error = obtener_movimiento_dia_use_case.ejecutar(
                    num_trabajador, fecha_actual
                )
                if error:
                    print(f"[WARNING] Error obteniendo movimiento {fecha_actual}: {error}")
                    movimiento = None
                
                # REGLA: No procesar sábados (5) y domingos (6) EXCEPTO si:
                # 1. Tiene horario asignado para ese día (no es 'DESCANSO' ni None)
                # 2. Tiene un movimiento ese día
                es_fin_de_semana = dia_semana in [5, 6]  # Sábado o Domingo
                tiene_horario_real = horario_dia and horario_dia.upper() != 'DESCANSO'
                tiene_movimiento = movimiento and movimiento.get('tiene_movimiento')
                
                if es_fin_de_semana and not tiene_horario_real and not tiene_movimiento:
                    print(f"[DEBUG] Día {fecha_actual} ({dia_nombre}) saltado: Fin de semana sin horario ni movimiento")
                    stats['saltados_descanso'] += 1
                    fecha_actual += timedelta(days=1)
                    continue
                
                # Si no tiene horario ese día o es día de descanso pero SÍ tiene movimiento
                if (not horario_dia or horario_dia.upper() == 'DESCANSO') and tiene_movimiento:
                    horario_dia = '00:00-00:00'  # Horario ficticio para procesar el movimiento
                    print(f"[DEBUG] Día {fecha_actual} ({dia_nombre}) es DESCANSO pero tiene movimiento")
                elif not horario_dia or horario_dia.upper() == 'DESCANSO':
                    # Es descanso y NO tiene movimiento, saltar
                    print(f"[DEBUG] Día {fecha_actual} ({dia_nombre}) saltado: DESCANSO sin movimiento")
                    stats['saltados_descanso'] += 1
                    fecha_actual += timedelta(days=1)
                    continue
                
                # Obtener checadas del día (con lógica inteligente)
                checadas, error = obtener_checadas_dia_use_case.ejecutar(
                    num_trabajador, fecha_actual, horario_dia
                )
                if error:
                    print(f"[WARNING] Error obteniendo checadas {fecha_actual}: {error}")
                    checadas = {'tiene_checadas': False}
                
                # Calcular incidencias (movimiento ya se obtuvo arriba)
                resultado = calcular_incidencias_use_case.ejecutar(
                    checadas=checadas,
                    horario_esperado=horario_dia,
                    tipo_plaza=trabajador_info['tipo_plaza'],
                    movimiento=movimiento
                )
                
                # Crear registro de bitácora
                registro = BitacoraRecord(
                    num_trabajador=num_trabajador,
                    departamento=trabajador_info['departamento'],
                    nombre_trabajador=trabajador_info['nombre'],
                    fecha=fecha_actual,
                    turno_id=horario_asignado['horario_plantilla_id'],
                    horario_texto=horario_dia,
                    codigo_incidencia=resultado['codigo_incidencia'],
                    tipo_movimiento=resultado.get('tipo_movimiento'),
                    movimiento_id=movimiento['movimiento_id'] if movimiento else None,
                    checada1=checadas.get('checada1'),
                    checada2=checadas.get('checada2'),
                    checada3=checadas.get('checada3'),
                    checada4=checadas.get('checada4'),
                    minutos_retardo=resultado['minutos_retardo'],
                    horas_trabajadas=resultado['horas_trabajadas'],
                    descripcion_incidencia=resultado['descripcion_incidencia'],
                    procesado_por=procesado_por
                )
                
                # Validar
                es_valido, error_validacion = registro.validar()
                if not es_valido:
                    print(f"[ERROR] Registro inválido {fecha_actual}: {error_validacion}")
                    print(f"  - Código: {registro.codigo_incidencia}, Tipo Mov: {registro.tipo_movimiento}")
                    print(f"  - Checada1: {registro.checada1}, Checada2: {registro.checada2}")
                    print(f"  - Movimiento: {movimiento}")
                    stats['errores'] += 1
                    fecha_actual += timedelta(days=1)
                    continue
                
                # Guardar en BD
                success, error, fue_actualizado = self._guardar_registro(registro)
                if error:
                    print(f"[ERROR] Error guardando registro {fecha_actual}: {error}")
                    stats['errores'] += 1
                else:
                    accion = "actualizado" if fue_actualizado else "insertado"
                    print(f"[OK] {fecha_actual} ({dia_nombre}) {accion}: {registro.codigo_incidencia} - {registro.descripcion_incidencia[:50]}")
                    if fue_actualizado:
                        stats['actualizados'] += 1
                    else:
                        stats['insertados'] += 1
                    registros.append(registro)
                
                fecha_actual += timedelta(days=1)
            
            # Resumen final
            total_dias = (fecha_fin - fecha_inicio).days + 1
            dias_procesados = stats['insertados'] + stats['actualizados']
            print(f"\n[INFO] Resumen de procesamiento trabajador {num_trabajador}:")
            print(f"  Total de días en rango: {total_dias}")
            print(f"  Días procesados: {dias_procesados}")
            print(f"  - Insertados: {stats['insertados']}")
            print(f"  - Actualizados: {stats['actualizados']}")
            print(f"  Días saltados (descanso): {stats['saltados_descanso']}")
            print(f"  Errores: {stats['errores']}")
            print(f"  Días sin procesar: {total_dias - dias_procesados - stats['saltados_descanso']}\n")
            
            return (registros, stats), None
            
        except Exception as e:
            return None, f"Error al procesar bitácora: {str(e)}"
    
    def _obtener_info_trabajador(self, num_trabajador: int) -> tuple:
        """Obtiene información básica del trabajador"""
        query = """
            SELECT 
                t.num_trabajador,
                t.nombre,
                t.tipoPlaza,
                d.id as departamento
            FROM trabajadores t
            LEFT JOIN departamentos d ON t.departamento_id = d.id
            WHERE t.num_trabajador = %s
        """
        
        resultados, error = self.query_executor.ejecutar(query, (num_trabajador,))
        
        if error:
            return None, f"Error al obtener trabajador: {error}"
        
        if not resultados:
            return None, f"Trabajador {num_trabajador} no encontrado"
        
        trabajador = resultados[0]
        return {
            'num_trabajador': trabajador['num_trabajador'],
            'nombre': trabajador['nombre'],
            'tipo_plaza': trabajador['tipoPlaza'],
            'departamento': trabajador['departamento']
        }, None
    
    def _guardar_registro(self, registro: BitacoraRecord) -> tuple:
        """
        Guarda o actualiza un registro en la BD
        Returns:
            tuple: (success, error, fue_actualizado)
        """
        # Verificar si ya existe
        query_existe = """
            SELECT id FROM bitacora 
            WHERE num_trabajador = %s AND fecha = %s
        """
        
        resultados, error = self.query_executor.ejecutar(
            query_existe, 
            (registro.num_trabajador, registro.fecha)
        )
        
        if error:
            return False, error, False
        
        fue_actualizado = bool(resultados)
        
        if resultados:
            # UPDATE
            query = """
                UPDATE bitacora SET
                    departamento = %s,
                    nombre_trabajador = %s,
                    turno_id = %s,
                    horario_texto = %s,
                    codigo_incidencia = %s,
                    tipo_movimiento = %s,
                    movimiento_id = %s,
                    checada1 = %s,
                    checada2 = %s,
                    checada3 = %s,
                    checada4 = %s,
                    minutos_retardo = %s,
                    horas_trabajadas = %s,
                    descripcion_incidencia = %s,
                    fecha_procesamiento = NOW(),
                    procesado_por = %s
                WHERE num_trabajador = %s AND fecha = %s
            """
            params = (
                registro.departamento, registro.nombre_trabajador,
                registro.turno_id, registro.horario_texto,
                registro.codigo_incidencia, registro.tipo_movimiento,
                registro.movimiento_id, registro.checada1,
                registro.checada2, registro.checada3, registro.checada4,
                registro.minutos_retardo, registro.horas_trabajadas,
                registro.descripcion_incidencia, registro.procesado_por,
                registro.num_trabajador, registro.fecha
            )
        else:
            # INSERT
            query = """
                INSERT INTO bitacora (
                    num_trabajador, departamento, nombre_trabajador,
                    fecha, turno_id, horario_texto,
                    codigo_incidencia, tipo_movimiento, movimiento_id,
                    checada1, checada2, checada3, checada4,
                    minutos_retardo, horas_trabajadas, descripcion_incidencia,
                    fecha_procesamiento, procesado_por
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s
                )
            """
            params = (
                registro.num_trabajador, registro.departamento, registro.nombre_trabajador,
                registro.fecha, registro.turno_id, registro.horario_texto,
                registro.codigo_incidencia, registro.tipo_movimiento, registro.movimiento_id,
                registro.checada1, registro.checada2, registro.checada3, registro.checada4,
                registro.minutos_retardo, registro.horas_trabajadas, registro.descripcion_incidencia,
                registro.procesado_por
            )
        
        resultado, error = self.query_executor.ejecutar(query, params)
        
        if error:
            return False, error, fue_actualizado
        
        return True, None, fue_actualizado


# Instancia singleton
procesar_bitacora_use_case = ProcesarBitacoraUseCase()
