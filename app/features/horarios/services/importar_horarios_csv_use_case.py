"""
Caso de uso: Importar Horarios desde CSV
Responsabilidad: Procesar CSV, crear/reutilizar plantillas, asignar a trabajadores
"""
import csv
import io
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.horarios.models.plantilla_horario import PlantillaHorario
from app.features.horarios.models.horario_trabajador import HorarioTrabajador
from app.features.horarios.services.crear_plantilla_horario_use_case import crear_plantilla_horario_use_case
from app.features.horarios.services.asignar_horario_trabajador_use_case import asignar_horario_trabajador_use_case


class ImportarHorariosCSVUseCase:
    """Importa horarios desde CSV"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
        self.plantillas_cache = {}  # Cache: hash -> id_plantilla
    
    def ejecutar(self, archivo_csv):
        """
        Importa horarios desde CSV
        
        Args:
            archivo_csv: Objeto de archivo CSV
            
        Returns:
            tuple: (resultado_dict, error)
        """
        try:
            # Leer CSV con encoding UTF-8-SIG para manejar BOM
            contenido = archivo_csv.read().decode('utf-8-sig')
            csv_reader = csv.DictReader(io.StringIO(contenido))
            
            resultados = {
                'total_filas': 0,
                'plantillas_creadas': 0,
                'plantillas_reutilizadas': 0,
                'asignaciones_exitosas': 0,
                'trabajadores_no_encontrados': [],
                'errores': []
            }
            
            for row in csv_reader:
                resultados['total_filas'] += 1
                
                try:
                    # Validar num_trabajador
                    num_trabajador = int(row.get('num_trabajador', 0))
                    
                    if not num_trabajador:
                        resultados['errores'].append(f"Fila {resultados['total_filas']}: num_trabajador no especificado")
                        continue
                    
                    # Validar campos requeridos
                    if not row.get('nombre_horario'):
                        resultados['errores'].append(f"Trabajador {num_trabajador}: nombre_horario es requerido")
                        continue
                    
                    if not row.get('fecha_inicio_asignacion'):
                        resultados['errores'].append(f"Trabajador {num_trabajador}: fecha_inicio_asignacion es requerida")
                        continue
                    
                    if not row.get('semestre'):
                        resultados['errores'].append(f"Trabajador {num_trabajador}: semestre es requerido")
                        continue
                    
                    # Verificar que el trabajador existe
                    query_trabajador = "SELECT num_trabajador FROM trabajadores WHERE num_trabajador = %s"
                    resultado, _ = self.query_executor.ejecutar(query_trabajador, (num_trabajador,))
                    
                    if not resultado:
                        resultados['trabajadores_no_encontrados'].append(num_trabajador)
                        continue
                    
                    # Crear objeto PlantillaHorario
                    plantilla = PlantillaHorario(
                        nombre_horario=row.get('nombre_horario'),
                        descripcion_horario=row.get('descripcion_horario', ''),
                        lunes_entrada_1=self._limpiar_hora(row.get('lunes_entrada_1')),
                        lunes_salida_1=self._limpiar_hora(row.get('lunes_salida_1')),
                        lunes_entrada_2=self._limpiar_hora(row.get('lunes_entrada_2')),
                        lunes_salida_2=self._limpiar_hora(row.get('lunes_salida_2')),
                        martes_entrada_1=self._limpiar_hora(row.get('martes_entrada_1')),
                        martes_salida_1=self._limpiar_hora(row.get('martes_salida_1')),
                        martes_entrada_2=self._limpiar_hora(row.get('martes_entrada_2')),
                        martes_salida_2=self._limpiar_hora(row.get('martes_salida_2')),
                        miercoles_entrada_1=self._limpiar_hora(row.get('miercoles_entrada_1')),
                        miercoles_salida_1=self._limpiar_hora(row.get('miercoles_salida_1')),
                        miercoles_entrada_2=self._limpiar_hora(row.get('miercoles_entrada_2')),
                        miercoles_salida_2=self._limpiar_hora(row.get('miercoles_salida_2')),
                        jueves_entrada_1=self._limpiar_hora(row.get('jueves_entrada_1')),
                        jueves_salida_1=self._limpiar_hora(row.get('jueves_salida_1')),
                        jueves_entrada_2=self._limpiar_hora(row.get('jueves_entrada_2')),
                        jueves_salida_2=self._limpiar_hora(row.get('jueves_salida_2')),
                        viernes_entrada_1=self._limpiar_hora(row.get('viernes_entrada_1')),
                        viernes_salida_1=self._limpiar_hora(row.get('viernes_salida_1')),
                        viernes_entrada_2=self._limpiar_hora(row.get('viernes_entrada_2')),
                        viernes_salida_2=self._limpiar_hora(row.get('viernes_salida_2')),
                        sabado_entrada_1=self._limpiar_hora(row.get('sabado_entrada_1')),
                        sabado_salida_1=self._limpiar_hora(row.get('sabado_salida_1')),
                        sabado_entrada_2=self._limpiar_hora(row.get('sabado_entrada_2')),
                        sabado_salida_2=self._limpiar_hora(row.get('sabado_salida_2')),
                        domingo_entrada_1=self._limpiar_hora(row.get('domingo_entrada_1')),
                        domingo_salida_1=self._limpiar_hora(row.get('domingo_salida_1')),
                        domingo_entrada_2=self._limpiar_hora(row.get('domingo_entrada_2')),
                        domingo_salida_2=self._limpiar_hora(row.get('domingo_salida_2')),
                        activo=True
                    )
                    
                    # Obtener o crear plantilla (reutiliza si el hash coincide)
                    id_plantilla = self._obtener_o_crear_plantilla(plantilla, resultados)
                    
                    if not id_plantilla:
                        continue
                    
                    # Crear asignación de horario al trabajador
                    horario_trabajador = HorarioTrabajador(
                        num_trabajador=num_trabajador,
                        plantilla_horario_id=id_plantilla,
                        fecha_inicio_asignacion=row.get('fecha_inicio_asignacion'),
                        fecha_fin_asignacion=row.get('fecha_fin_asignacion') if row.get('fecha_fin_asignacion') else None,
                        semestre=row.get('semestre'),
                        estado_asignacion='activo',
                        activo_asignacion=True
                    )
                    
                    # El caso de uso asignar_horario validará traslapes automáticamente
                    id_asignacion, error = asignar_horario_trabajador_use_case.ejecutar(horario_trabajador)
                    
                    print(f"[IMPORTAR CSV] Trabajador {num_trabajador}: id_asignacion={id_asignacion}, error={error}")
                    
                    if error:
                        resultados['errores'].append(f"Trabajador {num_trabajador}: {error}")
                    else:
                        resultados['asignaciones_exitosas'] += 1
                        
                except Exception as e:
                    resultados['errores'].append(f"Fila {resultados['total_filas']}: {str(e)}")
            
            return resultados, None
            
        except Exception as e:
            return None, f"Error al procesar CSV: {str(e)}"
    
    def _limpiar_hora(self, hora_str):
        """Limpia y valida formato de hora"""
        if not hora_str or str(hora_str).strip() == '':
            return None
        hora_str = str(hora_str).strip()
        # Convertir formato 9:00 a 09:00
        if ':' in hora_str:
            partes = hora_str.split(':')
            if len(partes) == 2:
                return f"{int(partes[0]):02d}:{int(partes[1]):02d}"
        return None
    
    def _obtener_o_crear_plantilla(self, plantilla, resultados):
        """Obtiene plantilla existente por hash o crea nueva"""
        horario_hash = plantilla.generar_hash_horario()
        
        # Buscar en cache
        if horario_hash in self.plantillas_cache:
            resultados['plantillas_reutilizadas'] += 1
            return self.plantillas_cache[horario_hash]
        
        # Buscar en BD
        query = "SELECT id FROM plantillas_horarios WHERE horario_hash = %s"
        resultado, _ = self.query_executor.ejecutar(query, (horario_hash,))
        
        if resultado:
            id_plantilla = resultado[0]['id']
            self.plantillas_cache[horario_hash] = id_plantilla
            resultados['plantillas_reutilizadas'] += 1
            return id_plantilla
        
        # Crear nueva plantilla
        id_plantilla, error = crear_plantilla_horario_use_case.ejecutar(plantilla)
        
        if error:
            resultados['errores'].append(f"Error creando plantilla: {error}")
            return None
        
        self.plantillas_cache[horario_hash] = id_plantilla
        resultados['plantillas_creadas'] += 1
        return id_plantilla


# Instancia singleton
importar_horarios_csv_use_case = ImportarHorariosCSVUseCase()
