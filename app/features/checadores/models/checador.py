"""
Modelo: Checador
Representa un dispositivo ZKTeco
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Checador:
    """Modelo simple de Checador - mapea a checadores_config"""
    
    id: str  # ID único del checador
    nombre: str
    ip: str
    puerto: int
    ubicacion: str
    activo: bool = True
    
    def to_dict(self):
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'ip': self.ip,
            'puerto': self.puerto,
            'ubicacion': self.ubicacion,
            'activo': self.activo
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea desde diccionario"""
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre'),
            ip=data.get('ip'),
            puerto=data.get('puerto', 4370),
            ubicacion=data.get('ubicacion'),
            activo=data.get('activo', True)
        )
from dataclasses import dataclass
from typing import Optional


@dataclass
class Checador:
    """Modelo simple de Checador"""
    
    ip: str
    nombre: str
    ubicacion: str
    id: Optional[str] = None
    puerto: int = 4370
    serie: Optional[str] = None
    activo: bool = True
    
    def to_dict(self):
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'ip': self.ip,
            'nombre': self.nombre,
            'ubicacion': self.ubicacion,
            'puerto': self.puerto,
            'serie': self.serie,
            'activo': self.activo
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea desde diccionario"""
        return cls(
            id=data.get('id'),
            ip=data.get('ip'),
            nombre=data.get('nombre'),
            ubicacion=data.get('ubicacion'),
            puerto=data.get('puerto', 4370),
            serie=data.get('serie'),
            activo=data.get('activo', True)
        )
