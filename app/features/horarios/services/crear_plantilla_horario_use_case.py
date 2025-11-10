"""
Caso de uso: Crear Plantilla de Horario
Responsabilidad: Validar y crear una plantilla de horario única
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.horarios.models.plantilla_horario import PlantillaHorario


class CrearPlantillaHorarioUseCase:
    """Crea una plantilla de horario validando que no exista duplicado"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, plantilla: PlantillaHorario):
        """
        Crea una plantilla de horario
        
        Args:
            plantilla: Objeto PlantillaHorario
            
        Returns:
            tuple: (id_insertado, error)
        """
        try:
            # Generar hash del horario
            horario_hash = plantilla.generar_hash_horario()
            
            # Verificar si ya existe una plantilla con el mismo horario
            query_verificar = "SELECT id, nombre_horario FROM plantillas_horarios WHERE horario_hash = %s"
            resultado, error = self.query_executor.ejecutar(query_verificar, (horario_hash,))
            
            if error:
                return None, error
            
            if resultado:
                return None, f"Ya existe una plantilla con este horario: {resultado[0]['nombre_horario']}"
            
            # Insertar plantilla
            query = """
                INSERT INTO plantillas_horarios (
                    nombre_horario, descripcion_horario,
                    lunes_entrada_1, lunes_salida_1, lunes_entrada_2, lunes_salida_2,
                    martes_entrada_1, martes_salida_1, martes_entrada_2, martes_salida_2,
                    miercoles_entrada_1, miercoles_salida_1, miercoles_entrada_2, miercoles_salida_2,
                    jueves_entrada_1, jueves_salida_1, jueves_entrada_2, jueves_salida_2,
                    viernes_entrada_1, viernes_salida_1, viernes_entrada_2, viernes_salida_2,
                    sabado_entrada_1, sabado_salida_1, sabado_entrada_2, sabado_salida_2,
                    domingo_entrada_1, domingo_salida_1, domingo_entrada_2, domingo_salida_2,
                    horario_hash, activo
                ) VALUES (
                    %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s
                )
            """
            
            params = (
                plantilla.nombre_horario, plantilla.descripcion_horario,
                plantilla.lunes_entrada_1, plantilla.lunes_salida_1, plantilla.lunes_entrada_2, plantilla.lunes_salida_2,
                plantilla.martes_entrada_1, plantilla.martes_salida_1, plantilla.martes_entrada_2, plantilla.martes_salida_2,
                plantilla.miercoles_entrada_1, plantilla.miercoles_salida_1, plantilla.miercoles_entrada_2, plantilla.miercoles_salida_2,
                plantilla.jueves_entrada_1, plantilla.jueves_salida_1, plantilla.jueves_entrada_2, plantilla.jueves_salida_2,
                plantilla.viernes_entrada_1, plantilla.viernes_salida_1, plantilla.viernes_entrada_2, plantilla.viernes_salida_2,
                plantilla.sabado_entrada_1, plantilla.sabado_salida_1, plantilla.sabado_entrada_2, plantilla.sabado_salida_2,
                plantilla.domingo_entrada_1, plantilla.domingo_salida_1, plantilla.domingo_entrada_2, plantilla.domingo_salida_2,
                horario_hash, plantilla.activo
            )
            
            resultado, error = self.query_executor.ejecutar(query, params)
            
            if error:
                return None, error
            
            # Obtener el ID insertado
            query_last_id = "SELECT LAST_INSERT_ID() as id"
            resultado_id, _ = self.query_executor.ejecutar(query_last_id)
            id_insertado = resultado_id[0]['id'] if resultado_id else None
            
            return id_insertado, None
            
        except Exception as e:
            return None, f"Error al crear plantilla: {str(e)}"


# Instancia singleton
crear_plantilla_horario_use_case = CrearPlantillaHorarioUseCase()
