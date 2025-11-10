"""
Caso de uso: Editar Asignación de Horario
Responsabilidad: Actualizar fechas y datos de una asignación existente
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection


class EditarAsignacionUseCase:
    """Edita una asignación de horario existente"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, id_asignacion, fecha_inicio, fecha_fin, semestre, estado):
        """
        Edita una asignación de horario
        
        VALIDACIONES:
        1. La asignación debe existir
        2. Fecha inicio y fin son obligatorias
        3. Fecha fin >= fecha inicio
        4. No traslape con otras asignaciones del mismo trabajador
        
        Args:
            id_asignacion: ID de la asignación a editar
            fecha_inicio: Nueva fecha inicio (YYYY-MM-DD)
            fecha_fin: Nueva fecha fin (YYYY-MM-DD)
            semestre: Nuevo semestre
            estado: Nuevo estado
            
        Returns:
            tuple: (success, error)
        """
        try:
            print(f"[EDITAR ASIGNACION] ID: {id_asignacion}, Fechas: {fecha_inicio} - {fecha_fin}")
            
            # 1. Validar fechas obligatorias
            if not fecha_inicio:
                return False, "La fecha de inicio es obligatoria"
            
            if not fecha_fin:
                return False, "La fecha fin es obligatoria"
            
            if fecha_fin < fecha_inicio:
                return False, "La fecha fin no puede ser anterior a la fecha de inicio"
            
            # 2. Obtener la asignación actual para saber el trabajador
            query_actual = "SELECT num_trabajador FROM horarios_trabajadores WHERE id = %s"
            resultado_actual, error = self.query_executor.ejecutar(query_actual, (id_asignacion,))
            
            if error:
                return False, error
            
            if not resultado_actual:
                return False, "Asignación no encontrada"
            
            num_trabajador = resultado_actual[0]['num_trabajador']
            
            # 3. Validar que NO haya traslape con otras asignaciones del mismo trabajador
            # Excluir la asignación actual (id != id_asignacion)
            query_traslape = """
                SELECT 
                    id,
                    fecha_inicio_asignacion,
                    fecha_fin_asignacion,
                    semestre
                FROM horarios_trabajadores
                WHERE num_trabajador = %s
                  AND id != %s
                  AND activo_asignacion = 1
                  AND fecha_inicio_asignacion <= %s
                  AND (fecha_fin_asignacion >= %s OR fecha_fin_asignacion IS NULL)
            """
            params_traslape = (
                num_trabajador,
                id_asignacion,
                fecha_fin,      # nueva_inicio <= existente_fin
                fecha_inicio    # nueva_fin >= existente_inicio
            )
            
            resultado_traslape, error = self.query_executor.ejecutar(query_traslape, params_traslape)
            
            if error:
                return False, error
            
            if resultado_traslape:
                # Hay traslape con otra asignación
                traslapes = []
                for asig in resultado_traslape:
                    fin = asig['fecha_fin_asignacion'] if asig['fecha_fin_asignacion'] else 'Indefinido'
                    traslapes.append(
                        f"ID {asig['id']}: {asig['fecha_inicio_asignacion']} - {fin} (Semestre: {asig['semestre']})"
                    )
                
                mensaje_error = (
                    f"No se puede actualizar. Ya existe(n) asignación(es) que se traslapan "
                    f"con el nuevo rango de fechas ({fecha_inicio} - {fecha_fin}):\n"
                    + "\n".join(traslapes)
                )
                
                print(f"[EDITAR ASIGNACION] TRASLAPE DETECTADO: {mensaje_error}")
                return False, mensaje_error
            
            # 4. No hay traslapes, proceder con la actualización
            query_update = """
                UPDATE horarios_trabajadores
                SET 
                    fecha_inicio_asignacion = %s,
                    fecha_fin_asignacion = %s,
                    semestre = %s,
                    estado_asignacion = %s
                WHERE id = %s
            """
            
            params_update = (
                fecha_inicio,
                fecha_fin,
                semestre,
                estado,
                id_asignacion
            )
            
            resultado, error = self.query_executor.ejecutar(query_update, params_update)
            
            if error:
                return False, error
            
            print(f"[EDITAR ASIGNACION] Asignación {id_asignacion} actualizada exitosamente")
            return True, None
            
        except Exception as e:
            return False, f"Error al editar asignación: {str(e)}"


# Instancia singleton
editar_asignacion_use_case = EditarAsignacionUseCase()
