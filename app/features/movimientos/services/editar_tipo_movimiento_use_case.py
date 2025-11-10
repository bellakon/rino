"""
Caso de uso: Editar Tipo de Movimiento
Responsabilidad: Actualizar un tipo de movimiento existente
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.movimientos.models.movimiento_models import TipoMovimiento
from app.config.movimientos_config import get_letras_values
from typing import Tuple, Optional


class EditarTipoMovimientoUseCase:
    """Edita un tipo de movimiento existente"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, tipo_id: int, tipo: TipoMovimiento) -> Tuple[bool, Optional[str]]:
        """
        Edita un tipo de movimiento
        
        Args:
            tipo_id: ID del tipo a editar
            tipo: Objeto TipoMovimiento con nuevos datos
            
        Returns:
            tuple: (exito, mensaje_error)
        """
        try:
            # Validar modelo
            valido, mensaje = tipo.validar()
            if not valido:
                return False, mensaje
            
            # Validar que la letra sea válida
            if tipo.letra not in get_letras_values():
                return False, f"Letra inválida. Debe ser una de: {', '.join(get_letras_values())}"
            
            # Verificar que el tipo existe
            query_existe = "SELECT id FROM tipos_movimientos WHERE id = %s"
            resultado, error = self.query_executor.ejecutar(query_existe, (tipo_id,))
            
            if error:
                return False, error
            
            if not resultado:
                return False, "Tipo de movimiento no encontrado"
            
            # Verificar que la nomenclatura no esté en uso por otro tipo
            query_duplicado = "SELECT id FROM tipos_movimientos WHERE nomenclatura = %s AND id != %s"
            resultado, error = self.query_executor.ejecutar(query_duplicado, (tipo.nomenclatura, tipo_id))
            
            if error:
                return False, error
            
            if resultado:
                return False, f"La nomenclatura '{tipo.nomenclatura}' ya está en uso"
            
            # Actualizar
            query = """
                UPDATE tipos_movimientos
                SET nomenclatura = %s,
                    nombre = %s,
                    descripcion = %s,
                    categoria = %s,
                    letra = %s,
                    campos_personalizados = %s,
                    activo = %s
                WHERE id = %s
            """
            params = (
                tipo.nomenclatura.strip().upper(),
                tipo.nombre.strip(),
                tipo.descripcion.strip() if tipo.descripcion else None,
                tipo.categoria,
                tipo.letra.upper(),
                tipo.get_campos_json(),
                1 if tipo.activo else 0,
                tipo_id
            )
            
            resultado, error = self.query_executor.ejecutar(query, params)
            
            if error:
                return False, error
            
            return True, None
            
        except Exception as e:
            return False, f"Error al editar tipo de movimiento: {str(e)}"


# Instancia singleton
editar_tipo_movimiento_use_case = EditarTipoMovimientoUseCase()
