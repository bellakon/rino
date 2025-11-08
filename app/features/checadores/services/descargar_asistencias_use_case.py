"""
Caso de uso: Descargar asistencias del checador
Responsabilidad: Descargar asistencias e insertarlas en BD (solo nuevas)
"""
from app.config.checadores_config import CheckadoresConfig
from app.features.checadores.models import Checador
from app.features.checadores.services.checador_service import checador_service
from app.core.database.query_executor import query_executor


class DescargarAsistenciasUseCase:
    """Descarga asistencias del checador e inserta en BD"""
    
    def ejecutar(self, checador_id):
        """
        Descarga asistencias del checador y las inserta en BD (solo nuevas)
        
        Args:
            checador_id (str): ID del checador
            
        Yields:
            dict: Progreso de la operación
            
        Returns:
            dict: Resultado final
        """
        # Obtener configuración del checador
        config = CheckadoresConfig.get_checador_by_id(checador_id)
        
        if not config:
            yield {'error': 'Checador no encontrado', 'finalizado': True}
            return
        
        checador = Checador.from_dict(config)
        
        # Verificar conexión a BD
        test_query = "SELECT 1"
        _, error_bd = query_executor.ejecutar(test_query)
        if error_bd:
            yield {
                'error': f'Error de conexión a BD: {error_bd}',
                'finalizado': True
            }
            return
        
        yield {
            'estado': 'Conectando al checador...',
            'progreso': 10
        }
        
        # Obtener asistencias del checador
        asistencias, error = checador_service.obtener_asistencias(
            checador.ip,
            checador.puerto
        )
        
        if error:
            yield {
                'error': error,
                'finalizado': True
            }
            return
        
        if not asistencias or len(asistencias) == 0:
            yield {
                'estado': 'No hay asistencias en el checador',
                'total': 0,
                'insertadas': 0,
                'duplicadas': 0,
                'finalizado': True
            }
            return
        
        total_asistencias = len(asistencias)
        
        yield {
            'estado': f'Descargadas {total_asistencias} asistencias. Insertando en BD...',
            'progreso': 30,
            'total': total_asistencias
        }
        
        # Insertar en lotes para evitar timeouts
        BATCH_SIZE = 1000
        insertadas = 0
        duplicadas = 0
        
        # Query INSERT - query_executor manejará duplicados automáticamente
        query = """
            INSERT INTO asistencias 
            (num_trabajador, nombre, fecha, hora, checador, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        
        for i in range(0, total_asistencias, BATCH_SIZE):
            batch = asistencias[i:i + BATCH_SIZE]
            
            # Preparar parámetros
            params_list = [
                (
                    a['num_trabajador'],
                    a.get('nombre'),  # Puede ser None si no se obtuvo
                    a['fecha'],
                    a['hora'],
                    a['checador']
                )
                for a in batch
            ]
            
            # Ejecutar batch con ignore_duplicates=True
            # query_executor maneja duplicados según el UNIQUE constraint
            # Retorna: (cantidad_insertada, error)
            # cantidad_insertada = solo las que se insertaron (duplicados son ignorados)
            batch_insertadas, error_insert = query_executor.ejecutar_batch(
                query,
                params_list,
                ignore_duplicates=True
            )
            
            if error_insert:
                yield {
                    'error': f'Error al insertar: {error_insert}',
                    'insertadas': insertadas,
                    'duplicadas': duplicadas,
                    'finalizado': True
                }
                return
            
            # batch_insertadas = registros que SÍ se insertaron
            # batch - batch_insertadas = duplicados que se ignoraron
            batch_duplicadas = len(batch) - batch_insertadas
            
            insertadas += batch_insertadas
            duplicadas += batch_duplicadas
            
            # Calcular progreso (30% a 90%)
            progreso = 30 + int((i + len(batch)) / total_asistencias * 60)
            
            yield {
                'estado': f'Procesando... {i + len(batch)}/{total_asistencias}',
                'progreso': progreso,
                'total': total_asistencias,
                'procesadas': i + len(batch),
                'insertadas': insertadas,
                'duplicadas': duplicadas
            }
        
        # Finalizado
        yield {
            'estado': 'Descarga completada',
            'progreso': 100,
            'total': total_asistencias,
            'insertadas': insertadas,
            'duplicadas': duplicadas,
            'finalizado': True
        }


# Instancia singleton
descargar_asistencias_use_case = DescargarAsistenciasUseCase()
