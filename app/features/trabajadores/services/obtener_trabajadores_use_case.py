"""
Caso de uso: Obtener trabajadores
Responsabilidad: Consultar trabajadores con filtros y paginación
"""
from app.core.database.query_executor import query_executor
from app.features.trabajadores.models import Trabajador
import math


class ObtenerTrabajadoresUseCase:
    """Obtiene trabajadores de la base de datos con filtros y paginación"""
    
    def ejecutar(self, num_trabajador=None, tipoPlaza=None, page=1, per_page=50):
        """
        Ejecuta SELECT con filtros y paginación, convierte a modelos Trabajador
        
        Args:
            num_trabajador: Filtro opcional por número de trabajador
            tipoPlaza: Filtro opcional por tipo de plaza
            page: Número de página (default: 1)
            per_page: Registros por página (default: 50)
        
        Returns:
            tuple: (dict con trabajadores, total, page, per_page, error)
        """
        # Construir WHERE clauses
        where_clauses = []
        params = []
        
        if num_trabajador:
            where_clauses.append("num_trabajador = %s")
            params.append(num_trabajador)
        
        if tipoPlaza:
            where_clauses.append("tipoPlaza = %s")
            params.append(tipoPlaza)
        
        where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        # Obtener total de registros
        count_query = f"SELECT COUNT(*) as total FROM trabajadores{where_sql}"
        count_result, error = query_executor.ejecutar(count_query, tuple(params) if params else None)
        
        if error:
            return None, error
        
        total = count_result[0]['total'] if count_result else 0
        
        # Calcular offset
        offset = (page - 1) * per_page
        
        # Obtener registros paginados
        query = f"""
            SELECT * FROM trabajadores
            {where_sql}
            ORDER BY num_trabajador ASC
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
