"""
Caso de uso: Migrar asistencias a RinoTime
Responsabilidad: Consultar asistencias y migrarlas a iclock_transaction en RinoTime
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.query_builder import QueryBuilder
from app.core.database.connection import db_connection, db_sync_connection
from datetime import datetime


class MigrarAsistenciasRinoTimeUseCase:
    """Migra asistencias de la BD local a RinoTime"""
    
    def __init__(self):
        self.query_executor_local = QueryExecutor(db_connection)
        self.query_executor_sync = QueryExecutor(db_sync_connection)
    
    def contar_asistencias(self, checador=None):
        """
        Cuenta cuántas asistencias se migrarán
        
        Args:
            checador: Filtrar por checador (serial number)
            
        Returns:
            tuple: (total_registros, error)
        """
        try:
            # Usar QueryBuilder para construir la query
            builder = QueryBuilder("SELECT COUNT(*) as total FROM asistencias")
            
            if checador:
                builder.add_filter('checador', checador)
            
            query, params = builder.build()
            resultado, error = self.query_executor_local.ejecutar(query, params)
            
            if error:
                return 0, error
            
            total = resultado[0]['total'] if resultado else 0
            return total, None
            
        except Exception as e:
            return 0, f"Error al contar asistencias: {str(e)}"
    
    def ejecutar(self, terminal_sn, checador=None):
        """
        Migra asistencias a RinoTime
        
        Args:
            terminal_sn: Serial del terminal (CLN5204760269 o CLN5204760200)
            checador: Filtrar por checador (serial del dispositivo de origen)
            
        Yields:
            dict: Progreso de la operación
        """
        try:
            # Usar QueryBuilder para construir la query de consulta
            builder = QueryBuilder("""
                SELECT 
                    num_trabajador,
                    nombre,
                    fecha,
                    hora,
                    checador
                FROM asistencias
            """)
            
            if checador:
                builder.add_filter('checador', checador)
            
            builder.add_order_by('fecha, hora')
            
            query, params = builder.build()
            
            yield {
                'estado': 'Consultando asistencias...',
                'progreso': 10
            }
            
            # Obtener asistencias de la BD local usando QueryExecutor
            asistencias, error = self.query_executor_local.ejecutar(query, params)
            
            if error:
                yield {
                    'error': error,
                    'finalizado': True
                }
                return
            
            if not asistencias or len(asistencias) == 0:
                yield {
                    'estado': 'No hay asistencias para migrar',
                    'total': 0,
                    'insertadas': 0,
                    'duplicadas': 0,
                    'finalizado': True
                }
                return
            
            total_asistencias = len(asistencias)
            
            yield {
                'estado': f'Encontradas {total_asistencias} asistencias. Verificando duplicados...',
                'progreso': 30,
                'total': total_asistencias
            }
            
            # Determinar terminal_alias según el serial
            terminal_alias = 'Edificio ACB' if terminal_sn == 'CLN5204760269' else 'Edificio LISC'
            terminal_id = 3 if terminal_sn == 'CLN5204760269' else 4
            
            # OPTIMIZACIÓN: Filtrar duplicados antes de insertar
            # Construir lista de combinaciones únicas para verificar
            # IMPORTANTE: No incluimos terminal_sn porque los registros locales
            # tienen el checador de origen, no el terminal de destino
            verificaciones = []
            for asistencia in asistencias:
                fecha_str = str(asistencia['fecha'])
                hora_str = str(asistencia['hora'])
                punch_time = f"{fecha_str} {hora_str}"
                
                verificaciones.append((
                    str(asistencia['num_trabajador']),
                    punch_time
                ))
            
            yield {
                'estado': 'Consultando registros existentes en RinoTime...',
                'progreso': 40
            }
            
            # Verificar cuáles ya existen (en lotes)
            registros_existentes = set()
            VERIFICAR_BATCH = 1000
            
            for i in range(0, len(verificaciones), VERIFICAR_BATCH):
                batch_verificar = verificaciones[i:i + VERIFICAR_BATCH]
                
                # Crear query para verificar este batch
                # Solo comparamos emp_code y punch_time (no terminal_sn)
                placeholders = ','.join(['(%s, %s)'] * len(batch_verificar))
                query_verificar = f"""
                    SELECT emp_code, punch_time
                    FROM iclock_transaction
                    WHERE (emp_code, punch_time) IN ({placeholders})
                """
                
                # Aplanar la lista de parámetros
                params_verificar = []
                for v in batch_verificar:
                    params_verificar.extend(v)
                
                existentes, error_ver = self.query_executor_sync.ejecutar(
                    query_verificar,
                    tuple(params_verificar)
                )
                
                if not error_ver and existentes:
                    for registro in existentes:
                        key = (registro['emp_code'], registro['punch_time'])
                        registros_existentes.add(key)
            
            total_duplicados_previos = len(registros_existentes)
            
            yield {
                'estado': f'Encontrados {total_duplicados_previos} duplicados. Preparando inserción...',
                'progreso': 50,
                'duplicadas': total_duplicados_previos
            }
            
            # Insertar en lotes usando QueryExecutor.ejecutar_batch
            BATCH_SIZE = 500
            insertadas = 0
            duplicadas = total_duplicados_previos  # Ya sabemos cuántos son duplicados
            errores = 0
            
            # Query INSERT para RinoTime (sin id, se auto-incrementa)
            insert_query = """
                INSERT INTO iclock_transaction (
                    emp_code,
                    punch_time,
                    punch_state,
                    verify_type,
                    work_code,
                    terminal_sn,
                    terminal_alias,
                    area_alias,
                    longitude,
                    latitude,
                    gps_location,
                    mobile,
                    source,
                    purpose,
                    crc,
                    is_attendance,
                    reserved,
                    upload_time,
                    sync_status,
                    sync_time,
                    emp_id,
                    terminal_id,
                    is_mask,
                    temperature
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
            """
            
            for i in range(0, total_asistencias, BATCH_SIZE):
                batch = asistencias[i:i + BATCH_SIZE]
                
                # Preparar lista de parámetros para el batch (solo los NO duplicados)
                params_list = []
                for asistencia in batch:
                    # Convertir fecha y hora a punch_time (datetime)
                    fecha_str = str(asistencia['fecha'])
                    hora_str = str(asistencia['hora'])
                    punch_time = f"{fecha_str} {hora_str}"
                    
                    # Verificar si este registro ya existe (solo emp_code + punch_time)
                    key = (str(asistencia['num_trabajador']), punch_time)
                    if key in registros_existentes:
                        continue  # Saltar duplicados ya conocidos
                    
                    # upload_time es ahora
                    upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                    
                    params_list.append((
                        str(asistencia['num_trabajador']),  # emp_code
                        punch_time,                          # punch_time
                        '255',                               # punch_state
                        25,                                  # verify_type
                        '',                                  # work_code
                        terminal_sn,                         # terminal_sn
                        terminal_alias,                      # terminal_alias
                        'Minatitlan',                       # area_alias
                        None,                               # longitude
                        None,                               # latitude
                        None,                               # gps_location
                        None,                               # mobile
                        1,                                  # source
                        9,                                  # purpose
                        'AAIAAACAAAIAAAFABAJA',            # crc
                        None,                               # is_attendance
                        None,                               # reserved
                        upload_time,                        # upload_time
                        None,                               # sync_status
                        None,                               # sync_time
                        None,                               # emp_id
                        terminal_id,                        # terminal_id
                        255,                                # is_mask
                        255.0                               # temperature
                    ))
                
                # Solo ejecutar batch si hay registros para insertar
                if params_list:
                    # Ejecutar batch usando QueryExecutor con ignore_duplicates
                    batch_insertadas, error_insert = self.query_executor_sync.ejecutar_batch(
                        insert_query,
                        params_list,
                        ignore_duplicates=True
                    )
                    
                    if error_insert:
                        errores += len(params_list)
                    else:
                        insertadas += batch_insertadas
                        # Puede haber duplicados que se crearon entre la verificación y ahora
                        duplicadas += (len(params_list) - batch_insertadas)
                
                # Calcular progreso (50% a 95%)
                progreso = 50 + int((i + len(batch)) / total_asistencias * 45)
                
                yield {
                    'estado': f'Procesando... {i + len(batch)}/{total_asistencias}',
                    'progreso': progreso,
                    'total': total_asistencias,
                    'procesadas': i + len(batch),
                    'insertadas': insertadas,
                    'duplicadas': duplicadas,
                    'errores': errores
                }
            
            # Finalizado
            yield {
                'estado': 'Migración completada',
                'progreso': 100,
                'total': total_asistencias,
                'insertadas': insertadas,
                'duplicadas': duplicadas,
                'errores': errores,
                'finalizado': True
            }
            
        except Exception as e:
            yield {
                'error': f"Error en migración: {str(e)}",
                'finalizado': True
            }


# Instancia singleton
migrar_asistencias_rinotime_use_case = MigrarAsistenciasRinoTimeUseCase()
