"""
Modelo: Registro de Bitácora
Representa un día procesado de un trabajador con incidencias calculadas
"""
from datetime import date, time, datetime
from typing import Optional
from decimal import Decimal


class BitacoraRecord:
    """Modelo de registro de bitácora"""
    
    def __init__(
        self,
        num_trabajador: int,
        fecha: date,
        codigo_incidencia: str,
        id: Optional[int] = None,
        departamento: Optional[str] = None,
        nombre_trabajador: Optional[str] = None,
        turno_id: Optional[int] = None,
        horario_texto: Optional[str] = None,
        tipo_movimiento: Optional[str] = None,
        movimiento_id: Optional[int] = None,
        checada1: Optional[time] = None,
        checada2: Optional[time] = None,
        checada3: Optional[time] = None,
        checada4: Optional[time] = None,
        minutos_retardo: int = 0,
        horas_trabajadas: Decimal = Decimal('0.00'),
        descripcion_incidencia: Optional[str] = None,
        fecha_procesamiento: Optional[datetime] = None,
        procesado_por: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.num_trabajador = num_trabajador
        self.departamento = departamento
        self.nombre_trabajador = nombre_trabajador
        self.fecha = fecha
        self.turno_id = turno_id
        self.horario_texto = horario_texto
        self.codigo_incidencia = codigo_incidencia
        self.tipo_movimiento = tipo_movimiento
        self.movimiento_id = movimiento_id
        self.checada1 = checada1
        self.checada2 = checada2
        self.checada3 = checada3
        self.checada4 = checada4
        self.minutos_retardo = minutos_retardo
        self.horas_trabajadas = horas_trabajadas
        self.descripcion_incidencia = descripcion_incidencia
        self.fecha_procesamiento = fecha_procesamiento
        self.procesado_por = procesado_por
        self.created_at = created_at
        self.updated_at = updated_at
    
    def validar(self) -> tuple[bool, Optional[str]]:
        """
        Valida el registro de bitácora
        
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        # Validar campos obligatorios
        if not self.num_trabajador:
            return False, "Número de trabajador es requerido"
        
        if not self.fecha:
            return False, "Fecha es requerida"
        
        if not self.codigo_incidencia:
            return False, "Código de incidencia es requerido"
        
        # Validar código de incidencia
        codigos_validos = ['A', 'F', 'R+', 'R-', 'O', 'ST', 'J', 'L']
        if self.codigo_incidencia not in codigos_validos:
            return False, f"Código de incidencia inválido. Debe ser uno de: {', '.join(codigos_validos)}"
        
        # Si es J o L, debe tener tipo_movimiento
        if self.codigo_incidencia in ['J', 'L'] and not self.tipo_movimiento:
            return False, "Código J o L requiere especificar tipo_movimiento"
        
        # Validar minutos de retardo
        if self.minutos_retardo < 0:
            return False, "Minutos de retardo no puede ser negativo"
        
        # Validar horas trabajadas
        if self.horas_trabajadas < 0:
            return False, "Horas trabajadas no puede ser negativo"
        
        return True, None
    
    def to_dict(self) -> dict:
        """Convierte el registro a diccionario para JSON"""
        
        def time_to_str(t):
            """Convierte time o timedelta a string"""
            if t is None:
                return None
            if isinstance(t, str):
                return t
            if isinstance(t, time):
                return t.isoformat()
            # Si es timedelta (MySQL TIME)
            from datetime import timedelta
            if isinstance(t, timedelta):
                total_seconds = int(t.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            return str(t)
        
        return {
            'id': self.id,
            'num_trabajador': self.num_trabajador,
            'departamento': self.departamento,
            'nombre_trabajador': self.nombre_trabajador,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'turno_id': self.turno_id,
            'horario_texto': self.horario_texto,
            'codigo_incidencia': self.codigo_incidencia,
            'tipo_movimiento': self.tipo_movimiento,
            'movimiento_id': self.movimiento_id,
            'checada1': time_to_str(self.checada1),
            'checada2': time_to_str(self.checada2),
            'checada3': time_to_str(self.checada3),
            'checada4': time_to_str(self.checada4),
            'minutos_retardo': self.minutos_retardo,
            'horas_trabajadas': float(self.horas_trabajadas),
            'descripcion_incidencia': self.descripcion_incidencia,
            'fecha_procesamiento': self.fecha_procesamiento.isoformat() if self.fecha_procesamiento else None,
            'procesado_por': self.procesado_por
        }
    
    def __repr__(self):
        return f"<BitacoraRecord {self.num_trabajador} - {self.fecha} - {self.codigo_incidencia}>"
