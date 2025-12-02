"""
Caso de uso: Editar Registro de Bitácora Manualmente
Permite editar checadas y recalcular incidencias para un registro específico
"""
from datetime import datetime, time, date
from decimal import Decimal
from typing import Optional, Dict, Tuple

from app.core.database.query_executor import query_executor
from app.features.bitacora.services.calcular_incidencias_use_case import calcular_incidencias_use_case
from app.features.bitacora.services.obtener_movimiento_dia_use_case import obtener_movimiento_dia_use_case


class EditarRegistroBitacoraUseCase:
    """
    Edita un registro de bitácora manualmente.
    Permite modificar checadas, updatable y recalcula incidencias.
    """
    
    def __init__(self):
        self.query_executor = query_executor
    
    def obtener_registro(self, registro_id: int) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Obtiene un registro de bitácora por ID
        
        Args:
            registro_id: ID del registro
            
        Returns:
            Tuple: (registro_dict, error)
        """
        query = """
            SELECT 
                b.id, b.num_trabajador, b.departamento, b.nombre_trabajador,
                b.fecha, b.turno_id, b.horario_texto,
                b.codigo_incidencia, b.tipo_movimiento, b.movimiento_id,
                b.checada1, b.checada2, b.checada3, b.checada4,
                b.minutos_retardo, b.horas_trabajadas, b.descripcion_incidencia,
                b.updatable, b.fecha_procesamiento, b.procesado_por,
                t.tipoPlaza
            FROM bitacora b
            LEFT JOIN trabajadores t ON b.num_trabajador = t.num_trabajador
            WHERE b.id = %s
        """
        
        resultado, error = self.query_executor.ejecutar(query, (registro_id,))
        
        if error:
            return None, f"Error al obtener registro: {error}"
        
        if not resultado:
            return None, "Registro no encontrado"
        
        registro = resultado[0]
        
        # Convertir timedelta a string HH:MM:SS
        def td_to_str(td):
            if td is None:
                return None
            if isinstance(td, str):
                return td
            if hasattr(td, 'total_seconds'):
                total_seconds = int(td.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            return str(td)
        
        return {
            'id': registro['id'],
            'num_trabajador': registro['num_trabajador'],
            'departamento': registro['departamento'],
            'nombre_trabajador': registro['nombre_trabajador'],
            'fecha': registro['fecha'].isoformat() if registro['fecha'] else None,
            'turno_id': registro['turno_id'],
            'horario_texto': registro['horario_texto'],
            'codigo_incidencia': registro['codigo_incidencia'],
            'tipo_movimiento': registro['tipo_movimiento'],
            'movimiento_id': registro['movimiento_id'],
            'checada1': td_to_str(registro['checada1']),
            'checada2': td_to_str(registro['checada2']),
            'checada3': td_to_str(registro['checada3']),
            'checada4': td_to_str(registro['checada4']),
            'minutos_retardo': registro['minutos_retardo'],
            'horas_trabajadas': float(registro['horas_trabajadas']) if registro['horas_trabajadas'] else 0,
            'descripcion_incidencia': registro['descripcion_incidencia'],
            'updatable': registro['updatable'],
            'tipo_plaza': registro['tipoPlaza'] or 'BASE'
        }, None
    
    def ejecutar(
        self,
        registro_id: int,
        checada1: Optional[str],
        checada2: Optional[str],
        checada3: Optional[str],
        checada4: Optional[str],
        updatable: bool,
        editado_por: str = 'MANUAL'
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Edita un registro de bitácora y recalcula incidencias
        
        Args:
            registro_id: ID del registro a editar
            checada1-4: Checadas en formato HH:MM:SS o None
            updatable: Si el registro puede ser actualizado en reprocesamiento
            editado_por: Usuario que realiza la edición
            
        Returns:
            Tuple: (registro_actualizado, error)
        """
        # 1. Obtener registro actual
        registro, error = self.obtener_registro(registro_id)
        if error:
            return None, error
        
        # 2. Parsear checadas
        def parse_time(time_str):
            if not time_str or time_str.strip() == '':
                return None
            try:
                # Soportar HH:MM y HH:MM:SS
                if len(time_str.split(':')) == 2:
                    time_str += ':00'
                return datetime.strptime(time_str, '%H:%M:%S').time()
            except:
                return None
        
        checada1_time = parse_time(checada1)
        checada2_time = parse_time(checada2)
        checada3_time = parse_time(checada3)
        checada4_time = parse_time(checada4)
        
        # 3. Preparar datos de checadas para el cálculo
        tiene_checadas = checada1_time is not None
        checadas_dict = {
            'tiene_checadas': tiene_checadas,
            'checada1': checada1_time,
            'checada2': checada2_time,
            'checada3': checada3_time,
            'checada4': checada4_time
        }
        
        # 4. Obtener movimiento del día (si existe)
        fecha_registro = datetime.strptime(registro['fecha'], '%Y-%m-%d').date()
        movimiento, _ = obtener_movimiento_dia_use_case.ejecutar(
            registro['num_trabajador'],
            fecha_registro
        )
        
        # 5. Recalcular incidencias usando la lógica existente
        resultado_calculo = calcular_incidencias_use_case.ejecutar(
            checadas=checadas_dict,
            horario_esperado=registro['horario_texto'] or '00:00-00:00',
            tipo_plaza=registro['tipo_plaza'],
            movimiento=movimiento
        )
        
        # 6. Actualizar registro en BD
        query = """
            UPDATE bitacora SET
                checada1 = %s,
                checada2 = %s,
                checada3 = %s,
                checada4 = %s,
                codigo_incidencia = %s,
                tipo_movimiento = %s,
                minutos_retardo = %s,
                horas_trabajadas = %s,
                descripcion_incidencia = %s,
                updatable = %s,
                fecha_procesamiento = NOW(),
                procesado_por = %s
            WHERE id = %s
        """
        
        params = (
            checada1_time,
            checada2_time,
            checada3_time,
            checada4_time,
            resultado_calculo['codigo_incidencia'],
            resultado_calculo['tipo_movimiento'],
            resultado_calculo['minutos_retardo'],
            resultado_calculo['horas_trabajadas'],
            resultado_calculo['descripcion_incidencia'],
            updatable,
            editado_por,
            registro_id
        )
        
        _, error = self.query_executor.ejecutar(query, params)
        
        if error:
            return None, f"Error al actualizar registro: {error}"
        
        # 7. Retornar registro actualizado
        registro_actualizado, _ = self.obtener_registro(registro_id)
        
        return registro_actualizado, None


# Instancia singleton
editar_registro_bitacora_use_case = EditarRegistroBitacoraUseCase()
