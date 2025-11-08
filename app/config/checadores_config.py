"""
Configuración de checadores ZKTeco
Lista de dispositivos disponibles
"""


class CheckadoresConfig:
    """
    Configuración de checadores ZKTeco
    Edita aquí para agregar, modificar o eliminar checadores
    """
    
    # Lista de checadores disponibles
    CHECADORES = [
        {
            'id': 'docentes_1',
            'nombre': 'DOCENTES ACB',
            'ip': '10.10.18.11',
            'puerto': 4370,
            'ubicacion': 'Edificio ACB',
            'activo': True
        },
    ]
    
    # Timeout para conexión (segundos)
    TIMEOUT = 5
    
    # Reintentos de conexión
    MAX_RETRIES = 3
    
    @classmethod
    def get_checadores_activos(cls):
        """Retorna solo los checadores activos"""
        return [c for c in cls.CHECADORES if c.get('activo', True)]
    
    @classmethod
    def get_checador_by_id(cls, checador_id):
        """Obtiene un checador por su ID"""
        return next((c for c in cls.CHECADORES if c['id'] == checador_id), None)
    
    @classmethod
    def get_checador_by_ip(cls, ip):
        """Obtiene un checador por su IP"""
        return next((c for c in cls.CHECADORES if c['ip'] == ip), None)
