"""
Caso de uso: Importar checadas desde archivo .res
Responsabilidad: Parsear archivo .res, detectar duplicados e insertar en BD con progreso
"""
from app.core.database.query_executor import query_executor
import csv
from typing import Generator, Dict, List, Tuple
from io import StringIO
from datetime import datetime


class ImportarChecadasUseCase:
    """Importa checadas desde archivo .res con detección de duplicados y progreso en tiempo real"""
    
    def ejecutar(self, archivo_contenido: str) -> Generator[Dict, None, None]:
        """
        Procesa archivo .res e inserta checadas en BD
        
        Args:
            archivo_contenido (str): Contenido del archivo .res como texto
            
        Yields:
            dict: Progreso de la operación con estado, progreso, total, insertadas, duplicadas
            
        Formato .res esperado (CSV):
            num_trabajador,"fecha","hora","checador"
            97,"2024-10-19","08:00","CLN5204760269"
        """
        
        yield {
            'estado': 'Analizando archivo...',
            'progreso': 5,
            'fase': 'lectura'
        }
        
        # Dividir en líneas sin cargar todo en memoria (para archivos grandes)
        # Procesar en chunks para no saturar memoria
        lineas_raw = archivo_contenido.strip().split('\n')
        total_lineas = len(lineas_raw)
        
        # Liberar memoria del contenido original
        del archivo_contenido
        
        if total_lineas == 0:
            yield {
                'error': 'El archivo está vacío',
                'finalizado': True
            }
            return
        
        yield {
            'estado': f'Archivo leído: {total_lineas:,} registros encontrados',
            'progreso': 10,
            'total': total_lineas,
            'fase': 'parseo'
        }
        
        # Parsear líneas CSV
        checadas_parseadas = []
        lineas_invalidas = []
        ultimo_yield_en = 0
        ultimo_checador = None  # Para registros sin checador, usar el último encontrado
        
        for idx, linea in enumerate(lineas_raw, start=1):
            # Saltar líneas vacías
            if not linea.strip():
                continue
            
            # Enviar progreso cada 1000 líneas para archivos grandes
            if idx - ultimo_yield_en >= 1000:
                progreso_parseo = 10 + int((idx / total_lineas) * 10)  # 10% a 20%
                yield {
                    'estado': f'Parseando... {idx:,}/{total_lineas:,} líneas',
                    'progreso': progreso_parseo,
                    'fase': 'parseo'
                }
                ultimo_yield_en = idx
                
            try:
                # Parsear CSV (maneja comillas correctamente)
                reader = csv.reader([linea])
                campos = next(reader)
                
                # Manejar registros con 3 o 4 campos
                if len(campos) == 3:
                    # Si falta checador, usar el último encontrado o valor por defecto
                    num_trabajador, fecha, hora = campos
                    checador = ultimo_checador if ultimo_checador else 'DESCONOCIDO'
                elif len(campos) == 4:
                    num_trabajador, fecha, hora, checador = campos
                else:
                    lineas_invalidas.append({
                        'linea': idx,
                        'contenido': linea[:100],
                        'error': f'Esperados 3 o 4 campos, encontrados {len(campos)}'
                    })
                    continue
                
                # Validar y limpiar num_trabajador (quitar ceros a la izquierda)
                num_trabajador = num_trabajador.strip()
                if not num_trabajador:
                    lineas_invalidas.append({
                        'linea': idx,
                        'contenido': linea[:100],
                        'error': 'num_trabajador está vacío'
                    })
                    continue
                    
                if not num_trabajador.isdigit():
                    lineas_invalidas.append({
                        'linea': idx,
                        'contenido': linea[:100],
                        'error': f'num_trabajador debe ser numérico (recibido: "{num_trabajador}")'
                    })
                    continue
                
                # Quitar ceros a la izquierda: 000348 -> 348
                num_trabajador = str(int(num_trabajador))
                
                # Validar fecha (YYYY-MM-DD)
                fecha = fecha.strip()
                if not fecha:
                    lineas_invalidas.append({
                        'linea': idx,
                        'contenido': linea[:100],
                        'error': 'fecha está vacía'
                    })
                    continue
                
                # Validar formato de fecha
                try:
                    datetime.strptime(fecha, '%Y-%m-%d')
                except ValueError:
                    lineas_invalidas.append({
                        'linea': idx,
                        'contenido': linea[:100],
                        'error': f'Formato de fecha inválido: "{fecha}" (esperado: YYYY-MM-DD)'
                    })
                    continue
                
                # Validar hora (HH:MM o HH:MM:SS)
                hora = hora.strip()
                if not hora:
                    lineas_invalidas.append({
                        'linea': idx,
                        'contenido': linea[:100],
                        'error': 'hora está vacía'
                    })
                    continue
                
                # Validar formato de hora
                try:
                    if ':' not in hora:
                        raise ValueError('Falta separador :')
                    # Aceptar HH:MM o HH:MM:SS
                    partes_hora = hora.split(':')
                    if len(partes_hora) == 2:
                        # Formato HH:MM
                        h, m = partes_hora
                        if not (h.isdigit() and m.isdigit()):
                            raise ValueError('Hora/minuto no numérico')
                        if not (0 <= int(h) <= 23 and 0 <= int(m) <= 59):
                            raise ValueError('Hora fuera de rango')
                        hora = f"{int(h):02d}:{int(m):02d}"
                    elif len(partes_hora) == 3:
                        # Formato HH:MM:SS
                        h, m, s = partes_hora
                        if not (h.isdigit() and m.isdigit() and s.isdigit()):
                            raise ValueError('Hora/minuto/segundo no numérico')
                        if not (0 <= int(h) <= 23 and 0 <= int(m) <= 59 and 0 <= int(s) <= 59):
                            raise ValueError('Hora fuera de rango')
                        hora = f"{int(h):02d}:{int(m):02d}"  # Normalizar a HH:MM
                    else:
                        raise ValueError('Formato incorrecto')
                except ValueError as e:
                    lineas_invalidas.append({
                        'linea': idx,
                        'contenido': linea[:100],
                        'error': f'Formato de hora inválido: "{hora}" (esperado: HH:MM)'
                    })
                    continue
                
                # Validar checador
                checador = checador.strip()
                if not checador:
                    lineas_invalidas.append({
                        'linea': idx,
                        'contenido': linea[:100],
                        'error': 'checador está vacío'
                    })
                    continue
                
                # Guardar el último checador válido
                ultimo_checador = checador
                
                # Todo válido, agregar a lista
                checadas_parseadas.append({
                    'num_trabajador': int(num_trabajador),
                    'fecha': fecha,
                    'hora': hora,
                    'checador': checador
                })
                
            except Exception as e:
                lineas_invalidas.append({
                    'linea': idx,
                    'contenido': linea[:100],
                    'error': f'Error al parsear: {str(e)}'
                })
        
        total_validas = len(checadas_parseadas)
        total_invalidas = len(lineas_invalidas)
        
        # Agrupar errores por tipo para mejor análisis
        errores_agrupados = {}
        for error_info in lineas_invalidas:
            tipo_error = error_info['error'].split(':')[0]  # Primera parte del mensaje
            if tipo_error not in errores_agrupados:
                errores_agrupados[tipo_error] = {
                    'count': 0,
                    'ejemplos': []
                }
            errores_agrupados[tipo_error]['count'] += 1
            if len(errores_agrupados[tipo_error]['ejemplos']) < 5:  # Guardar 5 ejemplos
                errores_agrupados[tipo_error]['ejemplos'].append(error_info)
        
        if total_validas == 0:
            yield {
                'error': f'No se encontraron registros válidos. {total_invalidas} líneas inválidas.',
                'errores_agrupados': errores_agrupados,
                'lineas_invalidas': lineas_invalidas[:20],  # Primeras 20 para debugging
                'finalizado': True
            }
            return
        
        yield {
            'estado': f'Parseo completado: {total_validas:,} válidas, {total_invalidas:,} inválidas',
            'progreso': 20,
            'total': total_validas,
            'invalidas': total_invalidas,
            'errores_agrupados': errores_agrupados,  # Enviar errores agrupados
            'fase': 'validacion'
        }
        
        # Detectar duplicados en la BD (batch SELECT para eficiencia)
        yield {
            'estado': 'Verificando duplicados en base de datos...',
            'progreso': 25,
            'fase': 'duplicados'
        }
        
        duplicados_bd = set()
        for progreso_info in self._detectar_duplicados_bd(checadas_parseadas):
            if 'progreso' in progreso_info:
                # Enviar progreso de detección de duplicados (25% a 40%)
                yield progreso_info
            else:
                # Es el resultado final
                duplicados_bd = progreso_info['duplicados']
        
        yield {
            'estado': f'Duplicados detectados: {len(duplicados_bd):,}',
            'progreso': 40,
            'duplicados_detectados': len(duplicados_bd),
            'fase': 'duplicados'
        }
        
        # Filtrar solo registros nuevos
        checadas_nuevas = [
            c for c in checadas_parseadas
            if (c['num_trabajador'], c['fecha'], c['hora']) not in duplicados_bd
        ]
        
        total_nuevas = len(checadas_nuevas)
        
        if total_nuevas == 0:
            yield {
                'estado': 'No hay registros nuevos para insertar',
                'progreso': 100,
                'total': total_validas,
                'insertadas': 0,
                'duplicadas': len(duplicados_bd),
                'invalidas': total_invalidas,
                'finalizado': True
            }
            return
        
        # PREVIEW: Mostrar resumen y esperar confirmación
        # IMPORTANTE: NO enviar todas las checadas al frontend (puede ser demasiado grande)
        # Solo enviar preview y guardar checadas en sesión del servidor
        # Enviar hasta 500 registros para preview (suficiente para ver variedad)
        max_preview = min(500, len(checadas_nuevas))
        preview_registros = checadas_nuevas[:max_preview]
        preview_invalidas = lineas_invalidas[:100]  # Primeras 100 inválidas
        
        # Guardar checadas en self para usarlas después de confirmación
        self.checadas_pendientes = checadas_nuevas
        
        yield {
            'estado': 'Análisis completado. Esperando confirmación...',
            'progreso': 45,
            'fase': 'preview',
            'requiere_confirmacion': True,
            'resumen': {
                'total_lineas': total_lineas,
                'validas': total_validas,
                'invalidas': total_invalidas,
                'duplicadas': len(duplicados_bd),
                'nuevas': total_nuevas,
                'a_insertar': total_nuevas
            },
            'preview': {
                'registros_nuevos': preview_registros,
                'total_nuevos': len(checadas_nuevas),
                'lineas_invalidas': preview_invalidas,
                'total_invalidas': len(lineas_invalidas)
            },
            'errores_agrupados': errores_agrupados
        }
        
        # El usuario debe confirmar desde el frontend
        # El endpoint /importar-confirmar continuará desde aquí
        return
    
    def ejecutar_insercion(self, checadas_nuevas: List[Dict]) -> Generator[Dict, None, None]:
        """
        Ejecuta la inserción de checadas después de confirmación del usuario
        
        Args:
            checadas_nuevas: Lista de checadas validadas y sin duplicados
            
        Yields:
            dict: Progreso de inserción
        """
        total_nuevas = len(checadas_nuevas)
        
        if total_nuevas == 0:
            yield {
                'error': 'No hay registros para insertar',
                'finalizado': True
            }
            return
        
        yield {
            'estado': f'Iniciando inserción de {total_nuevas:,} registros...',
            'progreso': 5,
            'fase': 'insercion'
        }
        
        # Obtener nombres de trabajadores
        yield {
            'estado': 'Obteniendo nombres de trabajadores...',
            'progreso': 10,
            'fase': 'nombres'
        }
        
        nombres_trabajadores = self._obtener_nombres_trabajadores(checadas_nuevas)
        
        yield {
            'estado': f'Nombres obtenidos: {len(nombres_trabajadores):,} trabajadores',
            'progreso': 15,
            'fase': 'nombres'
        }
        
        # Insertar en lotes (batches) para archivos grandes
        BATCH_SIZE = 1000
        insertadas = 0
        errores_insercion = []
        
        query = """
            INSERT INTO asistencias 
            (num_trabajador, nombre, fecha, hora, checador, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        
        for i in range(0, total_nuevas, BATCH_SIZE):
            batch = checadas_nuevas[i:i + BATCH_SIZE]
            
            # Preparar parámetros para batch con nombres
            params_list = [
                (
                    c['num_trabajador'], 
                    nombres_trabajadores.get(c['num_trabajador']),  # Nombre o None
                    c['fecha'], 
                    c['hora'], 
                    c['checador']
                )
                for c in batch
            ]
            
            # Ejecutar batch insert
            batch_insertadas, error = query_executor.ejecutar_batch(
                query,
                params_list,
                ignore_duplicates=True  # Por si acaso hay duplicados concurrentes
            )
            
            if error:
                errores_insercion.append({
                    'batch': i // BATCH_SIZE + 1,
                    'error': error
                })
                # Continuar con siguientes batches
                continue
            
            insertadas += batch_insertadas
            
            # Calcular progreso (15% a 95%)
            progreso = 15 + int((i + len(batch)) / total_nuevas * 80)
            
            yield {
                'estado': f'Insertando... {insertadas:,}/{total_nuevas:,}',
                'progreso': progreso,
                'insertadas': insertadas,
                'fase': 'insercion'
            }
        
        # Resultado final
        yield {
            'estado': 'Inserción completada exitosamente',
            'progreso': 100,
            'insertadas': insertadas,
            'errores': errores_insercion if errores_insercion else None,
            'finalizado': True
        }
    
    def _detectar_duplicados_bd(self, checadas: List[Dict]) -> Generator[Dict, None, None]:
        """
        Detecta duplicados en BD usando batch SELECT
        
        Args:
            checadas: Lista de diccionarios con num_trabajador, fecha, hora
            
        Yields:
            dict: Progreso de la detección
            
        Último yield contiene:
            {'duplicados': set de tuplas (num_trabajador, fecha, hora)}
        """
        if not checadas:
            yield {'duplicados': set()}
            return
        
        # Construir query con múltiples condiciones OR
        # Para eficiencia, agrupar en batches de 1000
        BATCH_SIZE = 1000
        duplicados = set()
        total_batches = (len(checadas) + BATCH_SIZE - 1) // BATCH_SIZE
        
        for batch_idx, i in enumerate(range(0, len(checadas), BATCH_SIZE), 1):
            batch = checadas[i:i + BATCH_SIZE]
            
            # Enviar progreso cada batch
            progreso = 25 + int((batch_idx / total_batches) * 15)  # 25% a 40%
            yield {
                'estado': f'Verificando duplicados... batch {batch_idx}/{total_batches}',
                'progreso': progreso,
                'fase': 'duplicados'
            }
            
            # Construir condiciones WHERE con IN para mejor performance
            # Crear lista de tuplas únicas
            tuplas_unicas = list(set(
                (c['num_trabajador'], c['fecha'], c['hora'])
                for c in batch
            ))
            
            if not tuplas_unicas:
                continue
            
            # Query optimizada usando IN con tuplas
            placeholders = ','.join(['(%s, %s, %s)'] * len(tuplas_unicas))
            query = f"""
                SELECT num_trabajador, fecha, hora
                FROM asistencias
                WHERE (num_trabajador, fecha, hora) IN ({placeholders})
            """
            
            # Aplanar lista de tuplas para params
            params = []
            for tupla in tuplas_unicas:
                params.extend(tupla)
            
            resultados, error = query_executor.ejecutar(query, tuple(params))
            
            if error:
                # Si hay error, asumir que no hay duplicados (inserción fallará después)
                continue
            
            if resultados:
                for row in resultados:
                    duplicados.add((
                        row['num_trabajador'],
                        str(row['fecha']),  # Convertir a string para comparación
                        str(row['hora'])
                    ))
        
        # Yield final con resultados
        yield {'duplicados': duplicados}
    
    def _obtener_nombres_trabajadores(self, checadas: List[Dict]) -> Dict[int, str]:
        """
        Obtiene nombres de trabajadores desde la tabla trabajadores
        
        Args:
            checadas: Lista de diccionarios con num_trabajador
            
        Returns:
            dict: {num_trabajador: nombre_trabajador}
        """
        if not checadas:
            return {}
        
        # Obtener números únicos de trabajadores
        nums_trabajadores = list(set(c['num_trabajador'] for c in checadas))
        
        if not nums_trabajadores:
            return {}
        
        # Query para obtener nombres
        placeholders = ','.join(['%s'] * len(nums_trabajadores))
        query = f"""
            SELECT num_trabajador, nombre
            FROM trabajadores
            WHERE num_trabajador IN ({placeholders})
        """
        
        resultados, error = query_executor.ejecutar(query, tuple(nums_trabajadores))
        
        nombres = {}
        if not error and resultados:
            for row in resultados:
                nombres[row['num_trabajador']] = row['nombre']
        
        return nombres


# Instancia singleton
importar_checadas_use_case = ImportarChecadasUseCase()
