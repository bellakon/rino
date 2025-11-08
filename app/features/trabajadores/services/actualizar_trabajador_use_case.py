"""
Caso de uso: Actualizar trabajador
Responsabilidad: Actualizar datos de trabajador existente
"""
from app.core.database.query_executor import query_executor


class ActualizarTrabajadorUseCase:
    """Actualiza un trabajador existente en la base de datos"""
    
    def ejecutar(self, trabajador_id, num_trabajador, nombre, departamento=None, 
                 tipoPlaza=None, ingresoSEPfecha=None, activo=True, movimiento=None):
        """
        Actualiza un trabajador existente
        
        Args:
            trabajador_id: ID del trabajador a actualizar
            num_trabajador: Número único del trabajador
            nombre: Nombre completo
            departamento: Departamento (opcional)
            tipoPlaza: Tipo de plaza (opcional)
            ingresoSEPfecha: Fecha de ingreso (opcional)
            activo: Estado activo
            movimiento: Tipo de movimiento (opcional)
        
        Returns:
            tuple: (success boolean, error)
        """
        try:
            query = """
                UPDATE trabajadores 
                SET num_trabajador = %s,
                    nombre = %s,
                    departamento = %s,
                    tipoPlaza = %s,
                    ingresoSEPfecha = %s,
                    activo = %s,
                    movimiento = %s
                WHERE id = %s
            """
            
            params = (
                num_trabajador,
                nombre,
                departamento,
                tipoPlaza,
                ingresoSEPfecha if ingresoSEPfecha else None,
                1 if activo else 0,
                movimiento,
                trabajador_id
            )
            
            resultado, error = query_executor.ejecutar(query, params)
            
            if error:
                # Verificar si es error de duplicado
                if 'Duplicate entry' in str(error) or 'duplicate key' in str(error).lower():
                    return False, f"Ya existe otro trabajador con el número {num_trabajador}"
                return False, error
            
            return True, None
            
        except Exception as e:
            return False, f"Error al actualizar trabajador: {str(e)}"


# Instancia singleton
actualizar_trabajador_use_case = ActualizarTrabajadorUseCase()
