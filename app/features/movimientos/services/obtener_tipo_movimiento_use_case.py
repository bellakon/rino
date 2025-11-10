"""
Caso de uso: Obtener Tipo de Movimiento
Responsabilidad: Consultar un tipo de movimiento por ID
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.movimientos.models.movimiento_models import TipoMovimiento
from typing import Optional


class ObtenerTipoMovimientoUseCase:
    """Obtiene un tipo de movimiento por ID"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, tipo_id: int) -> Optional[TipoMovimiento]:
        """
        Obtiene un tipo de movimiento por ID
        
        Args:
            tipo_id: ID del tipo de movimiento
            
        Returns:
            TipoMovimiento o None si no existe
        """
        try:
            query = """
                SELECT 
                    id, nomenclatura, nombre, descripcion, categoria, letra,
                    campos_personalizados, activo, created_at, updated_at
                FROM tipos_movimientos
                WHERE id = %s
            """
            
            resultado, error = self.query_executor.ejecutar(query, (tipo_id,))
            
            if error or not resultado:
                return None
            
            row = resultado[0]
            
            tipo = TipoMovimiento(
                id=row['id'],
                nomenclatura=row['nomenclatura'],
                nombre=row['nombre'],
                descripcion=row['descripcion'],
                categoria=row['categoria'],
                letra=row['letra'],
                activo=bool(row['activo']),
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            tipo.set_campos_from_json(row['campos_personalizados'])
            
            return tipo
            
        except Exception as e:
            print(f"[ERROR OBTENER TIPO] {str(e)}")
            return None


# Instancia singleton
obtener_tipo_movimiento_use_case = ObtenerTipoMovimientoUseCase()
