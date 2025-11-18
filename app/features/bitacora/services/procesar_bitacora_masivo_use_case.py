"""
Caso de uso: Procesar Bitácora para Múltiples Trabajadores
Procesa la bitácora de varios trabajadores en el rango de fechas especificado
"""
import logging
from datetime import date
from typing import List, Tuple, Dict, Any, Optional
from .procesar_bitacora_use_case import ProcesarBitacoraUseCase

logger = logging.getLogger(__name__)


class ProcesarBitacoraMasivoUseCase:
    """Procesa bitácora para múltiples trabajadores"""
    
    def __init__(self):
        self.procesar_individual_use_case = ProcesarBitacoraUseCase()
    
    def ejecutar(
        self,
        num_trabajadores: List[int],
        fecha_inicio: date,
        fecha_fin: date
    ) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Procesa la bitácora de múltiples trabajadores
        
        Args:
            num_trabajadores: Lista de números de trabajador
            fecha_inicio: Fecha de inicio del período
            fecha_fin: Fecha de fin del período
            
        Returns:
            Tupla (resultados, error) donde resultados es una lista de:
            {
                'num_trabajador': int,
                'nombre': str,
                'success': bool,
                'stats': {'insertados': int, 'actualizados': int, 'errores': int},
                'total_registros': int,
                'error': str (si falló)
            }
        """
        try:
            logger.info(f"Procesando bitácora masiva para {len(num_trabajadores)} trabajadores")
            logger.info(f"Período: {fecha_inicio} a {fecha_fin}")
            
            resultados = []
            
            for num_trabajador in num_trabajadores:
                logger.info(f"Procesando trabajador {num_trabajador}...")
                
                try:
                    # Procesar individualmente
                    resultado_individual, error = self.procesar_individual_use_case.ejecutar(
                        num_trabajador=num_trabajador,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin
                    )
                    
                    if error:
                        logger.error(f"Error procesando trabajador {num_trabajador}: {error}")
                        resultados.append({
                            'num_trabajador': num_trabajador,
                            'nombre': 'Desconocido',
                            'success': False,
                            'error': error,
                            'stats': {'insertados': 0, 'actualizados': 0, 'errores': 0},
                            'total_registros': 0
                        })
                    else:
                        registros, stats = resultado_individual
                        logger.info(f"Trabajador {num_trabajador}: {len(registros)} registros procesados")
                        logger.info(f"Stats: {stats}")
                        
                        # Obtener nombre del trabajador (del primer registro si existe)
                        nombre = 'Sin nombre'
                        if registros and len(registros) > 0:
                            nombre = registros[0].nombre_trabajador  # Corregido: nombre_trabajador, no trabajador_nombre
                        
                        resultados.append({
                            'num_trabajador': num_trabajador,
                            'nombre': nombre,
                            'success': True,
                            'stats': stats,
                            'total_registros': len(registros)
                        })
                
                except Exception as e:
                    logger.error(f"Excepción procesando trabajador {num_trabajador}: {str(e)}")
                    resultados.append({
                        'num_trabajador': num_trabajador,
                        'nombre': 'Desconocido',
                        'success': False,
                        'error': str(e),
                        'stats': {'insertados': 0, 'actualizados': 0, 'errores': 0},
                        'total_registros': 0
                    })
            
            logger.info(f"Procesamiento masivo completado: {len(resultados)} trabajadores procesados")
            
            # Calcular totales
            total_exitosos = sum(1 for r in resultados if r['success'])
            total_fallidos = len(resultados) - total_exitosos
            
            logger.info(f"Exitosos: {total_exitosos}, Fallidos: {total_fallidos}")
            
            return resultados, None
            
        except Exception as e:
            error_msg = f"Error en procesamiento masivo: {str(e)}"
            logger.error(error_msg)
            return None, error_msg


# Instancia singleton
procesar_bitacora_masivo_use_case = ProcesarBitacoraMasivoUseCase()
