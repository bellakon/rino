"""
Modelos de dominio para el módulo de movimientos
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import json


@dataclass
class CampoPersonalizado:
    """Campo personalizado configurable para un tipo de movimiento"""
    nombre: str
    tipo: str  # file, text, textarea, number, date
    requerido: bool
    label: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'nombre': self.nombre,
            'tipo': self.tipo,
            'requerido': self.requerido,
            'label': self.label
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CampoPersonalizado':
        return CampoPersonalizado(
            nombre=data['nombre'],
            tipo=data['tipo'],
            requerido=data['requerido'],
            label=data['label']
        )


@dataclass
class TipoMovimiento:
    """Tipo de movimiento del catálogo maestro"""
    nomenclatura: str
    nombre: str
    categoria: str
    letra: str  # A, B, C, D, E, F, G
    id: Optional[int] = None
    descripcion: Optional[str] = None
    campos_personalizados: List[CampoPersonalizado] = field(default_factory=list)
    activo: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def get_campos_json(self) -> Optional[str]:
        """Convierte los campos personalizados a JSON para almacenar en BD"""
        if not self.campos_personalizados:
            return None
        return json.dumps([campo.to_dict() for campo in self.campos_personalizados])
    
    def set_campos_from_json(self, json_str: Optional[str]):
        """Carga los campos personalizados desde JSON de BD"""
        if not json_str:
            self.campos_personalizados = []
            return
        
        try:
            data = json.loads(json_str) if isinstance(json_str, str) else json_str
            self.campos_personalizados = [CampoPersonalizado.from_dict(c) for c in data]
        except (json.JSONDecodeError, KeyError, TypeError):
            self.campos_personalizados = []
    
    def validar(self) -> tuple[bool, Optional[str]]:
        """Valida la entidad"""
        if not self.nomenclatura or len(self.nomenclatura.strip()) == 0:
            return False, "La nomenclatura es obligatoria"
        
        if len(self.nomenclatura) > 20:
            return False, "La nomenclatura no puede exceder 20 caracteres"
        
        if not self.nombre or len(self.nombre.strip()) == 0:
            return False, "El nombre es obligatorio"
        
        if not self.categoria or len(self.categoria.strip()) == 0:
            return False, "La categoría es obligatoria"
        
        if not self.letra or len(self.letra.strip()) == 0:
            return False, "La letra es obligatoria"
        
        categorias_validas = ['Comisión', 'Licencia', 'Permiso', 'Autorización', 'Capacitación', 'Otros']
        if self.categoria not in categorias_validas:
            return False, f"Categoría inválida. Debe ser una de: {', '.join(categorias_validas)}"
        
        return True, None


@dataclass
class Movimiento:
    """Movimiento aplicado a un trabajador"""
    num_trabajador: int
    tipo_movimiento_id: int
    fecha_inicio: datetime.date
    fecha_fin: datetime.date
    id: Optional[int] = None
    observaciones: Optional[str] = None
    datos_personalizados: Dict[str, Any] = field(default_factory=dict)
    usuario_registro: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Campos relacionados
    tipo_nomenclatura: Optional[str] = field(default=None, repr=False)
    tipo_nombre: Optional[str] = field(default=None, repr=False)
    trabajador_nombre: Optional[str] = field(default=None, repr=False)
    
    def get_datos_json(self) -> Optional[str]:
        """Convierte los datos personalizados a JSON para almacenar en BD"""
        if not self.datos_personalizados:
            return None
        return json.dumps(self.datos_personalizados)
    
    def set_datos_from_json(self, json_str: Optional[str]):
        """Carga los datos personalizados desde JSON de BD"""
        if not json_str:
            self.datos_personalizados = {}
            return
        
        try:
            self.datos_personalizados = json.loads(json_str) if isinstance(json_str, str) else json_str
        except (json.JSONDecodeError, TypeError):
            self.datos_personalizados = {}
    
    def validar(self) -> tuple[bool, Optional[str]]:
        """Valida la entidad"""
        if not self.num_trabajador or self.num_trabajador <= 0:
            return False, "El número de trabajador es obligatorio"
        
        if not self.tipo_movimiento_id or self.tipo_movimiento_id <= 0:
            return False, "El tipo de movimiento es obligatorio"
        
        if not self.fecha_inicio:
            return False, "La fecha de inicio es obligatoria"
        
        if not self.fecha_fin:
            return False, "La fecha fin es obligatoria"
        
        if self.fecha_fin < self.fecha_inicio:
            return False, "La fecha fin no puede ser anterior a la fecha de inicio"
        
        return True, None
