"""
Caso de uso: Obtener Checadas del Día
Obtiene todas las checadas de un trabajador en un día específico
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.config import bitacora_config
from datetime import date, time, datetime, timedelta
from typing import Optional, List, Dict, Tuple


class ObtenerChecadasDiaUseCase:
    """Obtiene checadas de un trabajador en un día"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def _son_checadas_duplicadas(self, hora1: time, hora2: time) -> bool:
        """
        Determina si dos checadas son duplicadas (diferencia menor a 1 minuto)
        
        Args:
            hora1: Primera hora (puede ser time o timedelta)
            hora2: Segunda hora (puede ser time o timedelta)
            
        Returns:
            True si la diferencia es menor a SEGUNDOS_MAX_CHECADAS_DUPLICADAS
        """
        # Convertir timedelta a time si es necesario (MySQL TIME viene como timedelta)
        def to_time(t):
            if isinstance(t, timedelta):
                total_seconds = int(t.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                return time(hours, minutes, seconds)
            return t
        
        hora1 = to_time(hora1)
        hora2 = to_time(hora2)
        
        # Convertir a datetime para calcular diferencia
        dt1 = datetime.combine(date.today(), hora1)
        dt2 = datetime.combine(date.today(), hora2)
        diferencia = abs((dt2 - dt1).total_seconds())
        
        return diferencia <= bitacora_config.SEGUNDOS_MAX_CHECADAS_DUPLICADAS
    
    def _filtrar_checadas_duplicadas(self, checadas_list: List[time]) -> List[time]:
        """
        Filtra checadas duplicadas INTELIGENTEMENTE
        
        ESTRATEGIA:
        - Si un grupo tiene duplicados muy cercanos (< 60 seg), mantener PRIMERA y ÚLTIMA
        - Esto permite que 17:00:00 y 17:00:51 se mantengan ambas (posible entrada y salida)
        - Pero 17:00:00, 17:00:10, 17:00:51 → mantiene 17:00:00 y 17:00:51
        
        Args:
            checadas_list: Lista de horas ordenadas
            
        Returns:
            Lista filtrada sin duplicados intermedios
        """
        if len(checadas_list) <= 1:
            return checadas_list
        
        filtradas = []
        i = 0
        
        while i < len(checadas_list):
            # Agregar la primera del grupo
            primera_del_grupo = checadas_list[i]
            filtradas.append(primera_del_grupo)
            
            # Buscar cuántas checadas están en el mismo grupo (duplicados consecutivos)
            j = i + 1
            ultima_del_grupo = primera_del_grupo
            
            while j < len(checadas_list):
                if self._son_checadas_duplicadas(checadas_list[j-1], checadas_list[j]):
                    # Es parte del mismo grupo
                    ultima_del_grupo = checadas_list[j]
                    j += 1
                else:
                    # Ya no es parte del grupo
                    break
            
            # Si hubo más de una checada en el grupo, agregar la última
            if j > i + 1:  # Hubo duplicados
                # Solo agregar la última si es diferente de la primera
                if not self._son_checadas_duplicadas(primera_del_grupo, ultima_del_grupo):
                    filtradas.append(ultima_del_grupo)
            
            # Continuar desde donde terminó el grupo
            i = j
        
        return filtradas
    
    def _asignar_checadas_inteligentemente(
        self, 
        checadas_filtradas: List[time],
        horario_esperado: Optional[str] = None
    ) -> Tuple[Optional[time], Optional[time], Optional[time], Optional[time]]:
        """
        Asigna checadas de forma inteligente a entrada1, salida1, entrada2, salida2
        PRIORIZA LA ASISTENCIA: elige las checadas más cercanas al horario esperado
        
        Args:
            checadas_filtradas: Lista de checadas sin duplicados
            horario_esperado: Horario como "09:00-17:00" o "08:00-12:00,14:00-16:00"
            
        Returns:
            Tupla (checada1, checada2, checada3, checada4)
        """
        if not checadas_filtradas:
            return None, None, None, None
        
        # Si solo hay 1 checada, es entrada
        if len(checadas_filtradas) == 1:
            return checadas_filtradas[0], None, None, None
        
        # Si hay 2 checadas, son entrada y salida
        if len(checadas_filtradas) == 2:
            return checadas_filtradas[0], checadas_filtradas[1], None, None
        
        # Si hay 3 o más checadas Y tenemos horario, ser INTELIGENTE
        if horario_esperado and len(checadas_filtradas) >= 3:
            return self._asignar_por_cercania_horario(checadas_filtradas, horario_esperado)
        
        # Fallback: si no hay horario, usar orden cronológico
        if len(checadas_filtradas) == 3:
            return checadas_filtradas[0], checadas_filtradas[1], checadas_filtradas[2], None
        
        # 4 o más
        return (
            checadas_filtradas[0],
            checadas_filtradas[1],
            checadas_filtradas[2] if len(checadas_filtradas) >= 3 else None,
            checadas_filtradas[3] if len(checadas_filtradas) >= 4 else None
        )
    
    def _asignar_por_cercania_horario(
        self, 
        checadas: List[time],
        horario_esperado: str
    ) -> Tuple[Optional[time], Optional[time], Optional[time], Optional[time]]:
        """
        Asigna checadas eligiendo las MÁS CERCANAS al horario esperado
        Esto PRIORIZA la asistencia del trabajador
        
        Ejemplo:
        - Checadas: 08:49, 10:49, 17:00
        - Horario: 09:00-17:00
        - Resultado: checada1=08:49 (más cerca de 09:00), checada2=17:00 (más cerca de 17:00)
        """
        try:
            # Parsear horario esperado
            if ',' in horario_esperado:
                # Horario mixto: "08:00-12:00,14:00-16:00"
                partes = horario_esperado.split(',')
                bloque1 = partes[0].split('-')
                bloque2 = partes[1].split('-') if len(partes) > 1 else None
                
                entrada1_esperada = self._parsear_hora(bloque1[0])
                salida1_esperada = self._parsear_hora(bloque1[1])
                entrada2_esperada = self._parsear_hora(bloque2[0]) if bloque2 else None
                salida2_esperada = self._parsear_hora(bloque2[1]) if bloque2 else None
                
                # Buscar las más cercanas a cada horario
                c1 = self._buscar_mas_cercana(checadas, entrada1_esperada)
                c2 = self._buscar_mas_cercana(checadas, salida1_esperada, excluir=[c1])
                c3 = self._buscar_mas_cercana(checadas, entrada2_esperada, excluir=[c1, c2]) if entrada2_esperada else None
                c4 = self._buscar_mas_cercana(checadas, salida2_esperada, excluir=[c1, c2, c3]) if salida2_esperada else None
                
                return c1, c2, c3, c4
            else:
                # Horario simple: "09:00-17:00"
                partes = horario_esperado.split('-')
                if len(partes) != 2:
                    # Horario inválido, usar fallback
                    return self._asignar_fallback(checadas)
                
                entrada_esperada = self._parsear_hora(partes[0])
                salida_esperada = self._parsear_hora(partes[1])
                
                # Buscar la más cercana a la entrada
                checada1 = self._buscar_mas_cercana(checadas, entrada_esperada)
                
                # Buscar la más cercana a la salida (excluyendo la que ya usamos)
                checada2 = self._buscar_mas_cercana(checadas, salida_esperada, excluir=[checada1])
                
                # Las demás checadas van en orden cronológico (sin repetir las usadas)
                # Convertir a set para comparación más robusta
                usadas = {str(checada1), str(checada2)} if checada1 and checada2 else set()
                restantes = [c for c in checadas if str(c) not in usadas]
                checada3 = restantes[0] if len(restantes) >= 1 else None
                checada4 = restantes[1] if len(restantes) >= 2 else None
                
                return checada1, checada2, checada3, checada4
        except Exception as e:
            print(f"[ERROR] Error en asignación inteligente: {e}")
            import traceback
            traceback.print_exc()
            # Fallback a asignación simple
            return self._asignar_fallback(checadas)
    
    def _asignar_fallback(self, checadas: List[time]) -> Tuple[Optional[time], Optional[time], Optional[time], Optional[time]]:
        """Asignación simple cuando falla la inteligente"""
        if len(checadas) == 0:
            return None, None, None, None
        elif len(checadas) == 1:
            return checadas[0], None, None, None
        elif len(checadas) == 2:
            return checadas[0], checadas[1], None, None
        elif len(checadas) == 3:
            return checadas[0], checadas[1], checadas[2], None
        else:
            return checadas[0], checadas[1], checadas[2], checadas[3]
    
    def _parsear_hora(self, hora_str: str) -> time:
        """Convierte string "09:00" a objeto time"""
        partes = hora_str.strip().split(':')
        return time(int(partes[0]), int(partes[1]))
    
    def _buscar_mas_cercana(
        self, 
        checadas: List[time], 
        hora_objetivo: time,
        excluir: List[time] = None
    ) -> Optional[time]:
        """
        Busca la checada más cercana a una hora objetivo
        
        Args:
            checadas: Lista de checadas disponibles
            hora_objetivo: Hora a la que queremos acercarnos
            excluir: Lista de checadas que ya no se pueden usar
            
        Returns:
            La checada más cercana o None
        """
        if not checadas:
            return None
        
        # Convertir timedelta a time si es necesario
        def to_time(t):
            if isinstance(t, timedelta):
                total_seconds = int(t.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                return time(hours, minutes, seconds)
            return t
        
        excluir = excluir or []
        excluir_convertidos = [to_time(e) for e in excluir]
        
        # Convertir todas las checadas a time para comparación
        checadas_convertidas = [(to_time(c), c) for c in checadas]  # (time, original)
        disponibles = [(t, orig) for t, orig in checadas_convertidas if t not in excluir_convertidos]
        
        if not disponibles:
            return None
        
        # Calcular diferencia en minutos para cada checada
        def diferencia_minutos(item) -> int:
            c = item[0]  # time convertido
            c_minutos = c.hour * 60 + c.minute
            obj_minutos = hora_objetivo.hour * 60 + hora_objetivo.minute
            return abs(c_minutos - obj_minutos)
        
        # Retornar la original de menor diferencia
        mejor = min(disponibles, key=diferencia_minutos)
        return mejor[1]  # Retornar el original (puede ser timedelta)
    
    def ejecutar(
        self,
        num_trabajador: int,
        fecha: date,
        horario_esperado: Optional[str] = None
    ) -> tuple[Optional[Dict], Optional[str]]:
        """
        Obtiene las checadas del día y las organiza por entrada/salida
        CON LÓGICA INTELIGENTE: filtra duplicados y prioriza asistencia
        
        Args:
            num_trabajador: Número del trabajador
            fecha: Fecha a consultar
            horario_esperado: Horario esperado del trabajador (opcional)
            
        Returns:
            tuple: (diccionario con checadas organizadas, error)
        """
        try:
            # Obtener TODAS las checadas del día ordenadas por hora
            query = """
                SELECT 
                    id,
                    num_trabajador,
                    fecha,
                    hora
                FROM asistencias
                WHERE num_trabajador = %s
                AND fecha = %s
                ORDER BY hora ASC
            """
            
            resultados, error = self.query_executor.ejecutar(
                query, 
                (num_trabajador, fecha)
            )
            
            if error:
                return None, f"Error al obtener checadas: {error}"
            
            # Si no hay checadas
            if not resultados:
                return {
                    'tiene_checadas': False,
                    'num_checadas': 0,
                    'checada1': None,  # Entrada 1
                    'checada2': None,  # Salida 1
                    'checada3': None,  # Entrada 2 (horario mixto)
                    'checada4': None,  # Salida 2 (horario mixto)
                    'checadas_originales': [],
                    'checadas_filtradas': []
                }, None
            
            # Extraer solo las horas
            checadas_originales = [r['hora'] for r in resultados]
            
            print(f"[DEBUG] Fecha {fecha}: {len(checadas_originales)} checadas originales: {checadas_originales}")
            
            # PASO 1: Filtrar checadas duplicadas (diferencia < 1 minuto)
            checadas_filtradas = self._filtrar_checadas_duplicadas(checadas_originales)
            
            print(f"[DEBUG] Fecha {fecha}: {len(checadas_filtradas)} checadas después de filtrar: {checadas_filtradas}")
            
            # PASO 2: Asignar inteligentemente a entrada/salida
            checada1, checada2, checada3, checada4 = self._asignar_checadas_inteligentemente(
                checadas_filtradas,
                horario_esperado
            )
            
            print(f"[DEBUG] Fecha {fecha}: Asignación final -> c1={checada1}, c2={checada2}, c3={checada3}, c4={checada4}")
            
            # Organizar resultado
            checadas_organizadas = {
                'tiene_checadas': True,
                'num_checadas': len(checadas_filtradas),  # Después de filtrar
                'num_checadas_originales': len(checadas_originales),
                'checada1': checada1,
                'checada2': checada2,
                'checada3': checada3,
                'checada4': checada4,
                'checadas_originales': checadas_originales,
                'checadas_filtradas': checadas_filtradas,
                'se_filtraron_duplicadas': len(checadas_originales) != len(checadas_filtradas)
            }
            
            return checadas_organizadas, None
            
        except Exception as e:
            return None, f"Error al obtener checadas del día: {str(e)}"


# Instancia singleton
obtener_checadas_dia_use_case = ObtenerChecadasDiaUseCase()
