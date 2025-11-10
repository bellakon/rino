"""
Caso de uso: Obtener trabajadores
Responsabilidad: Consultar trabajadores con filtros y paginación
"""
from app.core.database.query_executor import query_executor
from app.features.trabajadores.models import Trabajador
import math


class ObtenerTrabajadoresUseCase:
    """Obtiene trabajadores de la base de datos con filtros y paginación"""
    
    def ejecutar(self, num_trabajador=None, tipoPlaza=None, departamento_id=None, orden_por=None, page=1, per_page=50):
        """
        Ejecuta SELECT con filtros y paginación, convierte a modelos Trabajador
        
        Args:
            num_trabajador: Filtro opcional por número de trabajador
            tipoPlaza: Filtro opcional por tipo de plaza
            departamento_id: Filtro opcional por departamento
            orden_por: Campo para ordenar (num_trabajador, nombre, departamento)
            page: Número de página (default: 1)
            per_page: Registros por página (default: 50)
        
        Returns:
            tuple: (dict con trabajadores, total, page, per_page, error)
        """
        # Construir WHERE clauses
        where_clauses = []
        params = []
        
        if num_trabajador:
            where_clauses.append("t.num_trabajador = %s")
            params.append(num_trabajador)
        
        if tipoPlaza:
            where_clauses.append("t.tipoPlaza = %s")
            params.append(tipoPlaza)
        
        if departamento_id:
            where_clauses.append("t.departamento_id = %s")
            params.append(departamento_id)
        
        where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        # Determinar ORDER BY
        order_by_map = {
            'num_trabajador': 't.num_trabajador ASC',
            'nombre': 't.nombre ASC',
            'departamento': 'd.nombre ASC, t.num_trabajador ASC'
        }
        order_by_sql = order_by_map.get(orden_por, 't.num_trabajador ASC')
        
        # Obtener total de registros
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM trabajadores t
            LEFT JOIN departamentos d ON t.departamento_id = d.id
            {where_sql}
        """
        count_result, error = query_executor.ejecutar(count_query, tuple(params) if params else None)
        
        if error:
            return None, error
        
        total = count_result[0]['total'] if count_result else 0
        
        # Calcular offset
        offset = (page - 1) * per_page
        
        # Obtener registros paginados con nombre del departamento
        query = f"""
            SELECT 
                t.*,
                d.nombre as departamento_nombre
            FROM trabajadores t
            LEFT JOIN departamentos d ON t.departamento_id = d.id
            {where_sql}
            ORDER BY {order_by_sql}
            LIMIT %s OFFSET %s
        """
        params.extend([per_page, offset])
        
        registros, error = query_executor.ejecutar(query, tuple(params))
        
        if error:
            return None, error
        
        # Convertir diccionarios a objetos Trabajador
        trabajadores = [Trabajador.from_dict(reg) for reg in registros]
        
        return {
            'trabajadores': trabajadores,
            'total': total,
            'page': page,
            'per_page': per_page
        }, None


# Instancia singleton
obtener_trabajadores_use_case = ObtenerTrabajadoresUseCase()
