"""
Caso de uso: Cambiar Departamento de Trabajador
Responsabilidad: Actualizar el departamento_id de un trabajador
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection


class CambiarDepartamentoTrabajadorUseCase:
    """Cambia el departamento de un trabajador"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, trabajador_id, departamento_id):
        """
        Cambia el departamento de un trabajador
        
        Args:
            trabajador_id: ID del trabajador
            departamento_id: ID del nuevo departamento (puede ser None para "SIN ASIGNAR")
            
        Returns:
            tuple: (success, error)
        """
        try:
            # Si departamento_id es None o 0, asignar a "SIN ASIGNAR" (id=1)
            if not departamento_id or departamento_id == 0:
                departamento_id = 1
            
            # Verificar que el departamento existe
            query_departamento = "SELECT id FROM departamentos WHERE id = %s"
            resultado, error = self.query_executor.ejecutar(query_departamento, (departamento_id,))
            
            if error:
                return False, error
            
            if not resultado:
                return False, f"El departamento con ID {departamento_id} no existe"
            
            # Actualizar departamento del trabajador
            query = """
                UPDATE trabajadores 
                SET departamento_id = %s 
                WHERE id = %s
            """
            _, error = self.query_executor.ejecutar(query, (departamento_id, trabajador_id))
            
            if error:
                return False, error
            
            return True, None
            
        except Exception as e:
            return False, f"Error al cambiar departamento: {str(e)}"


# Instancia singleton
cambiar_departamento_trabajador_use_case = CambiarDepartamentoTrabajadorUseCase()
