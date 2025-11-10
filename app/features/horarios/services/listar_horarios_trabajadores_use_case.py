"""
Caso de uso: Listar Horarios de Trabajadores
Responsabilidad: Obtener asignaciones con información completa
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.query_builder import QueryBuilder
from app.core.database.connection import db_connection


class ListarHorariosTrabajadoresUseCase:
    """Lista asignaciones de horarios a trabajadores"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, semestre=None, num_trabajador=None, estado_asignacion=None):
        """
        Lista asignaciones de horarios
        
        Args:
            semestre: Filtrar por semestre
            num_trabajador: Filtrar por trabajador
            estado_asignacion: Filtrar por estado (activo/inactivo)
            
        Returns:
            tuple: (lista_horarios, error)
        """
        try:
            builder = QueryBuilder("""
                SELECT 
                    ht.id,
                    ht.num_trabajador,
                    t.nombre as nombre_completo,
                    d.nombre as departamento_nombre,
                    ht.plantilla_horario_id,
                    ph.nombre_horario,
                    ph.descripcion_horario,
                    ht.fecha_inicio_asignacion,
                    ht.fecha_fin_asignacion,
                    ht.semestre,
                    ht.estado_asignacion,
                    ht.activo_asignacion
                FROM horarios_trabajadores ht
                INNER JOIN trabajadores t ON ht.num_trabajador = t.num_trabajador
                LEFT JOIN departamentos d ON t.departamento_id = d.id
                INNER JOIN plantillas_horarios ph ON ht.plantilla_horario_id = ph.id
            """)
            
            if semestre:
                builder.add_filter('ht.semestre', semestre)
            
            if num_trabajador:
                builder.add_filter('ht.num_trabajador', num_trabajador)
            
            if estado_asignacion:
                builder.add_filter('ht.estado_asignacion', estado_asignacion)
            
            builder.add_order_by('t.nombre')
            
            query, params = builder.build()
            resultado, error = self.query_executor.ejecutar(query, params)
            
            if error:
                return [], error
            
            return resultado if resultado else [], None
            
        except Exception as e:
            return [], f"Error al listar horarios de trabajadores: {str(e)}"


# Instancia singleton
listar_horarios_trabajadores_use_case = ListarHorariosTrabajadoresUseCase()
