"""
Caso de uso: Editar Plantilla de Horario
Responsabilidad: Actualizar una plantilla existente
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.horarios.models.plantilla_horario import PlantillaHorario


class EditarPlantillaHorarioUseCase:
    """Edita una plantilla de horario existente"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, id_plantilla, plantilla):
        """
        Actualiza una plantilla de horario
        
        Args:
            id_plantilla: ID de la plantilla a editar
            plantilla: Objeto PlantillaHorario con los nuevos datos
            
        Returns:
            tuple: (success, error)
        """
        try:
            # Generar nuevo hash
            nuevo_hash = plantilla.generar_hash_horario()
            
            # Verificar que no exista otra plantilla con el mismo hash
            query_hash = """
                SELECT id FROM plantillas_horarios 
                WHERE horario_hash = %s AND id != %s
            """
            resultado, _ = self.query_executor.ejecutar(query_hash, (nuevo_hash, id_plantilla))
            
            if resultado:
                return False, "Ya existe otra plantilla con ese mismo horario"
            
            # Actualizar plantilla
            query = """
                UPDATE plantillas_horarios
                SET 
                    nombre_horario = %s,
                    descripcion_horario = %s,
                    lunes_entrada_1 = %s, lunes_salida_1 = %s, lunes_entrada_2 = %s, lunes_salida_2 = %s,
                    martes_entrada_1 = %s, martes_salida_1 = %s, martes_entrada_2 = %s, martes_salida_2 = %s,
                    miercoles_entrada_1 = %s, miercoles_salida_1 = %s, miercoles_entrada_2 = %s, miercoles_salida_2 = %s,
                    jueves_entrada_1 = %s, jueves_salida_1 = %s, jueves_entrada_2 = %s, jueves_salida_2 = %s,
                    viernes_entrada_1 = %s, viernes_salida_1 = %s, viernes_entrada_2 = %s, viernes_salida_2 = %s,
                    sabado_entrada_1 = %s, sabado_salida_1 = %s, sabado_entrada_2 = %s, sabado_salida_2 = %s,
                    domingo_entrada_1 = %s, domingo_salida_1 = %s, domingo_entrada_2 = %s, domingo_salida_2 = %s,
                    activo = %s,
                    horario_hash = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """
            
            params = (
                plantilla.nombre_horario,
                plantilla.descripcion_horario,
                plantilla.lunes_entrada_1, plantilla.lunes_salida_1, plantilla.lunes_entrada_2, plantilla.lunes_salida_2,
                plantilla.martes_entrada_1, plantilla.martes_salida_1, plantilla.martes_entrada_2, plantilla.martes_salida_2,
                plantilla.miercoles_entrada_1, plantilla.miercoles_salida_1, plantilla.miercoles_entrada_2, plantilla.miercoles_salida_2,
                plantilla.jueves_entrada_1, plantilla.jueves_salida_1, plantilla.jueves_entrada_2, plantilla.jueves_salida_2,
                plantilla.viernes_entrada_1, plantilla.viernes_salida_1, plantilla.viernes_entrada_2, plantilla.viernes_salida_2,
                plantilla.sabado_entrada_1, plantilla.sabado_salida_1, plantilla.sabado_entrada_2, plantilla.sabado_salida_2,
                plantilla.domingo_entrada_1, plantilla.domingo_salida_1, plantilla.domingo_entrada_2, plantilla.domingo_salida_2,
                plantilla.activo,
                nuevo_hash,
                id_plantilla
            )
            
            _, error = self.query_executor.ejecutar(query, params)
            
            if error:
                return False, error
            
            return True, None
            
        except Exception as e:
            return False, f"Error al editar plantilla: {str(e)}"


# Instancia singleton
editar_plantilla_horario_use_case = EditarPlantillaHorarioUseCase()
