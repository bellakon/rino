"""
Caso de uso: Consultar trabajadores registrados en checador
Responsabilidad: Obtener usuarios del checador y enriquecerlos con datos de BD
"""
from app.config.checadores_config import CheckadoresConfig
from app.features.checadores.models import Checador
from app.features.checadores.services.checador_service import checador_service
from app.core.database.query_executor import query_executor


class ConsultarTrabajadoresUseCase:
    """Consulta trabajadores registrados en checador con datos completos"""
    
    def ejecutar(self, checador_id):
        """
        Obtiene usuarios del checador y los enriquece con datos de trabajadores de BD
        
        Args:
            checador_id (str): ID del checador
            
        Returns:
            tuple: (checador, lista_trabajadores_enriquecidos, error)
        """
        # Obtener configuración del checador
        config = CheckadoresConfig.get_checador_by_id(checador_id)
        
        if not config:
            return None, None, "Checador no encontrado"
        
        checador = Checador.from_dict(config)
        
        # Obtener usuarios del checador
        usuarios_checador, error = checador_service.obtener_usuarios(
            checador.ip,
            checador.puerto
        )
        
        if error:
            return checador, None, error
        
        if not usuarios_checador:
            return checador, [], None
        
        # Obtener datos de trabajadores de la BD
        num_trabajadores = [u['user_id'] for u in usuarios_checador]
        placeholders = ','.join(['%s'] * len(num_trabajadores))
        
        query = f"SELECT * FROM trabajadores WHERE num_trabajador IN ({placeholders})"
        trabajadores_bd, error_bd = query_executor.ejecutar(query, num_trabajadores)
        
        # Crear diccionario de trabajadores por num_trabajador
        trabajadores_dict = {}
        if trabajadores_bd:
            trabajadores_dict = {t['num_trabajador']: t for t in trabajadores_bd}
        
        # Enriquecer usuarios del checador con datos de BD
        trabajadores_enriquecidos = []
        for usuario in usuarios_checador:
            num_trabajador = int(usuario['user_id'])
            trabajador_bd = trabajadores_dict.get(num_trabajador, {})
            
            trabajador_enriquecido = {
                'num_trabajador': num_trabajador,
                'nombre_checador': usuario['name'],
                'nombre': trabajador_bd.get('nombre', usuario['name']),
                'departamento': trabajador_bd.get('departamento'),
                'tipoPlaza': trabajador_bd.get('tipoPlaza'),
                'ingresoSEPfecha': trabajador_bd.get('ingresoSEPfecha'),
                'captura': trabajador_bd.get('captura'),
                'privilege': usuario['privilege'],
                'group_id': usuario['group_id'],
                'uid': usuario['uid'],
                'card': usuario.get('card'),
                'en_bd': num_trabajador in trabajadores_dict
            }
            
            trabajadores_enriquecidos.append(trabajador_enriquecido)
        
        return checador, trabajadores_enriquecidos, None


# Instancia singleton
consultar_trabajadores_use_case = ConsultarTrabajadoresUseCase()
