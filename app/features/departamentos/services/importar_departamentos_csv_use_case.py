"""
Caso de uso: Importar Departamentos desde CSV
Responsabilidad: Leer CSV y crear departamentos en la BD
"""
import csv
import io
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection
from app.shared.models.departamento import Departamento
from app.features.departamentos.services.crear_departamento_use_case import crear_departamento_use_case


class ImportarDepartamentosCSVUseCase:
    """Importa departamentos desde archivo CSV"""
    
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, archivo_csv):
        """
        Importa departamentos desde CSV
        
        CSV debe tener columnas: num_departamento,nombre,nomenclatura,activo
        
        Args:
            archivo_csv: FileStorage del archivo CSV
            
        Returns:
            tuple: (resultado_dict, error)
        """
        try:
            # Leer contenido del archivo
            contenido = archivo_csv.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(contenido))
            
            # Validar columnas requeridas
            columnas_requeridas = {'num_departamento', 'nombre', 'nomenclatura', 'activo'}
            columnas_csv = set(csv_reader.fieldnames)
            
            if not columnas_requeridas.issubset(columnas_csv):
                faltantes = columnas_requeridas - columnas_csv
                return None, f"Faltan columnas en el CSV: {', '.join(faltantes)}"
            
            # Procesar cada fila
            total = 0
            insertados = 0
            duplicados = 0
            errores = []
            
            for idx, fila in enumerate(csv_reader, start=2):  # start=2 porque fila 1 es header
                total += 1
                
                try:
                    # Validar campos
                    if not fila['num_departamento'] or not fila['nombre']:
                        errores.append(f"Fila {idx}: num_departamento y nombre son obligatorios")
                        continue
                    
                    # Convertir activo a boolean
                    activo_str = str(fila['activo']).strip().lower()
                    activo = activo_str in ['1', 'true', 'si', 'sí', 's', 'yes', 'y']
                    
                    # Crear objeto Departamento
                    departamento = Departamento(
                        num_departamento=int(fila['num_departamento']),
                        nombre=fila['nombre'].strip(),
                        nomenclatura=fila['nomenclatura'].strip() if fila['nomenclatura'] else '',
                        activo=activo
                    )
                    
                    # Intentar crear
                    id_insertado, error = crear_departamento_use_case.ejecutar(departamento)
                    
                    if error:
                        if 'Ya existe' in error:
                            duplicados += 1
                        else:
                            errores.append(f"Fila {idx}: {error}")
                    else:
                        insertados += 1
                        
                except ValueError as ve:
                    errores.append(f"Fila {idx}: Error de formato - {str(ve)}")
                except Exception as e:
                    errores.append(f"Fila {idx}: {str(e)}")
            
            resultado = {
                'total': total,
                'insertados': insertados,
                'duplicados': duplicados,
                'errores': errores,
                'error_count': len(errores)
            }
            
            return resultado, None
            
        except Exception as e:
            return None, f"Error al procesar CSV: {str(e)}"


# Instancia singleton
importar_departamentos_csv_use_case = ImportarDepartamentosCSVUseCase()
