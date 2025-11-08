"""
Caso de uso: Actualizar Departamento
Responsabilidad: Modificar un departamento existente
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.departamentos.models.departamento import Departamento


class ActualizarDepartamentoUseCase:
    """Actualiza un departamento"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, id_departamento, departamento: Departamento):
        """
        Actualiza un departamento
        
        Args:
            id_departamento: ID del departamento a actualizar
            departamento: Objeto con los nuevos datos
            
        Returns:
            tuple: (success, error)
        """
        try:
            # Verificar que no exista otro con el mismo num_departamento
            query_existe = """
                SELECT id FROM departamentos 
                WHERE num_departamento = %s AND id != %s
            """
            resultado, error = self.query_executor.ejecutar(
                query_existe, 
                (departamento.num_departamento, id_departamento)
            )
            
            if error:
                return False, error
            
            if resultado and len(resultado) > 0:
                return False, f"Ya existe otro departamento con el número {departamento.num_departamento}"
            
            # Actualizar
            query = """
                UPDATE departamentos
                SET num_departamento = %s,
                    nombre = %s,
                    nomenclatura = %s,
                    activo = %s
                WHERE id = %s
            """
            params = (
                departamento.num_departamento,
                departamento.nombre,
                departamento.nomenclatura,
                departamento.activo,
                id_departamento
            )
            
            _, error = self.query_executor.ejecutar(query, params)
            
            if error:
                return False, error
            
            return True, None
            
        except Exception as e:
            return False, f"Error al actualizar departamento: {str(e)}"


# Instancia singleton
actualizar_departamento_use_case = ActualizarDepartamentoUseCase()
