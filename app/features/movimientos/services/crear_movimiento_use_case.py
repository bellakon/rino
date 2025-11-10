"""
Caso de uso: Crear Movimiento
Responsabilidad: Insertar un nuevo movimiento en la BD
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.movimientos.models.movimiento_models import Movimiento
from typing import Tuple, Optional


class CrearMovimientoUseCase:
    """Crea un nuevo movimiento"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, movimiento: Movimiento) -> Tuple[Optional[int], Optional[str]]:
        """
        Crea un movimiento en la BD
        
        Args:
            movimiento: Objeto Movimiento
            
        Returns:
            tuple: (id_insertado, error)
        """
        try:
            # Validar modelo
            valido, mensaje = movimiento.validar()
            if not valido:
                return None, mensaje
            
            # Verificar que el trabajador existe (puede estar inactivo)
            query_trabajador = "SELECT num_trabajador FROM trabajadores WHERE num_trabajador = %s"
            resultado, error = self.query_executor.ejecutar(query_trabajador, (movimiento.num_trabajador,))
            
            if error:
                return None, error
            
            if not resultado:
                return None, f"El trabajador {movimiento.num_trabajador} no existe"
            
            # Verificar que el tipo de movimiento existe y está activo
            query_tipo = "SELECT id FROM tipos_movimientos WHERE id = %s AND activo = 1"
            resultado, error = self.query_executor.ejecutar(query_tipo, (movimiento.tipo_movimiento_id,))
            
            if error:
                return None, error
            
            if not resultado:
                return None, "El tipo de movimiento no existe o está inactivo"
            
            # Insertar
            query = """
                INSERT INTO movimientos 
                (num_trabajador, tipo_movimiento_id, fecha_inicio, fecha_fin, 
                 observaciones, datos_personalizados, usuario_registro)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                movimiento.num_trabajador,
                movimiento.tipo_movimiento_id,
                movimiento.fecha_inicio,
                movimiento.fecha_fin,
                movimiento.observaciones,
                movimiento.get_datos_json(),
                movimiento.usuario_registro
            )
            
            resultado, error = self.query_executor.ejecutar(query, params)
            
            if error:
                return None, error
            
            # Obtener ID insertado
            query_id = "SELECT LAST_INSERT_ID() as id"
            resultado_id, error = self.query_executor.ejecutar(query_id)
            
            if error or not resultado_id:
                return None, "Error al obtener ID insertado"
            
            movimiento_id = resultado_id[0]['id']
            print(f"[CREAR MOVIMIENTO] ID={movimiento_id}, Trabajador={movimiento.num_trabajador}")
            
            return movimiento_id, None
            
        except Exception as e:
            return None, f"Error al crear movimiento: {str(e)}"


# Instancia singleton
crear_movimiento_use_case = CrearMovimientoUseCase()
