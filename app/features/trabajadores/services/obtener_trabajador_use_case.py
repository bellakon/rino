"""
Caso de uso: Obtener información del trabajador
"""
from typing import Optional, Dict
from app.core.database.query_executor import query_executor


class ObtenerTrabajadorUseCase:
    """Obtiene información completa de un trabajador"""
    
    def __init__(self):
        self.query_executor = query_executor
    
    def ejecutar(self, num_trabajador: int) -> tuple[Optional[Dict], Optional[str]]:
        """
        Obtiene información del trabajador por número
        
        Args:
            num_trabajador: Número del trabajador
            
        Returns:
            tuple: (dict con datos del trabajador, error)
        """
        try:
            query = """
                SELECT 
                    num_trabajador,
                    nombre,
                    email,
                    departamento_id,
                    activo
                FROM trabajadores 
                WHERE num_trabajador = %s
            """
            
            resultado, error = self.query_executor.ejecutar(query, (num_trabajador,))
            
            if error:
                return None, f"Error al obtener trabajador: {error}"
            
            if not resultado:
                return None, f"No se encontró trabajador con número {num_trabajador}"
            
            return resultado[0], None
            
        except Exception as e:
            return None, f"Error inesperado: {str(e)}"


# Instancia singleton
obtener_trabajador_use_case = ObtenerTrabajadorUseCase()
