"""
Caso de uso: Crear Departamento
Responsabilidad: Insertar un nuevo departamento en la BD
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.departamentos.models.departamento import Departamento


class CrearDepartamentoUseCase:
    """Crea un nuevo departamento"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, departamento: Departamento):
        """
        Crea un departamento en la BD
        
        Args:
            departamento: Objeto Departamento
            
        Returns:
            tuple: (id_insertado, error)
        """
        try:
            # Verificar que no exista el num_departamento
            query_existe = "SELECT id FROM departamentos WHERE num_departamento = %s"
            resultado, error = self.query_executor.ejecutar(query_existe, (departamento.num_departamento,))
            
            if error:
                return None, error
            
            if resultado and len(resultado) > 0:
                return None, f"Ya existe un departamento con el número {departamento.num_departamento}"
            
            # Insertar
            query = """
                INSERT INTO departamentos (num_departamento, nombre, nomenclatura, activo)
                VALUES (%s, %s, %s, %s)
            """
            params = (
                departamento.num_departamento,
                departamento.nombre,
                departamento.nomenclatura,
                departamento.activo
            )
            
            id_insertado, error = self.query_executor.ejecutar(query, params)
            
            if error:
                return None, error
            
            return id_insertado, None
            
        except Exception as e:
            return None, f"Error al crear departamento: {str(e)}"


# Instancia singleton
crear_departamento_use_case = CrearDepartamentoUseCase()
