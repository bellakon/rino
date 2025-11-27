"""
Script para importar tipos de movimientos desde CSV a la base de datos
"""
import csv
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database.connection import DatabaseConnection

def importar_movimientos():
    """Importa los movimientos desde el archivo CSV"""
    
    db_connection = DatabaseConnection('sistema')
    
    try:
        print("📂 Leyendo archivo CSV...")
        
        # Leer el archivo CSV
        with open('importar.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            movimientos = list(reader)
        
        print(f"✅ Se encontraron {len(movimientos)} movimientos en el CSV\n")
        
        with db_connection.get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar si ya existen movimientos
            cursor.execute("SELECT COUNT(*) as total FROM tipos_movimientos")
            resultado = cursor.fetchone()
            total_actual = resultado[0]
            
            if total_actual > 0:
                print(f"⚠️  Ya existen {total_actual} movimientos en la base de datos")
                respuesta = input("¿Deseas eliminarlos e importar los nuevos? (s/n): ")
                
                if respuesta.lower() == 's':
                    cursor.execute("DELETE FROM tipos_movimientos")
                    print("🗑️  Movimientos existentes eliminados\n")
                else:
                    print("❌ Importación cancelada")
                    return
            
            # Preparar la consulta de inserción
            query = """
                INSERT INTO tipos_movimientos 
                (nomenclatura, nombre, descripcion, categoria, letra, campos_personalizados, activo)
                VALUES (%s, %s, %s, %s, %s, %s, 1)
            """
            
            # Insertar cada movimiento
            insertados = 0
            errores = 0
            
            for mov in movimientos:
                try:
                    cursor.execute(query, (
                        mov['nomenclatura'].strip(),
                        mov['nombre'].strip(),
                        mov['descripcion'].strip(),
                        mov['categoria'].strip(),
                        mov['letra'].strip(),
                        mov['campos_personalizados'].strip()
                    ))
                    insertados += 1
                    print(f"✅ Insertado: {mov['nomenclatura']} - {mov['nombre']}")
                except Exception as e:
                    errores += 1
                    print(f"❌ Error al insertar {mov['nomenclatura']}: {e}")
            
            print(f"\n{'='*60}")
            print(f"📊 RESUMEN DE IMPORTACIÓN")
            print(f"{'='*60}")
            print(f"✅ Movimientos insertados: {insertados}")
            print(f"❌ Errores: {errores}")
            print(f"📈 Total en base de datos: {insertados}")
            print(f"{'='*60}\n")
            
            # Mostrar algunos ejemplos
            cursor.execute("SELECT * FROM tipos_movimientos LIMIT 5")
            ejemplos = cursor.fetchall()
            
            print("📋 Ejemplos de movimientos importados:")
            for mov in ejemplos:
                print(f"   {mov[1]:8} - {mov[2]}")  # nomenclatura - nombre
            
            print("\n✅ Importación completada exitosamente!")
        
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo 'importar.csv'")
        print("   Asegúrate de que el archivo esté en la raíz del proyecto")
    except Exception as e:
        print(f"❌ Error durante la importación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔄 IMPORTACIÓN DE TIPOS DE MOVIMIENTOS")
    print("="*60 + "\n")
    
    importar_movimientos()
