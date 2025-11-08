"""
Modelo: Departamento
Representa un departamento de la institución
"""


class Departamento:
    """Modelo de Departamento"""
    
    def __init__(self, num_departamento, nombre, nomenclatura, activo=True, id=None):
        self.id = id
        self.num_departamento = num_departamento
        self.nombre = nombre
        self.nomenclatura = nomenclatura
        self.activo = activo
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'num_departamento': self.num_departamento,
            'nombre': self.nombre,
            'nomenclatura': self.nomenclatura,
            'activo': self.activo
        }
    
    @staticmethod
    def from_dict(data):
        """Crea un objeto Departamento desde un diccionario"""
        return Departamento(
            num_departamento=data.get('num_departamento'),
            nombre=data.get('nombre'),
            nomenclatura=data.get('nomenclatura'),
            activo=data.get('activo', True),
            id=data.get('id')
        )
