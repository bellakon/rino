"""
Caso de uso: Listar Tipos de Movimientos
Responsabilidad: Consultar tipos de movimientos con filtros
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.query_builder import QueryBuilder
from app.core.database.connection import db_connection
from app.features.movimientos.models.movimiento_models import TipoMovimiento
from typing import List, Optional


class ListarTiposMovimientosUseCase:
    """Lista tipos de movimientos con filtros opcionales"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(
        self,
        nomenclatura: Optional[str] = None,
        nombre: Optional[str] = None,
        categoria: Optional[str] = None,
        letra: Optional[str] = None,
        activo: Optional[bool] = None
    ) -> List[TipoMovimiento]:
        """
        Lista tipos de movimientos con filtros
        
        Args:
            nomenclatura: Filtro por nomenclatura (LIKE)
            nombre: Filtro por nombre (LIKE)
            categoria: Filtro exacto por categoría
            letra: Filtro exacto por letra
            activo: Filtro por estado activo
            
        Returns:
            List[TipoMovimiento]: Lista de tipos encontrados
        """
        try:
            base_query = """
                SELECT 
                    id, nomenclatura, nombre, descripcion, categoria, letra,
                    campos_personalizados, activo, created_at, updated_at
                FROM tipos_movimientos
            """
            
            builder = QueryBuilder(base_query)
            
            if nomenclatura:
                builder.add_filter("nomenclatura", f"%{nomenclatura}%", "LIKE")
            
            if nombre:
                builder.add_filter("nombre", f"%{nombre}%", "LIKE")
            
            if categoria:
                builder.add_filter("categoria", categoria)
            
            if letra:
                builder.add_filter("letra", letra.upper())
            
            if activo is not None:
                builder.add_filter("activo", 1 if activo else 0)
            
            # Construir query con parámetros
            query, params = builder.build()
            query += " ORDER BY letra, categoria, nombre"
            
            resultados, error = self.query_executor.ejecutar(query, params)
            
            if error:
                print(f"[ERROR LISTAR TIPOS] {error}")
                return []
            
            # Convertir resultados a objetos TipoMovimiento
            tipos = []
            for row in resultados:
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
                tipos.append(tipo)
            
            return tipos
            
        except Exception as e:
            print(f"[ERROR LISTAR TIPOS] {str(e)}")
            return []


# Instancia singleton
listar_tipos_movimientos_use_case = ListarTiposMovimientosUseCase()
