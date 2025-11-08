"""
Caso de uso: Listar Departamentos
Responsabilidad: Consultar todos los departamentos
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.query_builder import QueryBuilder
from app.core.database.connection import db_connection


class ListarDepartamentosUseCase:
    """Lista departamentos con filtros opcionales"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, activo=None, buscar=None):
        """
        Lista departamentos
        
        Args:
            activo: Filtrar por estado (True/False)
            buscar: Texto para buscar en nombre o nomenclatura
            
        Returns:
            tuple: (lista_departamentos, error)
        """
        try:
            builder = QueryBuilder("""
                SELECT 
                    id,
                    num_departamento,
                    nombre,
                    nomenclatura,
                    activo
                FROM departamentos
            """)
            
            if activo is not None:
                builder.add_filter('activo', activo)
            
            if buscar:
                builder.add_search(['nombre', 'nomenclatura'], buscar)
            
            builder.add_order_by('nombre')
            
            query, params = builder.build()
            resultado, error = self.query_executor.ejecutar(query, params)
            
            if error:
                return [], error
            
            return resultado if resultado else [], None
            
        except Exception as e:
            return [], f"Error al listar departamentos: {str(e)}"


# Instancia singleton
listar_departamentos_use_case = ListarDepartamentosUseCase()
