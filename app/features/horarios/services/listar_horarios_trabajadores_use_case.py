"""
Caso de uso: Listar Horarios de Trabajadores
Responsabilidad: Obtener asignaciones con información completa
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection


class ListarHorariosTrabajadoresUseCase:
    """Lista asignaciones de horarios a trabajadores"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, semestre=None, num_trabajador=None, nombre_trabajador=None, estado_asignacion=None):
        """
        Lista asignaciones de horarios
        
        Args:
            semestre: Filtrar por semestre
            num_trabajador: Filtrar por número de trabajador
            nombre_trabajador: Filtrar por nombre de trabajador (búsqueda parcial)
            estado_asignacion: Filtrar por estado (activo/inactivo)
            
        Returns:
            tuple: (lista_horarios, error)
        """
        try:
            print(f"[LISTAR ASIGNACIONES] Filtros: semestre={semestre}, num_trabajador={num_trabajador}, nombre={nombre_trabajador}, estado={estado_asignacion}")
            
            # Query base
            query = """
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
            """
            
            where_clauses = []
            params = []
            
            if semestre:
                where_clauses.append("ht.semestre = %s")
                params.append(semestre)
            
            if num_trabajador:
                where_clauses.append("ht.num_trabajador = %s")
                params.append(num_trabajador)
            
            if nombre_trabajador:
                where_clauses.append("t.nombre LIKE %s")
                params.append(f"%{nombre_trabajador}%")
            
            if estado_asignacion:
                where_clauses.append("ht.estado_asignacion = %s")
                params.append(estado_asignacion)
            
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
            
            query += " ORDER BY t.nombre"
            
            print(f"[LISTAR ASIGNACIONES] Query: {query}")
            print(f"[LISTAR ASIGNACIONES] Params: {params}")
            
            resultado, error = self.query_executor.ejecutar(query, tuple(params) if params else None)
            
            if error:
                print(f"[LISTAR ASIGNACIONES] Error: {error}")
                return [], error
            
            print(f"[LISTAR ASIGNACIONES] Encontrados: {len(resultado) if resultado else 0} registros")
            if resultado:
                print(f"[LISTAR ASIGNACIONES] Primer registro: {resultado[0]}")
            
            return resultado if resultado else [], None
            
        except Exception as e:
            print(f"[LISTAR ASIGNACIONES] Exception: {str(e)}")
            import traceback
            traceback.print_exc()
            return [], f"Error al listar horarios de trabajadores: {str(e)}"
            
            return resultado if resultado else [], None
            
        except Exception as e:
            print(f"[LISTAR ASIGNACIONES] Exception: {str(e)}")
            return [], f"Error al listar horarios de trabajadores: {str(e)}"


# Instancia singleton
listar_horarios_trabajadores_use_case = ListarHorariosTrabajadoresUseCase()
