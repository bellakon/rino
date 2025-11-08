"""
Constructor de queries SQL
Responsabilidad única: construir queries con filtros dinámicos
Elimina duplicación de lógica de construcción de WHERE clauses
"""


class QueryBuilder:
    """Construye queries SQL dinámicamente con filtros"""
    
    def __init__(self, base_query):
        """
        Inicializa el builder con la query base
        
        Args:
            base_query (str): Query base (ej: "SELECT * FROM tabla")
        """
        self.query = base_query
        self.params = []
        self.has_where = 'WHERE' in base_query.upper()
    
    def add_filter(self, column, value, operator='='):
        """
        Agrega un filtro a la query
        
        Args:
            column (str): Nombre de la columna
            value: Valor a filtrar
            operator (str): Operador SQL (=, >, <, LIKE, etc.)
            
        Returns:
            self: Para encadenamiento
        """
        if value is not None:
            # Agregar WHERE o AND según corresponda
            if self.has_where:
                self.query += " AND"
            else:
                self.query += " WHERE"
                self.has_where = True
            
            self.query += f" {column} {operator} %s"
            self.params.append(value)
        
        return self
    
    def add_date_filter(self, column, fecha_desde=None, fecha_hasta=None):
        """
        Agrega filtros de rango de fechas
        
        Args:
            column (str): Nombre de la columna de fecha
            fecha_desde (str): Fecha inicio
            fecha_hasta (str): Fecha fin
            
        Returns:
            self: Para encadenamiento
        """
        if fecha_desde:
            self.add_filter(f"DATE({column})", fecha_desde, '>=')
        
        if fecha_hasta:
            self.add_filter(f"DATE({column})", fecha_hasta, '<=')
        
        return self
    
    def add_order_by(self, column, direction='ASC'):
        """
        Agrega ORDER BY
        
        Args:
            column (str): Columna para ordenar
            direction (str): ASC o DESC
            
        Returns:
            self: Para encadenamiento
        """
        self.query += f" ORDER BY {column} {direction}"
        return self
    
    def add_limit(self, limite, offset=None):
        """
        Agrega LIMIT y opcionalmente OFFSET
        
        Args:
            limite (int): Número de registros
            offset (int): Offset para paginación
            
        Returns:
            self: Para encadenamiento
        """
        self.query += " LIMIT %s"
        self.params.append(limite)
        
        if offset is not None:
            self.query += " OFFSET %s"
            self.params.append(offset)
        
        return self
    
    def build(self):
        """
        Construye la query final con sus parámetros
        
        Returns:
            tuple: (query, params)
        """
        return self.query, tuple(self.params)
