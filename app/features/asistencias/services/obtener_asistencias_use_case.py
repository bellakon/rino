"""
Caso de uso: Obtener asistencias
Responsabilidad: Ejecutar SELECT y convertir resultados a modelos
"""
from app.core.database.query_executor import query_executor
from app.features.asistencias.models import Asistencia


class ObtenerAsistenciasUseCase:
    """Obtiene asistencias de la base de datos y las convierte a modelos"""
    
    def ejecutar(self):
        """
        Ejecuta SELECT simple y convierte a modelos Asistencia
        
        Returns:
            tuple: (lista de objetos Asistencia, error)
        """
        query = "SELECT * FROM asistencias ORDER BY fecha DESC, hora DESC LIMIT 100"
        
        registros, error = query_executor.ejecutar(query)
        
        if error:
            return None, error
        
        # Convertir diccionarios a objetos Asistencia
        asistencias = [Asistencia.from_dict(reg) for reg in registros]
        
        return asistencias, None


# Instancia singleton
obtener_asistencias_use_case = ObtenerAsistenciasUseCase()
