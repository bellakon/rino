"""
Caso de uso: Eliminar Plantilla de Horario
Responsabilidad: Validar y eliminar plantilla
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection


class EliminarPlantillaHorarioUseCase:
    """Elimina una plantilla de horario"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, id_plantilla):
        """
        Elimina una plantilla de horario
        
        Args:
            id_plantilla: ID de la plantilla
            
        Returns:
            tuple: (success, error)
        """
        try:
            # Verificar si hay trabajadores asignados con esta plantilla
            query_trabajadores = """
                SELECT COUNT(*) as total 
                FROM horarios_trabajadores 
                WHERE plantilla_horario_id = %s
            """
            resultado, error = self.query_executor.ejecutar(query_trabajadores, (id_plantilla,))
            
            if error:
                return False, error
            
            if resultado and resultado[0]['total'] > 0:
                return False, f"No se puede eliminar. Hay {resultado[0]['total']} trabajadores con este horario asignado"
            
            # Eliminar plantilla
            query = "DELETE FROM plantillas_horarios WHERE id = %s"
            _, error = self.query_executor.ejecutar(query, (id_plantilla,))
            
            if error:
                return False, error
            
            return True, None
            
        except Exception as e:
            return False, f"Error al eliminar plantilla: {str(e)}"


# Instancia singleton
eliminar_plantilla_horario_use_case = EliminarPlantillaHorarioUseCase()
