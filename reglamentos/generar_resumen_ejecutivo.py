#!/usr/bin/env python3
"""
Script para generar un RESUMEN EJECUTIVO de las reglas de asistencia
a partir del texto extraído de los reglamentos
"""

import re
from pathlib import Path

def analizar_texto_reglamento(texto, nombre_archivo):
    """
    Analiza el texto y extrae información relevante sobre asistencias
    """
    lineas = texto.split('\n')
    reglas_encontradas = []
    
    # Patrones a buscar (más específicos)
    patrones = [
        (r'(\d+)\s*minutos?\s+(de\s+)?tolerancia', 'TOLERANCIA EN MINUTOS'),
        (r'retardo\s+de\s+(\d+)\s+a\s+(\d+)\s+minutos?', 'RANGO DE RETARDO'),
        (r'(\d+)\s*minutos?\s+(antes|después|tarde|temprano)', 'TIEMPO ESPECÍFICO'),
        (r'falta\s+injustificada', 'FALTA INJUSTIFICADA'),
        (r'tres\s+retardos?\s*=\s*una\s+falta', 'REGLA 3 RETARDOS = FALTA'),
        (r'(entrada|salida)\s+(a las|de las)?\s*(\d{1,2}):(\d{2})', 'HORARIO ESPECÍFICO'),
        (r'(checada|registro|marcar)\s+(entrada|salida)', 'CHECADA'),
        (r'jornada\s+de\s+trabajo', 'JORNADA LABORAL'),
        (r'(permiso|licencia)\s+(con|sin)\s+(goce|descuento)', 'PERMISOS/LICENCIAS'),
    ]
    
    for i, linea in enumerate(lineas):
        linea_lower = linea.lower().strip()
        
        # Saltar líneas vacías o muy cortas
        if len(linea_lower) < 10:
            continue
        
        for patron, categoria in patrones:
            if re.search(patron, linea_lower):
                # Obtener contexto (3 líneas antes y 3 después)
                inicio = max(0, i - 3)
                fin = min(len(lineas), i + 4)
                contexto = '\n'.join(lineas[inicio:fin])
                
                reglas_encontradas.append({
                    'categoria': categoria,
                    'texto': contexto,
                    'linea': i
                })
                break
    
    return reglas_encontradas


def main():
    directorio = Path('/home/ccomputo/projects/rino/reglamentos')
    archivo_entrada = directorio / 'resumen_reglamentos_asistencias.txt'
    archivo_salida = directorio / 'RESUMEN_EJECUTIVO_asistencias.txt'
    
    print("="*80)
    print("GENERANDO RESUMEN EJECUTIVO DE REGLAS DE ASISTENCIA")
    print("="*80)
    
    if not archivo_entrada.exists():
        print(f"ERROR: No se encontró {archivo_entrada}")
        return
    
    # Leer el archivo generado anteriormente
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Separar por archivos
    archivos = contenido.split('################################################################################')
    
    with open(archivo_salida, 'w', encoding='utf-8') as salida:
        salida.write("="*80 + "\n")
        salida.write("RESUMEN EJECUTIVO - REGLAS DE ASISTENCIA EN REGLAMENTOS\n")
        salida.write("="*80 + "\n\n")
        salida.write("Este documento contiene las secciones MÁS RELEVANTES sobre:\n")
        salida.write("- Tolerancias de entrada/salida\n")
        salida.write("- Definiciones de retardo\n")
        salida.write("- Cálculo de faltas\n")
        salida.write("- Horarios de trabajo\n")
        salida.write("- Permisos y licencias\n\n")
        salida.write("="*80 + "\n\n")
        
        for archivo in archivos[1:]:  # Saltar el encabezado
            if not archivo.strip():
                continue
            
            # Extraer nombre del archivo
            match = re.search(r'# ARCHIVO: (.+\.pdf)', archivo)
            if match:
                nombre_archivo = match.group(1)
                print(f"\nAnalizando: {nombre_archivo}")
                
                salida.write("\n" + "="*80 + "\n")
                salida.write(f"ARCHIVO: {nombre_archivo}\n")
                salida.write("="*80 + "\n\n")
                
                # Analizar el contenido
                reglas = analizar_texto_reglamento(archivo, nombre_archivo)
                
                if reglas:
                    print(f"  - Encontradas {len(reglas)} reglas relevantes")
                    
                    # Agrupar por categoría
                    por_categoria = {}
                    for regla in reglas:
                        cat = regla['categoria']
                        if cat not in por_categoria:
                            por_categoria[cat] = []
                        por_categoria[cat].append(regla['texto'])
                    
                    # Escribir agrupado
                    for categoria, textos in sorted(por_categoria.items()):
                        salida.write(f"\n>>> {categoria} <<<\n")
                        salida.write("-" * 80 + "\n")
                        
                        # Eliminar duplicados
                        textos_unicos = list(set(textos))
                        
                        for texto in textos_unicos[:3]:  # Máximo 3 por categoría
                            salida.write(f"\n{texto}\n")
                            salida.write("-" * 40 + "\n")
                else:
                    print(f"  - No se encontraron reglas específicas")
                    salida.write("\n(No se encontraron reglas específicas de asistencia)\n")
        
        # Agregar sección de recomendaciones
        salida.write("\n\n" + "="*80 + "\n")
        salida.write("RECOMENDACIONES PARA BITÁCORA\n")
        salida.write("="*80 + "\n\n")
        salida.write("Basado en el análisis de los reglamentos, considera:\n\n")
        salida.write("1. Verificar tolerancias de entrada (buscar menciones de '10 minutos', '15 minutos')\n")
        salida.write("2. Revisar si aplica la regla '3 retardos = 1 falta'\n")
        salida.write("3. Confirmar diferencias entre personal DOCENTE y NO DOCENTE\n")
        salida.write("4. Validar rangos de retardo menor vs retardo mayor\n")
        salida.write("5. Verificar si hay reglas especiales para salidas tempranas\n")
        salida.write("6. Revisar políticas de justificación de faltas\n\n")
    
    print("\n" + "="*80)
    print(f"\n✓ RESUMEN EJECUTIVO GENERADO")
    print(f"\nArchivo: {archivo_salida}")
    print(f"\nPara revisarlo:")
    print(f"  cat {archivo_salida.name}")
    print(f"  less {archivo_salida.name}")
    print("\n" + "="*80)


if __name__ == '__main__':
    main()
