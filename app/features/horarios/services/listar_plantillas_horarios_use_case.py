"""
Caso de uso: Listar Plantillas de Horarios
Responsabilidad: Obtener plantillas con filtros
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.query_builder import QueryBuilder
from app.core.database.connection import db_connection


class ListarPlantillasHorariosUseCase:
    """Lista plantillas de horarios con filtros"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, activo=None, buscar=None):
        """
        Lista plantillas de horarios
        
        Args:
            activo: Filtrar por estado (True/False)
            buscar: Texto para buscar en nombre o descripción
            
        Returns:
            tuple: (lista_plantillas, error)
        """
        try:
            builder = QueryBuilder("""
                SELECT 
                    id,
                    nombre_horario,
                    descripcion_horario,
                    lunes_entrada_1, lunes_salida_1, lunes_entrada_2, lunes_salida_2,
                    martes_entrada_1, martes_salida_1, martes_entrada_2, martes_salida_2,
                    miercoles_entrada_1, miercoles_salida_1, miercoles_entrada_2, miercoles_salida_2,
                    jueves_entrada_1, jueves_salida_1, jueves_entrada_2, jueves_salida_2,
                    viernes_entrada_1, viernes_salida_1, viernes_entrada_2, viernes_salida_2,
                    sabado_entrada_1, sabado_salida_1, sabado_entrada_2, sabado_salida_2,
                    domingo_entrada_1, domingo_salida_1, domingo_entrada_2, domingo_salida_2,
                    activo
                FROM plantillas_horarios
            """)
            
            if activo is not None:
                builder.add_filter('activo', activo)
            
            if buscar:
                builder.add_search(['nombre_horario', 'descripcion_horario'], buscar)
            
            builder.add_order_by('nombre_horario')
            
            query, params = builder.build()
            resultado, error = self.query_executor.ejecutar(query, params)
            
            if error:
                return [], error
            
            return resultado if resultado else [], None
            
        except Exception as e:
            return [], f"Error al listar plantillas: {str(e)}"


# Instancia singleton
listar_plantillas_horarios_use_case = ListarPlantillasHorariosUseCase()
