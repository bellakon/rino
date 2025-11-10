"""
Modelo: PlantillaHorario
Representa una plantilla de horario reutilizable
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class PlantillaHorario:
    """Modelo de Plantilla de Horario"""
    
    nombre_horario: str
    descripcion_horario: str
    # Lunes
    lunes_entrada_1: Optional[str] = None  # HH:MM
    lunes_salida_1: Optional[str] = None
    lunes_entrada_2: Optional[str] = None
    lunes_salida_2: Optional[str] = None
    # Martes
    martes_entrada_1: Optional[str] = None
    martes_salida_1: Optional[str] = None
    martes_entrada_2: Optional[str] = None
    martes_salida_2: Optional[str] = None
    # Miércoles
    miercoles_entrada_1: Optional[str] = None
    miercoles_salida_1: Optional[str] = None
    miercoles_entrada_2: Optional[str] = None
    miercoles_salida_2: Optional[str] = None
    # Jueves
    jueves_entrada_1: Optional[str] = None
    jueves_salida_1: Optional[str] = None
    jueves_entrada_2: Optional[str] = None
    jueves_salida_2: Optional[str] = None
    # Viernes
    viernes_entrada_1: Optional[str] = None
    viernes_salida_1: Optional[str] = None
    viernes_entrada_2: Optional[str] = None
    viernes_salida_2: Optional[str] = None
    # Sábado
    sabado_entrada_1: Optional[str] = None
    sabado_salida_1: Optional[str] = None
    sabado_entrada_2: Optional[str] = None
    sabado_salida_2: Optional[str] = None
    # Domingo
    domingo_entrada_1: Optional[str] = None
    domingo_salida_1: Optional[str] = None
    domingo_entrada_2: Optional[str] = None
    domingo_salida_2: Optional[str] = None
    
    activo: bool = True
    id: Optional[int] = None
    
    def to_dict(self):
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'nombre_horario': self.nombre_horario,
            'descripcion_horario': self.descripcion_horario,
            'lunes_entrada_1': self.lunes_entrada_1,
            'lunes_salida_1': self.lunes_salida_1,
            'lunes_entrada_2': self.lunes_entrada_2,
            'lunes_salida_2': self.lunes_salida_2,
            'martes_entrada_1': self.martes_entrada_1,
            'martes_salida_1': self.martes_salida_1,
            'martes_entrada_2': self.martes_entrada_2,
            'martes_salida_2': self.martes_salida_2,
            'miercoles_entrada_1': self.miercoles_entrada_1,
            'miercoles_salida_1': self.miercoles_salida_1,
            'miercoles_entrada_2': self.miercoles_entrada_2,
            'miercoles_salida_2': self.miercoles_salida_2,
            'jueves_entrada_1': self.jueves_entrada_1,
            'jueves_salida_1': self.jueves_salida_1,
            'jueves_entrada_2': self.jueves_entrada_2,
            'jueves_salida_2': self.jueves_salida_2,
            'viernes_entrada_1': self.viernes_entrada_1,
            'viernes_salida_1': self.viernes_salida_1,
            'viernes_entrada_2': self.viernes_entrada_2,
            'viernes_salida_2': self.viernes_salida_2,
            'sabado_entrada_1': self.sabado_entrada_1,
            'sabado_salida_1': self.sabado_salida_1,
            'sabado_entrada_2': self.sabado_entrada_2,
            'sabado_salida_2': self.sabado_salida_2,
            'domingo_entrada_1': self.domingo_entrada_1,
            'domingo_salida_1': self.domingo_salida_1,
            'domingo_entrada_2': self.domingo_entrada_2,
            'domingo_salida_2': self.domingo_salida_2,
            'activo': self.activo
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea desde diccionario"""
        return cls(
            id=data.get('id'),
            nombre_horario=data.get('nombre_horario'),
            descripcion_horario=data.get('descripcion_horario'),
            lunes_entrada_1=data.get('lunes_entrada_1'),
            lunes_salida_1=data.get('lunes_salida_1'),
            lunes_entrada_2=data.get('lunes_entrada_2'),
            lunes_salida_2=data.get('lunes_salida_2'),
            martes_entrada_1=data.get('martes_entrada_1'),
            martes_salida_1=data.get('martes_salida_1'),
            martes_entrada_2=data.get('martes_entrada_2'),
            martes_salida_2=data.get('martes_salida_2'),
            miercoles_entrada_1=data.get('miercoles_entrada_1'),
            miercoles_salida_1=data.get('miercoles_salida_1'),
            miercoles_entrada_2=data.get('miercoles_entrada_2'),
            miercoles_salida_2=data.get('miercoles_salida_2'),
            jueves_entrada_1=data.get('jueves_entrada_1'),
            jueves_salida_1=data.get('jueves_salida_1'),
            jueves_entrada_2=data.get('jueves_entrada_2'),
            jueves_salida_2=data.get('jueves_salida_2'),
            viernes_entrada_1=data.get('viernes_entrada_1'),
            viernes_salida_1=data.get('viernes_salida_1'),
            viernes_entrada_2=data.get('viernes_entrada_2'),
            viernes_salida_2=data.get('viernes_salida_2'),
            sabado_entrada_1=data.get('sabado_entrada_1'),
            sabado_salida_1=data.get('sabado_salida_1'),
            sabado_entrada_2=data.get('sabado_entrada_2'),
            sabado_salida_2=data.get('sabado_salida_2'),
            domingo_entrada_1=data.get('domingo_entrada_1'),
            domingo_salida_1=data.get('domingo_salida_1'),
            domingo_entrada_2=data.get('domingo_entrada_2'),
            domingo_salida_2=data.get('domingo_salida_2'),
            activo=data.get('activo', True)
        )
    
    def generar_hash_horario(self):
        """Genera un hash único basado en los horarios para detectar duplicados"""
        horarios_str = '|'.join([
            str(self.lunes_entrada_1 or ''), str(self.lunes_salida_1 or ''),
            str(self.lunes_entrada_2 or ''), str(self.lunes_salida_2 or ''),
            str(self.martes_entrada_1 or ''), str(self.martes_salida_1 or ''),
            str(self.martes_entrada_2 or ''), str(self.martes_salida_2 or ''),
            str(self.miercoles_entrada_1 or ''), str(self.miercoles_salida_1 or ''),
            str(self.miercoles_entrada_2 or ''), str(self.miercoles_salida_2 or ''),
            str(self.jueves_entrada_1 or ''), str(self.jueves_salida_1 or ''),
            str(self.jueves_entrada_2 or ''), str(self.jueves_salida_2 or ''),
            str(self.viernes_entrada_1 or ''), str(self.viernes_salida_1 or ''),
            str(self.viernes_entrada_2 or ''), str(self.viernes_salida_2 or ''),
            str(self.sabado_entrada_1 or ''), str(self.sabado_salida_1 or ''),
            str(self.sabado_entrada_2 or ''), str(self.sabado_salida_2 or ''),
            str(self.domingo_entrada_1 or ''), str(self.domingo_salida_1 or ''),
            str(self.domingo_entrada_2 or ''), str(self.domingo_salida_2 or '')
        ])
        import hashlib
        return hashlib.md5(horarios_str.encode()).hexdigest()
