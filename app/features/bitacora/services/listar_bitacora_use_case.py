"""
Caso de uso: Listar Bitácora
Consulta registros de bitácora con filtros
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.query_builder import QueryBuilder
from app.core.database.connection import db_connection
from app.features.bitacora.models.bitacora_models import BitacoraRecord
from datetime import date
from typing import List, Optional


class ListarBitacoraUseCase:
    """Lista registros de bitácora con filtros"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(
        self,
        num_trabajador: Optional[int] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        codigo_incidencia: Optional[str] = None
    ) -> List[BitacoraRecord]:
        """
        Lista registros de bitácora
        
        Args:
            num_trabajador: Filtro por trabajador
            fecha_inicio: Filtro desde fecha
            fecha_fin: Filtro hasta fecha
            codigo_incidencia: Filtro por código (A, F, R+, etc.)
            
        Returns:
            Lista de registros de bitácora
        """
        try:
            base_query = """
                SELECT 
                    id, num_trabajador, departamento, nombre_trabajador,
                    fecha, turno_id, horario_texto,
                    codigo_incidencia, tipo_movimiento, movimiento_id,
                    checada1, checada2, checada3, checada4,
                    minutos_retardo, horas_trabajadas, descripcion_incidencia,
                    fecha_procesamiento, procesado_por,
                    created_at, updated_at
                FROM bitacora
            """
            
            builder = QueryBuilder(base_query)
            
            if num_trabajador:
                builder.add_filter("num_trabajador", num_trabajador)
            
            if fecha_inicio:
                builder.add_filter("fecha", fecha_inicio, ">=")
            
            if fecha_fin:
                builder.add_filter("fecha", fecha_fin, "<=")
            
            if codigo_incidencia:
                builder.add_filter("codigo_incidencia", codigo_incidencia)
            
            query, params = builder.build()
            query += " ORDER BY fecha DESC, num_trabajador"
            
            resultados, error = self.query_executor.ejecutar(query, params)
            
            if error:
                print(f"[ERROR LISTAR BITACORA] {error}")
                return []
            
            # Convertir a objetos BitacoraRecord
            registros = []
            for row in resultados:
                registro = BitacoraRecord(
                    id=row['id'],
                    num_trabajador=row['num_trabajador'],
                    departamento=row['departamento'],
                    nombre_trabajador=row['nombre_trabajador'],
                    fecha=row['fecha'],
                    turno_id=row['turno_id'],
                    horario_texto=row['horario_texto'],
                    codigo_incidencia=row['codigo_incidencia'],
                    tipo_movimiento=row['tipo_movimiento'],
                    movimiento_id=row['movimiento_id'],
                    checada1=row['checada1'],
                    checada2=row['checada2'],
                    checada3=row['checada3'],
                    checada4=row['checada4'],
                    minutos_retardo=row['minutos_retardo'],
                    horas_trabajadas=row['horas_trabajadas'],
                    descripcion_incidencia=row['descripcion_incidencia'],
                    fecha_procesamiento=row['fecha_procesamiento'],
                    procesado_por=row['procesado_por'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                registros.append(registro)
            
            return registros
            
        except Exception as e:
            print(f"[ERROR LISTAR BITACORA] {str(e)}")
            return []


# Instancia singleton
listar_bitacora_use_case = ListarBitacoraUseCase()
