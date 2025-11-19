"""
Caso de uso: Obtener Movimiento del Día
Verifica si un trabajador tiene un movimiento (justificación/licencia) en una fecha específica
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from datetime import date
from typing import Optional, Dict


class ObtenerMovimientoDiaUseCase:
    """Verifica si hay un movimiento que justifica un día"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(
        self,
        num_trabajador: int,
        fecha: date
    ) -> tuple[Optional[Dict], Optional[str]]:
        """
        Verifica si existe un movimiento que cubra la fecha
        
        Args:
            num_trabajador: Número del trabajador
            fecha: Fecha a verificar
            
        Returns:
            tuple: (diccionario con movimiento o None, error)
        """
        try:
            query = """
                SELECT 
                    m.id,
                    m.tipo_movimiento_id,
                    m.fecha_inicio,
                    m.fecha_fin,
                    m.observaciones,
                    tm.nomenclatura,
                    tm.nombre as tipo_nombre,
                    tm.categoria,
                    tm.letra
                FROM movimientos m
                INNER JOIN tipos_movimientos tm ON m.tipo_movimiento_id = tm.id
                WHERE m.num_trabajador = %s
                AND %s BETWEEN m.fecha_inicio AND m.fecha_fin
                LIMIT 1
            """
            
            resultados, error = self.query_executor.ejecutar(
                query, 
                (num_trabajador, fecha)
            )
            
            if error:
                return None, f"Error al buscar movimientos: {error}"
            
            if not resultados:
                return None, None  # No hay movimiento, no es error
            
            movimiento = resultados[0]
            
            return {
                'tiene_movimiento': True,
                'movimiento_id': movimiento['id'],
                'tipo_movimiento': movimiento['nomenclatura'],  # Nomenclatura (OT, COM001, etc.)
                'tipo_nombre': movimiento['tipo_nombre'],
                'categoria': movimiento['categoria'],
                'letra': movimiento['letra'],  # Letra para código de incidencia (J, L, A)
                'fecha_inicio': movimiento['fecha_inicio'],
                'fecha_fin': movimiento['fecha_fin'],
                'observaciones': movimiento['observaciones']
            }, None
            
        except Exception as e:
            return None, f"Error al obtener movimiento del día: {str(e)}"


# Instancia singleton
obtener_movimiento_dia_use_case = ObtenerMovimientoDiaUseCase()
