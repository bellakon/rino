"""
Caso de uso: Eliminar Asignación de Horario
Responsabilidad: Eliminar una asignación (DELETE real)
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection


class EliminarAsignacionUseCase:
    """Elimina una asignación de horario (DELETE de la BD)"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, id_asignacion):
        """
        Elimina una asignación de horario
        
        Args:
            id_asignacion: ID de la asignación a eliminar
            
        Returns:
            tuple: (success, error)
        """
        try:
            print(f"[ELIMINAR ASIGNACION] ID: {id_asignacion}")
            
            # Verificar que la asignación existe
            query_check = "SELECT id FROM horarios_trabajadores WHERE id = %s"
            resultado, error = self.query_executor.ejecutar(query_check, (id_asignacion,))
            
            if error:
                return False, error
            
            if not resultado:
                return False, "Asignación no encontrada"
            
            # DELETE real de la base de datos
            query = "DELETE FROM horarios_trabajadores WHERE id = %s"
            
            resultado, error = self.query_executor.ejecutar(query, (id_asignacion,))
            
            if error:
                return False, error
            
            print(f"[ELIMINAR ASIGNACION] Asignación {id_asignacion} eliminada de la BD")
            return True, None
            
        except Exception as e:
            return False, f"Error al eliminar asignación: {str(e)}"


# Instancia singleton
eliminar_asignacion_use_case = EliminarAsignacionUseCase()
