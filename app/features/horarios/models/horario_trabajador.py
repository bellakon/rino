"""
Modelo: HorarioTrabajador
Representa la asignación de un horario a un trabajador
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class HorarioTrabajador:
    """Modelo de Asignación de Horario a Trabajador"""
    
    num_trabajador: int
    plantilla_horario_id: int
    fecha_inicio_asignacion: str  # YYYY-MM-DD
    semestre: str
    fecha_fin_asignacion: Optional[str] = None  # YYYY-MM-DD
    estado_asignacion: str = 'activo'  # activo, inactivo
    activo_asignacion: bool = True
    id: Optional[int] = None
    
    # Campos extras del JOIN para mostrar
    nombre_completo: Optional[str] = None
    departamento: Optional[str] = None
    nombre_horario: Optional[str] = None
    descripcion_horario: Optional[str] = None
    
    def to_dict(self):
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'num_trabajador': self.num_trabajador,
            'plantilla_horario_id': self.plantilla_horario_id,
            'fecha_inicio_asignacion': self.fecha_inicio_asignacion,
            'fecha_fin_asignacion': self.fecha_fin_asignacion,
            'semestre': self.semestre,
            'estado_asignacion': self.estado_asignacion,
            'activo_asignacion': self.activo_asignacion,
            'nombre_completo': self.nombre_completo,
            'departamento': self.departamento,
            'nombre_horario': self.nombre_horario,
            'descripcion_horario': self.descripcion_horario
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea desde diccionario"""
        return cls(
            id=data.get('id'),
            num_trabajador=data.get('num_trabajador'),
            plantilla_horario_id=data.get('plantilla_horario_id'),
            fecha_inicio_asignacion=data.get('fecha_inicio_asignacion'),
            fecha_fin_asignacion=data.get('fecha_fin_asignacion'),
            semestre=data.get('semestre'),
            estado_asignacion=data.get('estado_asignacion', 'activo'),
            activo_asignacion=data.get('activo_asignacion', True),
            nombre_completo=data.get('nombre_completo'),
            departamento=data.get('departamento'),
            nombre_horario=data.get('nombre_horario'),
            descripcion_horario=data.get('descripcion_horario')
        )
