"""
Caso de uso: Obtener asistencias
Responsabilidad: Ejecutar SELECT y convertir resultados a modelos
"""
from app.core.database.query_executor import query_executor
from app.features.asistencias.models import Asistencia


class ObtenerAsistenciasUseCase:
    """Obtiene asistencias de la base de datos y las convierte a modelos"""
    
    def ejecutar(self, num_trabajador=None, nombre_trabajador=None, checador=None, fecha_inicio=None, fecha_fin=None, 
                 page=1, per_page=50, order_by='id', order_dir='desc'):
        """
        Ejecuta SELECT con filtros, ordenación y paginación, convierte a modelos Asistencia
        
        Args:
            num_trabajador: Filtro opcional por número de trabajador
            nombre_trabajador: Filtro opcional por nombre del trabajador
            checador: Filtro opcional por checador (serial)
            fecha_inicio: Filtro opcional por fecha inicial (YYYY-MM-DD)
            fecha_fin: Filtro opcional por fecha final (YYYY-MM-DD)
            page: Número de página (default: 1)
            per_page: Registros por página (default: 50)
            order_by: Campo por el cual ordenar (default: 'id')
            order_dir: Dirección de ordenación 'asc' o 'desc' (default: 'desc')
        
        Returns:
            tuple: (dict con asistencias, total, page, per_page, error)
        """
        # Construir WHERE clauses
        where_clauses = []
        params = []
        
        if num_trabajador:
            where_clauses.append("num_trabajador = %s")
            params.append(num_trabajador)
        
        if nombre_trabajador:
            where_clauses.append("nombre LIKE %s")
            params.append(f"%{nombre_trabajador}%")
        
        if checador:
            where_clauses.append("checador LIKE %s")
            params.append(f"%{checador}%")
        
        # Filtros de fecha
        if fecha_inicio and fecha_fin:
            # Rango de fechas
            where_clauses.append("fecha BETWEEN %s AND %s")
            params.append(fecha_inicio)
            params.append(fecha_fin)
        elif fecha_inicio:
            # Solo fecha inicial (búsqueda por fecha específica)
            where_clauses.append("fecha = %s")
            params.append(fecha_inicio)
        
        where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        # Validar y construir ORDER BY
        columnas_permitidas = {
            'id': 'id',
            'num_trabajador': 'num_trabajador',
            'nombre': 'nombre',
            'fecha': 'fecha',
            'hora': 'hora',
            'checador': 'checador'
        }
        
        order_column = columnas_permitidas.get(order_by, 'id')
        order_direction = 'ASC' if order_dir == 'asc' else 'DESC'
        order_sql = f"ORDER BY {order_column} {order_direction}"
        
        # Si se ordena por algo diferente a fecha/hora, agregar fecha DESC, hora DESC como secundario
        if order_by not in ['fecha', 'hora']:
            order_sql += ", fecha DESC, hora DESC"
        
        # Obtener total de registros
        count_query = f"SELECT COUNT(*) as total FROM asistencias{where_sql}"
        count_result, error = query_executor.ejecutar(count_query, tuple(params) if params else None)
        
        if error:
            return None, error
        
        total = count_result[0]['total'] if count_result else 0
        
        # Calcular offset
        offset = (page - 1) * per_page
        
        # Obtener registros paginados con ordenación
        query = f"""
            SELECT * FROM asistencias
            {where_sql}
            {order_sql}
            LIMIT %s OFFSET %s
        """
        params.extend([per_page, offset])
        
        registros, error = query_executor.ejecutar(query, tuple(params))
        
        if error:
            return None, error
        
        # Convertir diccionarios a objetos Asistencia
        asistencias = [Asistencia.from_dict(reg) for reg in registros]
        
        return {
            'asistencias': asistencias,
            'total': total,
            'page': page,
            'per_page': per_page
        }, None


# Instancia singleton
obtener_asistencias_use_case = ObtenerAsistenciasUseCase()
