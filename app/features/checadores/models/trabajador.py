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
    departamento: Optional[str] = None
    tipoPlaza: Optional[str] = None
    ingresoSEPfecha: Optional[str] = None  # YYYY-MM-DD
    captura: Optional[str] = None  # YYYY-MM-DD
    id: Optional[int] = None
    
    def to_dict(self):
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'num_trabajador': self.num_trabajador,
            'nombre': self.nombre,
            'departamento': self.departamento,
            'tipoPlaza': self.tipoPlaza,
            'ingresoSEPfecha': self.ingresoSEPfecha,
            'captura': self.captura
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea desde diccionario"""
        return cls(
            id=data.get('id'),
            num_trabajador=data.get('num_trabajador'),
            nombre=data.get('nombre'),
            departamento=data.get('departamento'),
            tipoPlaza=data.get('tipoPlaza'),
            ingresoSEPfecha=data.get('ingresoSEPfecha'),
            captura=data.get('captura')
        )
