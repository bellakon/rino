"""
Caso de uso: Importar trabajadores desde CSV
Responsabilidad: Leer CSV y insertar trabajadores sin duplicar
"""
from app.core.database.query_executor import query_executor
import csv
import io


class ImportarTrabajadoresUseCase:
    """Importa trabajadores desde archivo CSV"""
    
    def ejecutar(self, archivo_csv):
        """
        Lee CSV y inserta trabajadores en la base de datos
        
        Args:
            archivo_csv: FileStorage object del archivo CSV
        
        Returns:
            tuple: (dict con resultados, error)
        """
        try:
            # Leer contenido del archivo y manejar BOM UTF-8
            contenido = archivo_csv.stream.read()
            
            # Intentar decodificar con UTF-8-sig (maneja BOM automáticamente)
            try:
                texto = contenido.decode("utf-8-sig")
            except UnicodeDecodeError:
                # Fallback a latin-1 si UTF-8 falla
                texto = contenido.decode("latin-1")
            
            stream = io.StringIO(texto, newline=None)
            csv_reader = csv.DictReader(stream)
            
            # Preparar lista de trabajadores
            trabajadores_lista = []
            filas_procesadas = 0
            filas_ignoradas = 0
            
            for row in csv_reader:
                filas_procesadas += 1
                # Verificar que las columnas existen y tienen valores
                if 'num' in row and 'nombre' in row and row['num'] and row['nombre']:
                    try:
                        trabajadores_lista.append({
                            'num_trabajador': int(row['num'].strip()),
                            'nombre': row['nombre'].strip(),
                            'email': row.get('email', '').strip() or None,  # Nueva columna opcional
                            'activo': 1
                        })
                    except ValueError:
                        # Ignorar filas con num_trabajador inválido
                        filas_ignoradas += 1
                        continue
                else:
                    filas_ignoradas += 1
            
            if not trabajadores_lista:
                return None, f"El archivo CSV está vacío o no tiene el formato correcto. Filas procesadas: {filas_procesadas}, ignoradas: {filas_ignoradas}. Verifique que las columnas se llamen 'num', 'nombre' y opcionalmente 'email'"
            
            # Insertar en lotes usando query_executor
            query = """
                INSERT INTO trabajadores (num_trabajador, nombre, email, activo)
                VALUES (%(num_trabajador)s, %(nombre)s, %(email)s, %(activo)s)
            """
            
            registros_insertados, error = query_executor.ejecutar_batch(
                query, 
                trabajadores_lista,
                ignore_duplicates=True
            )
            
            if error:
                return None, error
            
            duplicados = len(trabajadores_lista) - registros_insertados
            
            return {
                'total_leidos': len(trabajadores_lista),
                'insertados': registros_insertados,
                'duplicados': duplicados
            }, None
            
        except Exception as e:
            return None, f"Error al procesar CSV: {str(e)}"


# Instancia singleton
importar_trabajadores_use_case = ImportarTrabajadoresUseCase()
