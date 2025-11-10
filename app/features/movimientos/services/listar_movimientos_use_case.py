"""
Caso de uso: Listar Movimientos
Responsabilidad: Consultar movimientos con filtros
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.query_builder import QueryBuilder
from app.core.database.connection import db_connection
from app.features.movimientos.models.movimiento_models import Movimiento
from typing import List, Optional
from datetime import date


class ListarMovimientosUseCase:
    """Lista movimientos con filtros opcionales"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(
        self,
        num_trabajador: Optional[int] = None,
        tipo_movimiento_id: Optional[int] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        nombre_trabajador: Optional[str] = None
    ) -> List[Movimiento]:
        """
        Lista movimientos con filtros
        
        Args:
            num_trabajador: Filtro por número de trabajador
            tipo_movimiento_id: Filtro por tipo de movimiento
            fecha_inicio: Filtro por fecha inicio (desde)
            fecha_fin: Filtro por fecha fin (hasta)
            nombre_trabajador: Filtro por nombre de trabajador (LIKE)
            
        Returns:
            List[Movimiento]: Lista de movimientos encontrados
        """
        try:
            base_query = """
                SELECT 
                    m.id, m.num_trabajador, m.tipo_movimiento_id,
                    m.fecha_inicio, m.fecha_fin, m.observaciones,
                    m.datos_personalizados, m.usuario_registro,
                    m.created_at, m.updated_at,
                    t.nombre as trabajador_nombre,
                    tm.nomenclatura as tipo_nomenclatura,
                    tm.nombre as tipo_nombre
                FROM movimientos m
                INNER JOIN trabajadores t ON m.num_trabajador = t.num_trabajador
                INNER JOIN tipos_movimientos tm ON m.tipo_movimiento_id = tm.id
            """
            
            builder = QueryBuilder(base_query)
            
            if num_trabajador:
                builder.add_filter("m.num_trabajador", num_trabajador)
            
            if tipo_movimiento_id:
                builder.add_filter("m.tipo_movimiento_id", tipo_movimiento_id)
            
            if fecha_inicio:
                builder.add_filter("m.fecha_inicio", fecha_inicio, ">=")
            
            if fecha_fin:
                builder.add_filter("m.fecha_fin", fecha_fin, "<=")
            
            if nombre_trabajador:
                builder.add_filter("t.nombre", f"%{nombre_trabajador}%", "LIKE")
            
            # Construir query con parámetros
            query, params = builder.build()
            query += " ORDER BY m.fecha_inicio DESC, m.id DESC"
            
            resultados, error = self.query_executor.ejecutar(query, params)
            
            if error:
                print(f"[ERROR LISTAR MOVIMIENTOS] {error}")
                return []
            
            # Convertir resultados a objetos Movimiento
            movimientos = []
            for row in resultados:
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
                movimiento.trabajador_nombre = row['trabajador_nombre']
                movimiento.tipo_nomenclatura = row['tipo_nomenclatura']
                movimiento.tipo_nombre = row['tipo_nombre']
                
                movimientos.append(movimiento)
            
            return movimientos
            
        except Exception as e:
            print(f"[ERROR LISTAR MOVIMIENTOS] {str(e)}")
            return []


# Instancia singleton
listar_movimientos_use_case = ListarMovimientosUseCase()
