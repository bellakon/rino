"""
Caso de uso: Verificar conexión de checadores
Responsabilidad: Obtener checadores y verificar su estado de conexión
"""
from app.config.checadores_config import CheckadoresConfig
from app.features.checadores.models import Checador
from app.features.checadores.services.checador_service import checador_service


class VerificarConexionUseCase:
    """Obtiene checadores y verifica su conexión"""
    
    def obtener_checadores(self):
        """
        Obtiene todos los checadores como modelos
        
        Returns:
            list: Lista de objetos Checador
        """
        checadores_config = CheckadoresConfig.CHECADORES
        return [Checador.from_dict(c) for c in checadores_config]
    
    def verificar_conexion(self, checador_id):
        """
        Verifica la conexión de un checador específico y obtiene información
        
        Args:
            checador_id (str): ID del checador
            
        Returns:
            tuple: (datos_checador, estado_conexion, info_dispositivo, error)
        """
        # Obtener configuración del checador
        config = CheckadoresConfig.get_checador_by_id(checador_id)
        
        if not config:
            return None, False, None, "Checador no encontrado"
        
        # Crear modelo
        checador = Checador.from_dict(config)
        
        # Verificar conexión y obtener información
        info_dispositivo, error_info = checador_service.obtener_info_dispositivo(
            checador.ip, 
            checador.puerto
        )
        
        if error_info:
            # Si falla obtener info, solo verificar conexión
            exito, error = checador_service.probar_conexion(
                checador.ip, 
                checador.puerto
            )
            return checador, exito, None, error
        
        return checador, True, info_dispositivo, None


# Instancia singleton
verificar_conexion_use_case = VerificarConexionUseCase()
