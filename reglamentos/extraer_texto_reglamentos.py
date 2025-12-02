#!/usr/bin/env python3
"""
Script para extraer texto de los PDFs de reglamentos y generar un resumen
enfocado en reglas de asistencia, retardos, entradas, salidas, etc.
"""

import os
import sys
from pathlib import Path

# Intentar importar PyPDF2 o pypdf
try:
    import PyPDF2
    PDF_LIB = 'PyPDF2'
except ImportError:
    try:
        import pypdf
        PDF_LIB = 'pypdf'
    except ImportError:
        print("ERROR: No se encontró ninguna librería de PDF instalada")
        print("Instala una de estas opciones:")
        print("  pip install PyPDF2")
        print("  pip install pypdf")
        sys.exit(1)

def extraer_texto_pdf(ruta_pdf):
    """
    Extrae texto de un archivo PDF
    
    Args:
        ruta_pdf: Ruta al archivo PDF
        
    Returns:
        str: Texto extraído del PDF
    """
    try:
        texto_completo = []
        
        with open(ruta_pdf, 'rb') as archivo:
            if PDF_LIB == 'PyPDF2':
                lector = PyPDF2.PdfReader(archivo)
                num_paginas = len(lector.pages)
                
                print(f"  Procesando {num_paginas} páginas...")
                
                for i, pagina in enumerate(lector.pages, 1):
                    texto = pagina.extract_text()
                    if texto:
                        texto_completo.append(f"\n--- PÁGINA {i} ---\n")
                        texto_completo.append(texto)
            else:  # pypdf
                import pypdf
                lector = pypdf.PdfReader(archivo)
                num_paginas = len(lector.pages)
                
                print(f"  Procesando {num_paginas} páginas...")
                
                for i, pagina in enumerate(lector.pages, 1):
                    texto = pagina.extract_text()
                    if texto:
                        texto_completo.append(f"\n--- PÁGINA {i} ---\n")
                        texto_completo.append(texto)
        
        return '\n'.join(texto_completo)
        
    except Exception as e:
        return f"ERROR al procesar PDF: {str(e)}"


def buscar_secciones_relevantes(texto, nombre_archivo):
    """
    Busca y extrae secciones relevantes sobre asistencia
    
    Args:
        texto: Texto completo del PDF
        nombre_archivo: Nombre del archivo para contexto
        
    Returns:
        str: Secciones relevantes encontradas
    """
    # Palabras clave para buscar secciones relevantes
    palabras_clave = [
        'asistencia', 'retardo', 'falta', 'entrada', 'salida',
        'puntualidad', 'horario', 'checada', 'registro',
        'tolerancia', 'minutos', 'incidencia', 'justificación',
        'permiso', 'licencia', 'ausencia', 'tardanza'
    ]
    
    lineas = texto.split('\n')
    secciones_relevantes = []
    
    # Buscar líneas que contengan palabras clave
    for i, linea in enumerate(lineas):
        linea_lower = linea.lower()
        
        for palabra in palabras_clave:
            if palabra in linea_lower:
                # Incluir contexto (líneas antes y después)
                inicio = max(0, i - 2)
                fin = min(len(lineas), i + 5)
                contexto = '\n'.join(lineas[inicio:fin])
                
                if contexto not in secciones_relevantes:
                    secciones_relevantes.append(contexto)
                break
    
    if secciones_relevantes:
        return '\n\n' + '='*80 + '\n\n'.join(secciones_relevantes)
    else:
        return "\n(No se encontraron secciones con palabras clave relevantes)"


def main():
    """Función principal"""
    directorio_actual = Path(__file__).parent
    
    print("="*80)
    print("EXTRACTOR DE TEXTO DE REGLAMENTOS")
    print("="*80)
    print(f"\nBuscando PDFs en: {directorio_actual}\n")
    
    # Buscar todos los archivos PDF
    archivos_pdf = list(directorio_actual.glob('*.pdf'))
    
    if not archivos_pdf:
        print("No se encontraron archivos PDF en el directorio")
        return
    
    print(f"Se encontraron {len(archivos_pdf)} archivos PDF:\n")
    for pdf in archivos_pdf:
        print(f"  - {pdf.name}")
    
    print("\n" + "="*80 + "\n")
    
    # Archivo de salida
    archivo_salida = directorio_actual / 'resumen_reglamentos_asistencias.txt'
    
    with open(archivo_salida, 'w', encoding='utf-8') as salida:
        salida.write("="*80 + "\n")
        salida.write("RESUMEN DE REGLAMENTOS - ASPECTOS DE ASISTENCIA\n")
        salida.write("="*80 + "\n")
        salida.write(f"\nGenerado automáticamente desde {len(archivos_pdf)} archivos PDF\n")
        salida.write(f"Librería usada: {PDF_LIB}\n")
        salida.write("\nPalabras clave buscadas: asistencia, retardo, falta, entrada, salida,\n")
        salida.write("puntualidad, horario, tolerancia, minutos, incidencia, etc.\n")
        salida.write("\n" + "="*80 + "\n\n")
        
        # Procesar cada PDF
        for pdf in archivos_pdf:
            print(f"Procesando: {pdf.name}")
            
            salida.write("\n\n" + "#"*80 + "\n")
            salida.write(f"# ARCHIVO: {pdf.name}\n")
            salida.write("#"*80 + "\n")
            
            # Extraer texto completo
            texto_completo = extraer_texto_pdf(pdf)
            
            # Guardar texto completo
            salida.write("\n--- TEXTO COMPLETO ---\n")
            salida.write(texto_completo)
            
            # Buscar y guardar secciones relevantes
            salida.write("\n\n--- SECCIONES RELEVANTES (filtradas por palabras clave) ---\n")
            secciones = buscar_secciones_relevantes(texto_completo, pdf.name)
            salida.write(secciones)
            
            print(f"  ✓ Completado: {pdf.name}\n")
    
    print("="*80)
    print(f"\n✓ PROCESO COMPLETADO\n")
    print(f"Archivo generado: {archivo_salida}")
    print(f"Puedes revisarlo con: cat {archivo_salida.name}")
    print("\n" + "="*80)


if __name__ == '__main__':
    main()
