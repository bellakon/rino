"""
Caso de uso: Consultar checadores donde está registrado un trabajador
Responsabilidad: Verificar en qué checadores está registrado un trabajador específico
"""
from app.config.checadores_config import CheckadoresConfig
from app.features.checadores.services.checador_service import checador_service


class ConsultarChecadoresTrabajadorUseCase:
    """Consulta en qué checadores está registrado un trabajador"""
    
    def ejecutar(self, num_trabajador):
        """
        Verifica en cada checador activo si el trabajador está registrado
        
        Args:
            num_trabajador: Número del trabajador a buscar
        
        Returns:
            tuple: (lista de TODOS los checadores con estado de registro, error)
        """
        try:
            checadores_lista = []
            
            # Obtener todos los checadores activos (CheckadoresConfig.CHECADORES es una lista)
            for config in CheckadoresConfig.CHECADORES:
                if not config.get('activo', True):
                    continue
                
                checador_info = {
                    'id': config['id'],
                    'nombre': config['nombre'],
                    'ip': config['ip'],
                    'puerto': config['puerto'],
                    'ubicacion': config.get('ubicacion', ''),
                    'activo': config.get('activo', True),
                    'registrado': False,  # Por defecto no está registrado
                    'error_conexion': None
                }
                
                # Conectar al checador
                conn, error = checador_service.conectar(config['ip'], config['puerto'])
                
                if error or not conn:
                    checador_info['error_conexion'] = error or 'No se pudo conectar'
                    checadores_lista.append(checador_info)
                    continue
                
                try:
                    # Obtener usuarios del checador
                    usuarios = conn.get_users()
                    
                    # Verificar si el trabajador está registrado
                    for usuario in usuarios:
                        if int(usuario.user_id) == num_trabajador:
                            checador_info['registrado'] = True
                            break
                    
                finally:
                    checador_service.desconectar(conn)
                
                checadores_lista.append(checador_info)
            
            return checadores_lista, None
            
        except Exception as e:
            return None, f"Error al consultar checadores: {str(e)}"


# Instancia singleton
consultar_checadores_trabajador_use_case = ConsultarChecadoresTrabajadorUseCase()
