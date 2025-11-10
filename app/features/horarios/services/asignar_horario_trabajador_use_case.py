"""
Caso de uso: Asignar Horario a Trabajador
Responsabilidad: Validar y crear asignación
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.horarios.models.horario_trabajador import HorarioTrabajador


class AsignarHorarioTrabajadorUseCase:
    """Asigna un horario a un trabajador"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, horario: HorarioTrabajador):
        """
        Asigna un horario a un trabajador
        
        VALIDACIONES ESTRICTAS:
        1. El trabajador debe existir
        2. La plantilla de horario debe existir
        3. NO puede haber traslape de fechas para el mismo trabajador
        4. El traslape se verifica considerando:
           - Mismo num_trabajador
           - Rangos de fechas que se cruzan
           - Sin importar el semestre (ya que las fechas son absolutas)
        
        Args:
            horario: Objeto HorarioTrabajador
            
        Returns:
            tuple: (id_insertado, error)
        """
        try:
            print(f"[ASIGNAR] Iniciando asignación para trabajador {horario.num_trabajador}")
            print(f"[ASIGNAR] Plantilla: {horario.plantilla_horario_id}, Fechas: {horario.fecha_inicio_asignacion} - {horario.fecha_fin_asignacion}")
            
            # 0. Validar que las fechas sean obligatorias
            if not horario.fecha_inicio_asignacion:
                return None, "La fecha de inicio es obligatoria"
            
            if not horario.fecha_fin_asignacion:
                return None, "La fecha fin es obligatoria"
            
            # Validar que fecha_fin >= fecha_inicio
            if horario.fecha_fin_asignacion < horario.fecha_inicio_asignacion:
                return None, "La fecha fin no puede ser anterior a la fecha de inicio"
            
            # 1. Verificar que el trabajador existe
            query_trabajador = "SELECT num_trabajador FROM trabajadores WHERE num_trabajador = %s"
            resultado, error = self.query_executor.ejecutar(query_trabajador, (horario.num_trabajador,))
            
            if error:
                return None, error
            
            if not resultado:
                return None, f"El trabajador {horario.num_trabajador} no existe"
            
            # 2. Verificar que la plantilla existe
            query_plantilla = "SELECT id FROM plantillas_horarios WHERE id = %s"
            resultado, error = self.query_executor.ejecutar(query_plantilla, (horario.plantilla_horario_id,))
            
            if error:
                return None, error
            
            if not resultado:
                return None, "La plantilla de horario no existe"
            
            # 3. VALIDACIÓN CRÍTICA: Verificar que NO haya traslape de fechas
            # Condición de traslape entre dos rangos [A1, A2] y [B1, B2]:
            # Hay traslape si: A1 <= B2 AND A2 >= B1
            # 
            # Para la nueva asignación [nueva_inicio, nueva_fin] vs existente [existente_inicio, existente_fin]:
            # Traslape si: nueva_inicio <= existente_fin AND nueva_fin >= existente_inicio
            
            query_traslape = """
                SELECT 
                    id,
                    fecha_inicio_asignacion,
                    fecha_fin_asignacion,
                    semestre,
                    plantilla_horario_id
                FROM horarios_trabajadores
                WHERE num_trabajador = %s
                  AND activo_asignacion = 1
                  AND fecha_inicio_asignacion <= %s
                  AND (fecha_fin_asignacion >= %s OR fecha_fin_asignacion IS NULL)
            """
            params_traslape = (
                horario.num_trabajador,
                horario.fecha_fin_asignacion,      # nueva_inicio <= existente_fin
                horario.fecha_inicio_asignacion    # nueva_fin >= existente_inicio
            )
            
            resultado_traslape, error = self.query_executor.ejecutar(query_traslape, params_traslape)
            
            if error:
                return None, error
            
            if resultado_traslape:
                # Hay traslape, construir mensaje detallado
                traslapes = []
                for asig in resultado_traslape:
                    fin = asig['fecha_fin_asignacion'] if asig['fecha_fin_asignacion'] else 'Indefinido'
                    traslapes.append(
                        f"ID {asig['id']}: {asig['fecha_inicio_asignacion']} - {fin} (Semestre: {asig['semestre']})"
                    )
                
                mensaje_error = (
                    f"No se puede asignar el horario. El trabajador {horario.num_trabajador} "
                    f"ya tiene asignaciones que se traslapan con el rango de fechas solicitado "
                    f"({horario.fecha_inicio_asignacion} - {horario.fecha_fin_asignacion or 'Indefinido'}).\n"
                    f"Asignaciones conflictivas:\n" + "\n".join(traslapes)
                )
                
                print(f"[ASIGNAR] TRASLAPE DETECTADO: {mensaje_error}")
                
                return None, mensaje_error
            
            # 4. No hay traslapes, proceder con la inserción
            query = """
                INSERT INTO horarios_trabajadores (
                    num_trabajador, plantilla_horario_id, fecha_inicio_asignacion,
                    fecha_fin_asignacion, semestre, estado_asignacion, activo_asignacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            params = (
                horario.num_trabajador,
                horario.plantilla_horario_id,
                horario.fecha_inicio_asignacion,
                horario.fecha_fin_asignacion,
                horario.semestre,
                horario.estado_asignacion,
                horario.activo_asignacion
            )
            
            resultado, error = self.query_executor.ejecutar(query, params)
            
            if error:
                return None, error
            
            # Obtener el ID insertado
            query_last_id = "SELECT LAST_INSERT_ID() as id"
            resultado_id, _ = self.query_executor.ejecutar(query_last_id)
            id_insertado = resultado_id[0]['id'] if resultado_id else None
            
            print(f"[ASIGNAR] Asignación EXITOSA: ID={id_insertado}")
            
            return id_insertado, None
            
        except Exception as e:
            return None, f"Error al asignar horario: {str(e)}"


# Instancia singleton
asignar_horario_trabajador_use_case = AsignarHorarioTrabajadorUseCase()
