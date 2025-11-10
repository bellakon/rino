"""
Caso de uso: Obtener Plantilla de Horario por ID
Responsabilidad: Obtener una plantilla específica
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection


class ObtenerPlantillaHorarioUseCase:
    """Obtiene una plantilla de horario por ID"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, id_plantilla):
        """
        Obtiene una plantilla de horario
        
        Args:
            id_plantilla: ID de la plantilla
            
        Returns:
            tuple: (plantilla_dict, error)
        """
        try:
            query = """
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
                WHERE id = %s
            """
            
            resultado, error = self.query_executor.ejecutar(query, (id_plantilla,))
            
            if error:
                return None, error
            
            if not resultado:
                return None, "Plantilla no encontrada"
            
            # Convertir TIME a string formato HH:MM
            plantilla = resultado[0]
            for key, value in plantilla.items():
                if 'entrada' in key or 'salida' in key:
                    if value is None:
                        plantilla[key] = ''
                    else:
                        # Si es timedelta (tiempo de MySQL), convertir a string HH:MM
                        if hasattr(value, 'total_seconds'):
                            total_seconds = int(value.total_seconds())
                            hours = total_seconds // 3600
                            minutes = (total_seconds % 3600) // 60
                            plantilla[key] = f"{hours:02d}:{minutes:02d}"
                        else:
                            # Si ya es string, usarlo directamente
                            plantilla[key] = str(value)
            
            return plantilla, None
            
        except Exception as e:
            return None, f"Error al obtener plantilla: {str(e)}"


# Instancia singleton
obtener_plantilla_horario_use_case = ObtenerPlantillaHorarioUseCase()
