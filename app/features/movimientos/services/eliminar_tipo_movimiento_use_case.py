"""
Caso de uso: Eliminar Tipo de Movimiento
Responsabilidad: Eliminar o desactivar un tipo de movimiento
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from typing import Tuple, Optional


class EliminarTipoMovimientoUseCase:
    """Elimina o desactiva un tipo de movimiento"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, tipo_id: int) -> Tuple[bool, Optional[str]]:
        """
        Elimina un tipo de movimiento
        Si tiene movimientos asociados, solo lo desactiva
        
        Args:
            tipo_id: ID del tipo a eliminar
            
        Returns:
            tuple: (exito, mensaje)
        """
        try:
            # Verificar que el tipo existe
            query_existe = "SELECT id FROM tipos_movimientos WHERE id = %s"
            resultado, error = self.query_executor.ejecutar(query_existe, (tipo_id,))
            
            if error:
                return False, error
            
            if not resultado:
                return False, "Tipo de movimiento no encontrado"
            
            # Verificar si tiene movimientos asociados
            query_movimientos = "SELECT COUNT(*) as total FROM movimientos WHERE tipo_movimiento_id = %s"
            resultado, error = self.query_executor.ejecutar(query_movimientos, (tipo_id,))
            
            if error:
                return False, error
            
            tiene_movimientos = resultado[0]['total'] > 0
            
            if tiene_movimientos:
                # Solo desactivar
                query = "UPDATE tipos_movimientos SET activo = 0 WHERE id = %s"
                resultado, error = self.query_executor.ejecutar(query, (tipo_id,))
                
                if error:
                    return False, error
                
                return True, "Tipo desactivado (tiene movimientos asociados)"
            else:
                # Eliminar permanentemente
                query = "DELETE FROM tipos_movimientos WHERE id = %s"
                resultado, error = self.query_executor.ejecutar(query, (tipo_id,))
                
                if error:
                    return False, error
                
                return True, None
            
        except Exception as e:
            return False, f"Error al eliminar tipo de movimiento: {str(e)}"


# Instancia singleton
eliminar_tipo_movimiento_use_case = EliminarTipoMovimientoUseCase()
