"""
Caso de uso: Crear Tipo de Movimiento
Responsabilidad: Insertar un nuevo tipo de movimiento en la BD
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.features.movimientos.models.movimiento_models import TipoMovimiento
from app.config.movimientos_config import get_letras_values


class CrearTipoMovimientoUseCase:
    """Crea un nuevo tipo de movimiento"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, tipo: TipoMovimiento):
        """
        Crea un tipo de movimiento en la BD
        
        Args:
            tipo: Objeto TipoMovimiento
            
        Returns:
            tuple: (id_insertado, error)
        """
        try:
            # Validar modelo
            valido, mensaje = tipo.validar()
            if not valido:
                return None, mensaje
            
            # Validar que la letra sea válida
            if tipo.letra not in get_letras_values():
                return None, f"Letra inválida. Debe ser una de: {', '.join(get_letras_values())}"
            
            # Verificar que no exista la nomenclatura
            query_existe = "SELECT id FROM tipos_movimientos WHERE nomenclatura = %s"
            resultado, error = self.query_executor.ejecutar(query_existe, (tipo.nomenclatura,))
            
            if error:
                return None, error
            
            if resultado and len(resultado) > 0:
                return None, f"Ya existe un tipo de movimiento con nomenclatura '{tipo.nomenclatura}'"
            
            # Insertar
            query = """
                INSERT INTO tipos_movimientos 
                (nomenclatura, nombre, descripcion, categoria, letra, campos_personalizados, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                tipo.nomenclatura.strip().upper(),
                tipo.nombre.strip(),
                tipo.descripcion.strip() if tipo.descripcion else None,
                tipo.categoria,
                tipo.letra.upper(),
                tipo.get_campos_json(),
                1 if tipo.activo else 0
            )
            
            resultado, error = self.query_executor.ejecutar(query, params)
            
            if error:
                return None, error
            
            # El QueryExecutor devuelve {'affected_rows': n} para INSERT
            # Necesitamos obtener el last_insert_id
            query_id = "SELECT LAST_INSERT_ID() as id"
            resultado_id, error = self.query_executor.ejecutar(query_id)
            
            if error or not resultado_id:
                return None, "Error al obtener ID insertado"
            
            tipo_id = resultado_id[0]['id']
            print(f"[CREAR TIPO MOVIMIENTO] ID={tipo_id}, Nomenclatura={tipo.nomenclatura}")
            
            return tipo_id, None
            
        except Exception as e:
            return None, f"Error al crear tipo de movimiento: {str(e)}"


# Instancia singleton
crear_tipo_movimiento_use_case = CrearTipoMovimientoUseCase()
