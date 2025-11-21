"""
Caso de uso: Crear Movimiento Masivo
Crea el mismo movimiento para múltiples trabajadores
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.movimientos.models.movimiento_models import Movimiento
from typing import List, Optional
from datetime import date


class CrearMovimientoMasivoUseCase:
    """Crea un movimiento para múltiples trabajadores"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(
        self,
        nums_trabajadores: List[int],
        tipo_movimiento_id: int,
        fecha_inicio: date,
        fecha_fin: date,
        observaciones: Optional[str] = None,
        datos_personalizados: Optional[dict] = None,
        usuario_registro: Optional[str] = None
    ) -> tuple[Optional[List[int]], Optional[str]]:
        """
        Crea el mismo movimiento para múltiples trabajadores
        
        Args:
            nums_trabajadores: Lista de números de trabajador
            tipo_movimiento_id: ID del tipo de movimiento
            fecha_inicio: Fecha de inicio del movimiento
            fecha_fin: Fecha fin del movimiento
            observaciones: Observaciones del movimiento
            datos_personalizados: Datos adicionales en JSON
            usuario_registro: Usuario que registra
            
        Returns:
            tuple: (lista de IDs creados, error)
        """
        try:
            # Validar que hay trabajadores
            if not nums_trabajadores or len(nums_trabajadores) == 0:
                return None, "Debe seleccionar al menos un trabajador"
            
            # Validar fechas
            if fecha_fin < fecha_inicio:
                return None, "La fecha fin no puede ser anterior a la fecha de inicio"
            
            # Validar que el tipo de movimiento existe
            query_validar = """
                SELECT id, nomenclatura, nombre 
                FROM tipos_movimientos 
                WHERE id = %s AND activo = 1
            """
            resultado, error = self.query_executor.ejecutar(query_validar, (tipo_movimiento_id,))
            
            if error:
                return None, f"Error al validar tipo de movimiento: {error}"
            
            if not resultado or len(resultado) == 0:
                return None, "El tipo de movimiento no existe o está inactivo"
            
            # Validar que todos los trabajadores existen
            placeholders = ','.join(['%s'] * len(nums_trabajadores))
            query_trabajadores = f"""
                SELECT num_trabajador, nombre 
                FROM trabajadores 
                WHERE num_trabajador IN ({placeholders})
            """
            trabajadores_encontrados, error = self.query_executor.ejecutar(
                query_trabajadores, 
                tuple(nums_trabajadores)
            )
            
            if error:
                return None, f"Error al validar trabajadores: {error}"
            
            if len(trabajadores_encontrados) != len(nums_trabajadores):
                nums_encontrados = [t['num_trabajador'] for t in trabajadores_encontrados]
                nums_no_encontrados = [n for n in nums_trabajadores if n not in nums_encontrados]
                return None, f"Trabajadores no encontrados: {', '.join(map(str, nums_no_encontrados))}"
            
            # Preparar datos JSON
            import json
            datos_json = None
            if datos_personalizados:
                datos_json = json.dumps(datos_personalizados)
            
            # Insertar movimiento para cada trabajador
            query_insert = """
                INSERT INTO movimientos 
                (num_trabajador, tipo_movimiento_id, fecha_inicio, fecha_fin, 
                 observaciones, datos_personalizados, usuario_registro)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            ids_creados = []
            trabajadores_procesados = []
            errores = []
            
            for num_trabajador in nums_trabajadores:
                try:
                    resultado, error = self.query_executor.ejecutar(
                        query_insert,
                        (num_trabajador, tipo_movimiento_id, fecha_inicio, fecha_fin,
                         observaciones, datos_json, usuario_registro)
                    )
                    
                    if error:
                        trabajador_nombre = next(
                            (t['nombre'] for t in trabajadores_encontrados if t['num_trabajador'] == num_trabajador),
                            str(num_trabajador)
                        )
                        errores.append(f"Error en trabajador {trabajador_nombre}: {error}")
                        continue
                    
                    # Obtener el ID insertado
                    query_last_id = "SELECT LAST_INSERT_ID() as id"
                    result_id, _ = self.query_executor.ejecutar(query_last_id)
                    if result_id and len(result_id) > 0:
                        movimiento_id = result_id[0]['id']
                        ids_creados.append(movimiento_id)
                        trabajador_nombre = next(
                            (t['nombre'] for t in trabajadores_encontrados if t['num_trabajador'] == num_trabajador),
                            str(num_trabajador)
                        )
                        trabajadores_procesados.append(trabajador_nombre)
                        
                except Exception as e:
                    trabajador_nombre = next(
                        (t['nombre'] for t in trabajadores_encontrados if t['num_trabajador'] == num_trabajador),
                        str(num_trabajador)
                    )
                    errores.append(f"Error en trabajador {trabajador_nombre}: {str(e)}")
            
            # Verificar resultados
            if len(ids_creados) == 0:
                return None, f"No se pudo crear ningún movimiento. Errores: {'; '.join(errores)}"
            
            if len(errores) > 0:
                mensaje_exito = f"Movimiento creado para {len(ids_creados)} trabajador(es): {', '.join(trabajadores_procesados[:5])}"
                if len(trabajadores_procesados) > 5:
                    mensaje_exito += f" y {len(trabajadores_procesados) - 5} más"
                mensaje_error = f"Errores en {len(errores)} trabajador(es): {'; '.join(errores[:3])}"
                if len(errores) > 3:
                    mensaje_error += f" y {len(errores) - 3} más"
                return ids_creados, f"{mensaje_exito}. {mensaje_error}"
            
            return ids_creados, None
            
        except Exception as e:
            return None, f"Error al crear movimientos masivos: {str(e)}"


# Instancia singleton
crear_movimiento_masivo_use_case = CrearMovimientoMasivoUseCase()
