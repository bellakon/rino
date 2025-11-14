"""
Caso de uso: Obtener Horario Asignado
Obtiene el horario asignado a un trabajador en un rango de fechas
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from datetime import date
from typing import Optional, List, Dict


class ObtenerHorarioAsignadoUseCase:
    """Obtiene horarios asignados a un trabajador"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(
        self,
        num_trabajador: int,
        fecha_inicio: date,
        fecha_fin: date
    ) -> tuple[Optional[List[Dict]], Optional[str]]:
        """
        Obtiene el horario asignado en el rango de fechas
        
        Args:
            num_trabajador: Número del trabajador
            fecha_inicio: Fecha inicio del rango
            fecha_fin: Fecha fin del rango
            
        Returns:
            tuple: (lista de horarios por día, error)
        """
        try:
            # Obtener asignaciones de horario que cubren el rango
            query = """
                SELECT 
                    ht.id,
                    ht.num_trabajador,
                    ht.fecha_inicio_asignacion as fecha_inicio,
                    ht.fecha_fin_asignacion as fecha_fin,
                    ht.plantilla_horario_id as horario_plantilla_id,
                    ph.nombre_horario as horario_nombre,
                    ph.descripcion_horario as turno_nomenclatura,
                    ph.lunes_entrada_1, ph.lunes_salida_1, ph.lunes_entrada_2, ph.lunes_salida_2,
                    ph.martes_entrada_1, ph.martes_salida_1, ph.martes_entrada_2, ph.martes_salida_2,
                    ph.miercoles_entrada_1, ph.miercoles_salida_1, ph.miercoles_entrada_2, ph.miercoles_salida_2,
                    ph.jueves_entrada_1, ph.jueves_salida_1, ph.jueves_entrada_2, ph.jueves_salida_2,
                    ph.viernes_entrada_1, ph.viernes_salida_1, ph.viernes_entrada_2, ph.viernes_salida_2,
                    ph.sabado_entrada_1, ph.sabado_salida_1, ph.sabado_entrada_2, ph.sabado_salida_2,
                    ph.domingo_entrada_1, ph.domingo_salida_1, ph.domingo_entrada_2, ph.domingo_salida_2
                FROM horarios_trabajadores ht
                INNER JOIN plantillas_horarios ph ON ht.plantilla_horario_id = ph.id
                WHERE ht.num_trabajador = %s
                AND ht.fecha_inicio_asignacion <= %s
                AND (ht.fecha_fin_asignacion IS NULL OR ht.fecha_fin_asignacion >= %s)
                AND ht.activo_asignacion = 1
                ORDER BY ht.fecha_inicio_asignacion DESC
                LIMIT 1
            """
            
            resultados, error = self.query_executor.ejecutar(
                query, 
                (num_trabajador, fecha_fin, fecha_inicio)
            )
            
            if error:
                return None, f"Error al obtener horario asignado: {error}"
            
            if not resultados:
                return None, "Trabajador no tiene horario asignado en el rango de fechas"
            
            asignacion = resultados[0]
            
            # Función auxiliar para construir horario de un día
            def construir_horario_dia(entrada_1, salida_1, entrada_2, salida_2):
                """Construye el texto de horario para un día específico"""
                if not entrada_1 and not entrada_2:
                    return "DESCANSO"
                
                # Convertir time/timedelta a string
                def time_to_str(t):
                    if t is None:
                        return None
                    if isinstance(t, str):
                        return t
                    # MySQL TIME se convierte a timedelta
                    from datetime import timedelta
                    if isinstance(t, timedelta):
                        total_seconds = int(t.total_seconds())
                        hours = total_seconds // 3600
                        minutes = (total_seconds % 3600) // 60
                        return f"{hours:02d}:{minutes:02d}"
                    # Si es datetime.time
                    return t.strftime('%H:%M')
                
                entrada_1_str = time_to_str(entrada_1)
                salida_1_str = time_to_str(salida_1)
                entrada_2_str = time_to_str(entrada_2)
                salida_2_str = time_to_str(salida_2)
                
                # Si tiene segundo turno, es mixto
                if entrada_2_str and salida_2_str:
                    return f"{entrada_1_str}-{salida_1_str},{entrada_2_str}-{salida_2_str}"
                elif entrada_1_str and salida_1_str:
                    return f"{entrada_1_str}-{salida_1_str}"
                else:
                    return "DESCANSO"
            
            # Construir respuesta con horario por día de la semana
            horario_info = {
                'asignacion_id': asignacion['id'],
                'horario_plantilla_id': asignacion['horario_plantilla_id'],
                'horario_nombre': asignacion['horario_nombre'],
                'turno_nomenclatura': asignacion['turno_nomenclatura'],
                'fecha_inicio_asignacion': asignacion['fecha_inicio'],
                'fecha_fin_asignacion': asignacion['fecha_fin'],
                'horarios_por_dia': {
                    0: construir_horario_dia(asignacion['lunes_entrada_1'], asignacion['lunes_salida_1'], 
                                            asignacion['lunes_entrada_2'], asignacion['lunes_salida_2']),
                    1: construir_horario_dia(asignacion['martes_entrada_1'], asignacion['martes_salida_1'],
                                            asignacion['martes_entrada_2'], asignacion['martes_salida_2']),
                    2: construir_horario_dia(asignacion['miercoles_entrada_1'], asignacion['miercoles_salida_1'],
                                            asignacion['miercoles_entrada_2'], asignacion['miercoles_salida_2']),
                    3: construir_horario_dia(asignacion['jueves_entrada_1'], asignacion['jueves_salida_1'],
                                            asignacion['jueves_entrada_2'], asignacion['jueves_salida_2']),
                    4: construir_horario_dia(asignacion['viernes_entrada_1'], asignacion['viernes_salida_1'],
                                            asignacion['viernes_entrada_2'], asignacion['viernes_salida_2']),
                    5: construir_horario_dia(asignacion['sabado_entrada_1'], asignacion['sabado_salida_1'],
                                            asignacion['sabado_entrada_2'], asignacion['sabado_salida_2']),
                    6: construir_horario_dia(asignacion['domingo_entrada_1'], asignacion['domingo_salida_1'],
                                            asignacion['domingo_entrada_2'], asignacion['domingo_salida_2'])
                }
            }
            
            return [horario_info], None
            
        except Exception as e:
            return None, f"Error al obtener horario asignado: {str(e)}"


# Instancia singleton
obtener_horario_asignado_use_case = ObtenerHorarioAsignadoUseCase()
