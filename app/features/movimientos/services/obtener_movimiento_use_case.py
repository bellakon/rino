"""
Caso de uso: Obtener Movimiento
Responsabilidad: Consultar un movimiento por ID con datos relacionados
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.movimientos.models.movimiento_models import Movimiento
from typing import Optional


class ObtenerMovimientoUseCase:
    """Obtiene un movimiento por ID con información relacionada"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, movimiento_id: int) -> Optional[Movimiento]:
        """
        Obtiene un movimiento por ID
        
        Args:
            movimiento_id: ID del movimiento
            
        Returns:
            Movimiento o None si no existe
        """
        try:
            query = """
                SELECT 
                    m.id, m.num_trabajador, m.tipo_movimiento_id,
                    m.fecha_inicio, m.fecha_fin, m.observaciones,
                    m.datos_personalizados, m.usuario_registro,
                    m.created_at, m.updated_at,
                    t.nombre as nombre_trabajador,
                    tm.nombre as nombre_tipo
                FROM movimientos m
                INNER JOIN trabajadores t ON m.num_trabajador = t.num_trabajador
                INNER JOIN tipos_movimientos tm ON m.tipo_movimiento_id = tm.id
                WHERE m.id = %s
            """
            
            resultado, error = self.query_executor.ejecutar(query, (movimiento_id,))
            
            if error or not resultado:
                return None
            
            row = resultado[0]
            
            movimiento = Movimiento(
                id=row['id'],
                num_trabajador=row['num_trabajador'],
                tipo_movimiento_id=row['tipo_movimiento_id'],
                fecha_inicio=row['fecha_inicio'],
                fecha_fin=row['fecha_fin'],
                observaciones=row['observaciones'],
                usuario_registro=row['usuario_registro'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            movimiento.set_datos_from_json(row['datos_personalizados'])
            
            # Agregar información adicional para la vista
            movimiento.nombre_trabajador = row['nombre_trabajador']
            movimiento.nombre_tipo = row['nombre_tipo']
            
            return movimiento
            
        except Exception as e:
            print(f"[ERROR OBTENER MOVIMIENTO] {str(e)}")
            return None


# Instancia singleton
obtener_movimiento_use_case = ObtenerMovimientoUseCase()
