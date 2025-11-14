"""
Caso de uso: Obtener Checadas del Día
Obtiene todas las checadas de un trabajador en un día específico
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from datetime import date, time
from typing import Optional, List, Dict


class ObtenerChecadasDiaUseCase:
    """Obtiene checadas de un trabajador en un día"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(
        self,
        num_trabajador: int,
        fecha: date
    ) -> tuple[Optional[Dict], Optional[str]]:
        """
        Obtiene las checadas del día y las organiza por entrada/salida
        
        Args:
            num_trabajador: Número del trabajador
            fecha: Fecha a consultar
            
        Returns:
            tuple: (diccionario con checadas organizadas, error)
        """
        try:
            # Obtener TODAS las checadas del día ordenadas por hora
            query = """
                SELECT 
                    id,
                    num_trabajador,
                    fecha,
                    hora
                FROM asistencias
                WHERE num_trabajador = %s
                AND fecha = %s
                ORDER BY hora ASC
            """
            
            resultados, error = self.query_executor.ejecutar(
                query, 
                (num_trabajador, fecha)
            )
            
            if error:
                return None, f"Error al obtener checadas: {error}"
            
            # Si no hay checadas
            if not resultados:
                return {
                    'tiene_checadas': False,
                    'num_checadas': 0,
                    'checada1': None,  # Entrada 1
                    'checada2': None,  # Salida 1
                    'checada3': None,  # Entrada 2 (horario mixto)
                    'checada4': None   # Salida 2 (horario mixto)
                }, None
            
            # Organizar checadas (asumimos entrada-salida-entrada-salida)
            checadas_organizadas = {
                'tiene_checadas': True,
                'num_checadas': len(resultados),
                'checada1': resultados[0]['hora'] if len(resultados) >= 1 else None,
                'checada2': resultados[1]['hora'] if len(resultados) >= 2 else None,
                'checada3': resultados[2]['hora'] if len(resultados) >= 3 else None,
                'checada4': resultados[3]['hora'] if len(resultados) >= 4 else None,
                'todas_las_checadas': [r['hora'] for r in resultados]
            }
            
            return checadas_organizadas, None
            
        except Exception as e:
            return None, f"Error al obtener checadas del día: {str(e)}"


# Instancia singleton
obtener_checadas_dia_use_case = ObtenerChecadasDiaUseCase()
