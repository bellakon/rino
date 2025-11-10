"""
Caso de uso: Obtener Asignación de Horario
Responsabilidad: Obtener una asignación específica por ID
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection


class ObtenerAsignacionUseCase:
    """Obtiene una asignación de horario por ID"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, id_asignacion):
        """
        Obtiene una asignación por ID
        
        Args:
            id_asignacion: ID de la asignación
            
        Returns:
            tuple: (asignacion_dict, error)
        """
        try:
            query = """
                SELECT 
                    ht.id,
                    ht.num_trabajador,
                    ht.plantilla_horario_id,
                    ht.fecha_inicio_asignacion,
                    ht.fecha_fin_asignacion,
                    ht.semestre,
                    ht.estado_asignacion,
                    ht.activo_asignacion,
                    t.nombre as nombre_completo,
                    ph.nombre_horario
                FROM horarios_trabajadores ht
                INNER JOIN trabajadores t ON ht.num_trabajador = t.num_trabajador
                INNER JOIN plantillas_horarios ph ON ht.plantilla_horario_id = ph.id
                WHERE ht.id = %s
            """
            
            resultado, error = self.query_executor.ejecutar(query, (id_asignacion,))
            
            if error:
                return None, error
            
            if not resultado:
                return None, "Asignación no encontrada"
            
            return resultado[0], None
            
        except Exception as e:
            return None, f"Error al obtener asignación: {str(e)}"


# Instancia singleton
obtener_asignacion_use_case = ObtenerAsignacionUseCase()
