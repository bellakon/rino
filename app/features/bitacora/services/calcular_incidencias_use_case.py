"""
Caso de uso: Calcular Incidencias
Analiza checadas vs horario y determina el código de incidencia
"""
from app.config import bitacora_config
from datetime import time, datetime, timedelta
from typing import Dict, Optional
from decimal import Decimal


class CalcularIncidenciasUseCase:
    """Calcula incidencias comparando checadas con horario esperado"""
    
    def __init__(self):
        pass
    
    def _timedelta_to_time(self, td):
        """Convierte timedelta a time (MySQL TIME se convierte a timedelta)"""
        if td is None:
            return None
        if isinstance(td, time):
            return td
        if isinstance(td, timedelta):
            total_seconds = int(td.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return time(hours, minutes, seconds)
        if isinstance(td, str):
            # Si es string, parsearlo
            return datetime.strptime(td, '%H:%M:%S').time() if ':' in td else None
        return td
    
    def ejecutar(
        self,
        checadas: Dict,
        horario_esperado: str,
        tipo_plaza: str,
        movimiento: Optional[Dict] = None
    ) -> Dict:
        """
        Calcula el código de incidencia y detalles
        
        Args:
            checadas: Dict con checada1, checada2, checada3, checada4
            horario_esperado: String como "08:00-16:00" o "08:00-12:00,14:00-16:00"
            tipo_plaza: Tipo de plaza del trabajador (DOCENTE, etc.)
            movimiento: Dict con info de movimiento si existe
            
        Returns:
            Dict con: codigo_incidencia, tipo_movimiento, minutos_retardo, 
                     horas_trabajadas, descripcion_incidencia
        """
        # Si tiene movimiento, es J o L
        if movimiento and movimiento.get('tiene_movimiento'):
            categoria = movimiento.get('categoria', '')
            if 'Licencia' in categoria:
                return {
                    'codigo_incidencia': 'L',
                    'tipo_movimiento': movimiento.get('tipo_movimiento'),
                    'minutos_retardo': 0,
                    'horas_trabajadas': Decimal('0.00'),
                    'descripcion_incidencia': f"Licencia: {movimiento.get('tipo_nombre')}"
                }
            else:
                return {
                    'codigo_incidencia': 'J',
                    'tipo_movimiento': movimiento.get('tipo_movimiento'),
                    'minutos_retardo': 0,
                    'horas_trabajadas': Decimal('0.00'),
                    'descripcion_incidencia': f"Justificado: {movimiento.get('tipo_nombre')}"
                }
        
        # Sin checadas = FALTA
        if not checadas.get('tiene_checadas'):
            return {
                'codigo_incidencia': 'F',
                'tipo_movimiento': None,
                'minutos_retardo': 0,
                'horas_trabajadas': Decimal('0.00'),
                'descripcion_incidencia': 'Falta - No marcó asistencia'
            }
        
        # Parsear horario esperado
        horarios_parseados = self._parsear_horario(horario_esperado)
        if not horarios_parseados:
            return {
                'codigo_incidencia': 'O',
                'tipo_movimiento': None,
                'minutos_retardo': 0,
                'horas_trabajadas': Decimal('0.00'),
                'descripcion_incidencia': 'Omisión - Horario no válido'
            }
        
        # Determinar si es docente
        es_docente = bitacora_config.es_docente(tipo_plaza)
        
        # Calcular según tipo de horario
        if len(horarios_parseados) == 1:
            # Horario simple (una entrada y una salida)
            return self._calcular_horario_simple(
                checadas, 
                horarios_parseados[0], 
                es_docente
            )
        else:
            # Horario mixto (entrada-salida-entrada-salida)
            return self._calcular_horario_mixto(
                checadas, 
                horarios_parseados, 
                es_docente
            )
    
    def _parsear_horario(self, horario_texto: str) -> list:
        """
        Parsea string de horario a objetos time
        
        Args:
            horario_texto: "08:00-16:00" o "08:00-12:00,14:00-16:00"
            
        Returns:
            Lista de tuplas [(entrada1, salida1), (entrada2, salida2)]
        """
        try:
            horarios = []
            
            # Split por coma para horarios mixtos
            bloques = horario_texto.split(',')
            
            for bloque in bloques:
                partes = bloque.strip().split('-')
                if len(partes) == 2:
                    entrada = datetime.strptime(partes[0].strip(), '%H:%M').time()
                    salida = datetime.strptime(partes[1].strip(), '%H:%M').time()
                    horarios.append((entrada, salida))
            
            return horarios
        except:
            return []
    
    def _calcular_horario_simple(
        self, 
        checadas: Dict, 
        horario: tuple, 
        es_docente: bool
    ) -> Dict:
        """Calcula incidencias para horario simple (una entrada, una salida)"""
        entrada_esperada, salida_esperada = horario
        checada1 = self._timedelta_to_time(checadas.get('checada1'))
        checada2 = self._timedelta_to_time(checadas.get('checada2'))
        
        # Sin entrada = FALTA
        if not checada1:
            return {
                'codigo_incidencia': 'F',
                'tipo_movimiento': None,
                'minutos_retardo': 0,
                'horas_trabajadas': Decimal('0.00'),
                'descripcion_incidencia': 'Falta - No marcó entrada'
            }
        
        # Calcular diferencia de entrada
        minutos_diferencia_entrada = self._calcular_diferencia_minutos(
            checada1, 
            entrada_esperada
        )
        
        # Validar entrada temprana
        if minutos_diferencia_entrada < 0:  # Llegó antes
            minutos_antes = abs(minutos_diferencia_entrada)
            if minutos_antes > bitacora_config.MINUTOS_ANTES_PERMITIDOS:
                return {
                    'codigo_incidencia': 'F',
                    'tipo_movimiento': None,
                    'minutos_retardo': 0,
                    'horas_trabajadas': Decimal('0.00'),
                    'descripcion_incidencia': f'Falta - Entrada demasiado temprana ({minutos_antes} min antes)'
                }
        
        # Calcular código de retardo para entrada
        minutos_tarde = max(0, minutos_diferencia_entrada)
        codigo_entrada = bitacora_config.calcular_codigo_retardo(minutos_tarde)
        
        # Si no marcó salida = OMISIÓN
        if not checada2:
            return {
                'codigo_incidencia': 'O',
                'tipo_movimiento': None,
                'minutos_retardo': minutos_tarde,
                'horas_trabajadas': Decimal('0.00'),
                'descripcion_incidencia': 'Omisión - Marcó entrada pero no salida'
            }
        
        # Validar salida
        minutos_diferencia_salida = self._calcular_diferencia_minutos(
            checada2, 
            salida_esperada
        )
        
        codigo_salida, desc_salida = bitacora_config.validar_salida(
            minutos_diferencia_salida, 
            es_docente
        )
        
        # Calcular horas trabajadas
        horas_trabajadas = self._calcular_horas_trabajadas(checada1, checada2)
        
        # Determinar código final (el peor de entrada y salida)
        codigo_final = self._codigo_mas_grave(codigo_entrada, codigo_salida)
        
        # Generar descripción
        desc_entrada = self._generar_descripcion_entrada(codigo_entrada, minutos_tarde)
        descripcion = f"{desc_entrada}. {desc_salida}" if desc_salida != 'Asistencia' else desc_entrada
        
        return {
            'codigo_incidencia': codigo_final,
            'tipo_movimiento': None,
            'minutos_retardo': minutos_tarde,
            'horas_trabajadas': horas_trabajadas,
            'descripcion_incidencia': descripcion
        }
    
    def _calcular_horario_mixto(
        self, 
        checadas: Dict, 
        horarios: list, 
        es_docente: bool
    ) -> Dict:
        """Calcula incidencias para horario mixto (dos bloques)"""
        # Para horario mixto necesitamos 4 checadas idealmente
        # Simplificado: verificar cada bloque
        
        bloque1 = horarios[0]  # (entrada1, salida1)
        bloque2 = horarios[1] if len(horarios) > 1 else None
        
        checada1 = self._timedelta_to_time(checadas.get('checada1'))
        checada2 = self._timedelta_to_time(checadas.get('checada2'))
        checada3 = self._timedelta_to_time(checadas.get('checada3'))
        checada4 = self._timedelta_to_time(checadas.get('checada4'))
        
        # Validar primer bloque (igual que horario simple)
        if not checada1:
            return {
                'codigo_incidencia': 'F',
                'tipo_movimiento': None,
                'minutos_retardo': 0,
                'horas_trabajadas': Decimal('0.00'),
                'descripcion_incidencia': 'Falta - No marcó primera entrada'
            }
        
        # Calcular incidencia del primer bloque
        resultado_bloque1 = self._calcular_bloque_horario(
            checada1, checada2, bloque1, es_docente, "primer bloque"
        )
        
        # Si hay segundo bloque, validar
        if bloque2 and (checada3 or checada4):
            resultado_bloque2 = self._calcular_bloque_horario(
                checada3, checada4, bloque2, es_docente, "segundo bloque"
            )
            
            # Combinar resultados (código más grave)
            codigo_final = self._codigo_mas_grave(
                resultado_bloque1['codigo_incidencia'],
                resultado_bloque2['codigo_incidencia']
            )
            
            horas_totales = resultado_bloque1['horas_trabajadas'] + resultado_bloque2['horas_trabajadas']
            minutos_totales = resultado_bloque1['minutos_retardo'] + resultado_bloque2['minutos_retardo']
            
            return {
                'codigo_incidencia': codigo_final,
                'tipo_movimiento': None,
                'minutos_retardo': minutos_totales,
                'horas_trabajadas': horas_totales,
                'descripcion_incidencia': f"Bloque 1: {resultado_bloque1['descripcion_incidencia']}. Bloque 2: {resultado_bloque2['descripcion_incidencia']}"
            }
        
        return resultado_bloque1
    
    def _calcular_bloque_horario(
        self, 
        entrada_checada, 
        salida_checada, 
        horario, 
        es_docente, 
        nombre_bloque
    ) -> Dict:
        """Calcula incidencia para un bloque de horario"""
        entrada_esperada, salida_esperada = horario
        
        if not entrada_checada:
            return {
                'codigo_incidencia': 'F',
                'minutos_retardo': 0,
                'horas_trabajadas': Decimal('0.00'),
                'descripcion_incidencia': f'Falta - No marcó entrada en {nombre_bloque}'
            }
        
        minutos_diferencia = self._calcular_diferencia_minutos(entrada_checada, entrada_esperada)
        minutos_tarde = max(0, minutos_diferencia)
        codigo = bitacora_config.calcular_codigo_retardo(minutos_tarde)
        
        if not salida_checada:
            return {
                'codigo_incidencia': 'O',
                'minutos_retardo': minutos_tarde,
                'horas_trabajadas': Decimal('0.00'),
                'descripcion_incidencia': f'Omisión - No marcó salida en {nombre_bloque}'
            }
        
        horas = self._calcular_horas_trabajadas(entrada_checada, salida_checada)
        desc = self._generar_descripcion_entrada(codigo, minutos_tarde)
        
        return {
            'codigo_incidencia': codigo,
            'minutos_retardo': minutos_tarde,
            'horas_trabajadas': horas,
            'descripcion_incidencia': desc
        }
    
    def _calcular_diferencia_minutos(self, hora_real: time, hora_esperada: time) -> int:
        """Calcula diferencia en minutos (positivo = tarde, negativo = temprano)"""
        real_minutos = hora_real.hour * 60 + hora_real.minute
        esperada_minutos = hora_esperada.hour * 60 + hora_esperada.minute
        return real_minutos - esperada_minutos
    
    def _calcular_horas_trabajadas(self, entrada: time, salida: time) -> Decimal:
        """Calcula horas trabajadas entre entrada y salida"""
        entrada_minutos = entrada.hour * 60 + entrada.minute
        salida_minutos = salida.hour * 60 + salida.minute
        minutos_trabajados = salida_minutos - entrada_minutos
        horas = Decimal(minutos_trabajados) / Decimal(60)
        return round(horas, 2)
    
    def _codigo_mas_grave(self, codigo1: str, codigo2: str) -> str:
        """Determina cuál código de incidencia es más grave"""
        gravedad = {'F': 5, 'O': 4, 'R+': 3, 'ST': 2, 'R-': 1, 'A': 0}
        return codigo1 if gravedad.get(codigo1, 0) >= gravedad.get(codigo2, 0) else codigo2
    
    def _generar_descripcion_entrada(self, codigo: str, minutos_tarde: int) -> str:
        """Genera descripción legible del código de entrada"""
        if codigo == 'A':
            return 'Asistencia'
        elif codigo == 'R-':
            return f'Retardo Menor ({minutos_tarde} min)'
        elif codigo == 'R+':
            return f'Retardo Mayor ({minutos_tarde} min)'
        elif codigo == 'F':
            return f'Falta ({minutos_tarde} min tarde)'
        return 'Incidencia'


# Instancia singleton
calcular_incidencias_use_case = CalcularIncidenciasUseCase()
