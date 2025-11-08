"""
Modelo: Trabajador
Representa un trabajador registrado en el sistema
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Trabajador:
    """Modelo de Trabajador"""
    
    num_trabajador: int
    nombre: str
    departamento_id: Optional[int] = None  # FK a tabla departamentos
    tipoPlaza: Optional[str] = None
    ingresoSEPfecha: Optional[str] = None  # YYYY-MM-DD
    captura: Optional[str] = None  # YYYY-MM-DD
    activo: Optional[bool] = True
    movimiento: Optional[str] = None
    id: Optional[int] = None
    
    def to_dict(self):
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'num_trabajador': self.num_trabajador,
            'nombre': self.nombre,
            'departamento_id': self.departamento_id,
            'tipoPlaza': self.tipoPlaza,
            'ingresoSEPfecha': self.ingresoSEPfecha,
            'captura': self.captura,
            'activo': self.activo,
            'movimiento': self.movimiento
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea desde diccionario"""
        return cls(
            id=data.get('id'),
            num_trabajador=data.get('num_trabajador'),
            nombre=data.get('nombre'),
            departamento_id=data.get('departamento_id'),
            tipoPlaza=data.get('tipoPlaza'),
            ingresoSEPfecha=data.get('ingresoSEPfecha'),
            captura=data.get('captura'),
            activo=data.get('activo', True),
            movimiento=data.get('movimiento')
        )
