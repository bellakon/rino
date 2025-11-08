"""
Caso de uso: Eliminar trabajador
Responsabilidad: Eliminar trabajador de la base de datos
"""
from app.core.database.query_executor import query_executor


class EliminarTrabajadorUseCase:
    """Elimina un trabajador de la base de datos"""
    
    def ejecutar(self, trabajador_id):
        """
        Elimina un trabajador por su ID
        
        Args:
            trabajador_id: ID del trabajador a eliminar
        
        Returns:
            tuple: (success boolean, error)
        """
        try:
            query = "DELETE FROM trabajadores WHERE id = %s"
            
            resultado, error = query_executor.ejecutar(query, (trabajador_id,))
            
            if error:
                return False, error
            
            return True, None
            
        except Exception as e:
            return False, f"Error al eliminar trabajador: {str(e)}"


# Instancia singleton
eliminar_trabajador_use_case = EliminarTrabajadorUseCase()
