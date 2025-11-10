"""
Caso de uso: Editar Movimiento
Responsabilidad: Actualizar un movimiento existente
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.movimientos.models.movimiento_models import Movimiento
from typing import Tuple, Optional


class EditarMovimientoUseCase:
    """Edita un movimiento existente"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, movimiento_id: int, movimiento: Movimiento) -> Tuple[bool, Optional[str]]:
        """
        Edita un movimiento
        
        Args:
            movimiento_id: ID del movimiento a editar
            movimiento: Objeto Movimiento con nuevos datos
            
        Returns:
            tuple: (exito, mensaje_error)
        """
        try:
            # Validar modelo
            valido, mensaje = movimiento.validar()
            if not valido:
                return False, mensaje
            
            # Verificar que el movimiento existe
            query_existe = "SELECT id FROM movimientos WHERE id = %s"
            resultado, error = self.query_executor.ejecutar(query_existe, (movimiento_id,))
            
            if error:
                return False, error
            
            if not resultado:
                return False, "Movimiento no encontrado"
            
            # Verificar que el trabajador existe
            query_trabajador = "SELECT num_trabajador FROM trabajadores WHERE num_trabajador = %s"
            resultado, error = self.query_executor.ejecutar(query_trabajador, (movimiento.num_trabajador,))
            
            if error:
                return False, error
            
            if not resultado:
                return False, f"El trabajador {movimiento.num_trabajador} no existe"
            
            # Verificar que el tipo de movimiento existe y está activo
            query_tipo = "SELECT id FROM tipos_movimientos WHERE id = %s AND activo = 1"
            resultado, error = self.query_executor.ejecutar(query_tipo, (movimiento.tipo_movimiento_id,))
            
            if error:
                return False, error
            
            if not resultado:
                return False, "El tipo de movimiento no existe o está inactivo"
            
            # Actualizar
            query = """
                UPDATE movimientos
                SET num_trabajador = %s,
                    tipo_movimiento_id = %s,
                    fecha_inicio = %s,
                    fecha_fin = %s,
                    observaciones = %s,
                    datos_personalizados = %s
                WHERE id = %s
            """
            params = (
                movimiento.num_trabajador,
                movimiento.tipo_movimiento_id,
                movimiento.fecha_inicio,
                movimiento.fecha_fin,
                movimiento.observaciones,
                movimiento.get_datos_json(),
                movimiento_id
            )
            
            resultado, error = self.query_executor.ejecutar(query, params)
            
            if error:
                return False, error
            
            return True, None
            
        except Exception as e:
            return False, f"Error al editar movimiento: {str(e)}"


# Instancia singleton
editar_movimiento_use_case = EditarMovimientoUseCase()
