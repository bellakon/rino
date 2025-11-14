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
            stats = {'insertados': 0, 'actualizados': 0, 'errores': 0}
            fecha_actual = fecha_inicio
            
            while fecha_actual <= fecha_fin:
                # Obtener horario del día de la semana
                dia_semana = fecha_actual.weekday()  # 0=Lunes, 6=Domingo
                horario_dia = horario_asignado['horarios_por_dia'].get(dia_semana)
                
                # Si no tiene horario ese día, pasar al siguiente
                if not horario_dia or horario_dia == 'Descanso':
                    fecha_actual += timedelta(days=1)
                    continue
                
                # Obtener checadas del día
                checadas, error = obtener_checadas_dia_use_case.ejecutar(
                    num_trabajador, fecha_actual
                )
                if error:
                    print(f"[WARNING] Error obteniendo checadas {fecha_actual}: {error}")
                    checadas = {'tiene_checadas': False}
                
                # Obtener movimiento del día (si existe)
                movimiento, error = obtener_movimiento_dia_use_case.ejecutar(
                    num_trabajador, fecha_actual
                )
                if error:
                    print(f"[WARNING] Error obteniendo movimiento {fecha_actual}: {error}")
                    movimiento = None
                
                # Calcular incidencias
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
                    print(f"[WARNING] Registro inválido {fecha_actual}: {error_validacion}")
                    stats['errores'] += 1
                    fecha_actual += timedelta(days=1)
                    continue
                
                # Guardar en BD
                success, error, fue_actualizado = self._guardar_registro(registro)
                if error:
                    print(f"[ERROR] Error guardando registro {fecha_actual}: {error}")
                    stats['errores'] += 1
                else:
                    if fue_actualizado:
                        stats['actualizados'] += 1
                    else:
                        stats['insertados'] += 1
                    registros.append(registro)
                
                fecha_actual += timedelta(days=1)
            
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
