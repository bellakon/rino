"""
Caso de uso: Eliminar Movimiento
Responsabilidad: Eliminar un movimiento de la BD
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from typing import Tuple, Optional


class EliminarMovimientoUseCase:
    """Elimina un movimiento"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, movimiento_id: int) -> Tuple[bool, Optional[str]]:
        """
        Elimina un movimiento
        
        Args:
            movimiento_id: ID del movimiento a eliminar
            
        Returns:
            tuple: (exito, mensaje_error)
        """
        try:
            # Verificar que el movimiento existe
            query_existe = "SELECT id FROM movimientos WHERE id = %s"
            resultado, error = self.query_executor.ejecutar(query_existe, (movimiento_id,))
            
            if error:
                return False, error
            
            if not resultado:
                return False, "Movimiento no encontrado"
            
            # Eliminar
            query = "DELETE FROM movimientos WHERE id = %s"
            resultado, error = self.query_executor.ejecutar(query, (movimiento_id,))
            
            if error:
                return False, error
            
            return True, None
            
        except Exception as e:
            return False, f"Error al eliminar movimiento: {str(e)}"


# Instancia singleton
eliminar_movimiento_use_case = EliminarMovimientoUseCase()
