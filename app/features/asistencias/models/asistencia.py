"""
Modelo: Asistencia
Representa un registro de asistencia de un trabajador
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Asistencia:
    """Modelo simple de Asistencia"""
    
    num_trabajador: int
    fecha: str  # YYYY-MM-DD
    hora: str   # HH:MM:SS
    checador: str
    nombre: Optional[str] = None  # Nombre del trabajador del checador
    id: Optional[int] = None
    
    def to_dict(self):
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'num_trabajador': self.num_trabajador,
            'fecha': self.fecha,
            'hora': self.hora,
            'checador': self.checador,
            'nombre': self.nombre
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea desde diccionario"""
        return cls(
            id=data.get('id'),
            num_trabajador=data.get('num_trabajador'),
            fecha=data.get('fecha'),
            hora=data.get('hora'),
            checador=data.get('checador'),
            nombre=data.get('nombre')
        )
