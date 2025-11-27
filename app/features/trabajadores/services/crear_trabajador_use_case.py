"""
Caso de uso: Crear trabajador
Responsabilidad: Insertar nuevo trabajador en la base de datos
"""
from app.core.database.query_executor import query_executor


class CrearTrabajadorUseCase:
    """Crea un nuevo trabajador en la base de datos"""
    
    def ejecutar(self, num_trabajador, nombre, email=None, departamento=None, tipoPlaza=None, 
                 ingresoSEPfecha=None, activo=True, movimiento=None):
        """
        Inserta un nuevo trabajador
        
        Args:
            num_trabajador: Número único del trabajador
            nombre: Nombre completo
            email: Correo electrónico (opcional)
            departamento: Departamento (opcional)
            tipoPlaza: Tipo de plaza (opcional)
            ingresoSEPfecha: Fecha de ingreso (opcional)
            activo: Estado activo (default: True)
            movimiento: Tipo de movimiento (opcional)
        
        Returns:
            tuple: (trabajador_id, error)
        """
        try:
            query = """
                INSERT INTO trabajadores 
                (num_trabajador, nombre, email, departamento, tipoPlaza, ingresoSEPfecha, activo, movimiento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            params = (
                num_trabajador,
                nombre,
                email,
                departamento,
                tipoPlaza,
                ingresoSEPfecha if ingresoSEPfecha else None,
                1 if activo else 0,
                movimiento
            )
            
            resultado, error = query_executor.ejecutar(query, params)
            
            if error:
                # Verificar si es error de duplicado
                if 'Duplicate entry' in str(error) or 'duplicate key' in str(error).lower():
                    return None, f"Ya existe un trabajador con el número {num_trabajador}"
                return None, error
            
            # Obtener el ID insertado
            query_id = "SELECT LAST_INSERT_ID() as id"
            id_result, error = query_executor.ejecutar(query_id)
            
            if error:
                return None, error
            
            trabajador_id = id_result[0]['id'] if id_result else None
            
            return trabajador_id, None
            
        except Exception as e:
            return None, f"Error al crear trabajador: {str(e)}"


# Instancia singleton
crear_trabajador_use_case = CrearTrabajadorUseCase()
