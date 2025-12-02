"""
Caso de uso: Generar PDF Masivo de Bitácora
Genera un PDF con reportes individuales de múltiples trabajadores
Cada trabajador tiene su propia sección con encabezado personalizado
"""
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict
from app.features.bitacora.services.listar_bitacora_use_case import listar_bitacora_use_case


class GenerarPdfMasivoBitacoraUseCase:
    """Genera PDF masivo con reportes individuales por trabajador"""
    
    def __init__(self):
        self.dias_semana = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        self.registros_por_pagina = 15
    
    def ejecutar(
        self,
        num_trabajadores: List[int],
        fecha_inicio: str,
        fecha_fin: str
    ) -> tuple[Optional[BytesIO], Optional[str]]:
        """
        Genera PDF masivo con reportes individuales
        
        Args:
            num_trabajadores: Lista de números de trabajadores
            fecha_inicio: Fecha inicio del periodo (YYYY-MM-DD)
            fecha_fin: Fecha fin del periodo (YYYY-MM-DD)
            
        Returns:
            tuple: (buffer con PDF, error)
        """
        try:
            # Crear buffer en memoria
            buffer = BytesIO()
            
            # Crear documento con orientación horizontal
            doc = SimpleDocTemplate(
                buffer,
                pagesize=landscape(letter),
                leftMargin=0.5*inch,
                rightMargin=0.5*inch,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch
            )
            
            elements = []
            
            # Crear estilos
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Normal'],
                fontSize=12,
                alignment=1,  # Centrado
                spaceAfter=10,
                spaceBefore=10
            )
            
            page_info_style = ParagraphStyle(
                'PageInfo',
                parent=styles['Normal'],
                fontSize=8,
                alignment=2  # Derecha
            )
            
            # Procesar cada trabajador
            total_trabajadores = len(num_trabajadores)
            
            for idx, num_trabajador in enumerate(num_trabajadores):
                # Obtener registros del trabajador
                # listar_bitacora_use_case.ejecutar() retorna List[BitacoraRecord], no tupla
                registros = listar_bitacora_use_case.ejecutar(
                    num_trabajador=num_trabajador,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin
                )
                
                if not registros:
                    print(f"[INFO] No hay registros para trabajador {num_trabajador}")
                    continue
                
                # Convertir a diccionarios
                registros_dict = [reg.to_dict() for reg in registros]
                
                # Filtrar días sin horario o con DESCANSO
                registros_filtrados = [
                    r for r in registros_dict 
                    if r.get('horario_texto') and r.get('horario_texto').upper() != 'DESCANSO'
                ]
                
                if not registros_filtrados:
                    continue
                
                # Obtener info del trabajador (del primer registro)
                primer_registro = registros_filtrados[0]
                nombre_trabajador = primer_registro.get('nombre_trabajador', '')
                
                # Procesar registros por páginas
                pagina_actual = 1
                total_registros = len(registros_filtrados)
                
                for i in range(0, total_registros, self.registros_por_pagina):
                    # Agregar encabezado personalizado para este trabajador
                    elements.extend(self._crear_encabezado_individual(
                        nombre_trabajador,
                        num_trabajador,
                        fecha_inicio,
                        fecha_fin,
                        title_style
                    ))
                    
                    # Obtener lote de registros
                    lote_registros = registros_filtrados[i:i + self.registros_por_pagina]
                    
                    # Crear tabla para este lote
                    tabla = self._crear_tabla(lote_registros)
                    elements.append(tabla)
                    
                    # Agregar información de página
                    elements.append(Spacer(1, 10))
                    elements.append(
                        Paragraph(
                            f"Trabajador {idx + 1}/{total_trabajadores} - HOJA #{pagina_actual}",
                            page_info_style
                        )
                    )
                    
                    # Agregar salto de página si no es la última página del trabajador
                    if i + self.registros_por_pagina < total_registros:
                        elements.append(PageBreak())
                        pagina_actual += 1
                
                # Salto de página entre trabajadores (si no es el último)
                if idx < total_trabajadores - 1:
                    elements.append(PageBreak())
            
            # Construir PDF
            if not elements:
                return None, "No hay registros para generar PDF"
            
            doc.build(elements)
            
            # Volver al inicio del buffer
            buffer.seek(0)
            
            return buffer, None
            
        except Exception as e:
            return None, f"Error al generar PDF masivo: {str(e)}"
    
    def _crear_encabezado_individual(
        self,
        nombre_trabajador: str,
        num_trabajador: int,
        fecha_inicio: str,
        fecha_fin: str,
        title_style
    ) -> list:
        """Crea encabezado personalizado para un trabajador"""
        encabezado = []
        
        encabezado.append(
            Paragraph(
                "TECNOLÓGICO NACIONAL DE MEXICO CAMPUS MINATITLÁN",
                title_style
            )
        )
        encabezado.append(
            Paragraph("REGISTRO DE CHECADAS", title_style)
        )
        encabezado.append(
            Paragraph(
                f"PERIODO DEL {fecha_inicio} AL {fecha_fin}",
                title_style
            )
        )
        encabezado.append(
            Paragraph(
                f"TRABAJADOR: {num_trabajador} - {nombre_trabajador}",
                title_style
            )
        )
        encabezado.append(
            Paragraph(
                f"Fecha de Impresión: {datetime.now().strftime('%d-%m-%Y')}",
                title_style
            )
        )
        encabezado.append(Spacer(1, 10))
        
        return encabezado
    
    def _crear_tabla(self, registros_dict: List[Dict]) -> Table:
        """Crea tabla con registros de bitácora"""
        
        # Encabezados de columnas
        headers = [
            'Codigo',
            'Depto.',
            'Nombre',
            'Fecha',
            'Turno',
            'Horario',
            'C',
            'Mov',
            'Checada1',
            'Checada2',
            'Checada3',
            'Checada4'
        ]
        
        data = [headers]
        
        # Agregar datos de cada registro
        for reg in registros_dict:
            row = [
                str(reg.get('num_trabajador', '')),
                str(reg.get('departamento', '')),
                reg.get('nombre_trabajador', ''),
                self._formatear_fecha(reg.get('fecha')),
                str(reg.get('turno_id', '')),
                self._formatear_horario(reg.get('horario_texto')),
                reg.get('codigo_incidencia', ''),
                reg.get('tipo_movimiento', ''),
                self._formatear_hora(reg.get('checada1')),
                self._formatear_hora(reg.get('checada2')),
                self._formatear_hora(reg.get('checada3')),
                self._formatear_hora(reg.get('checada4'))
            ]
            data.append(row)
        
        # Crear tabla con anchos específicos
        table = Table(
            data,
            colWidths=[40, 35, 200, 70, 35, 70, 30, 40, 50, 50, 50, 50]
        )
        
        # Aplicar estilos
        table.setStyle(TableStyle([
            # ENCABEZADOS
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # DATOS
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            
            # BORDES
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            
            # ALINEACIÓN POR COLUMNA
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),   # Codigo
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),   # Depto
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),     # Nombre (izquierda)
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),   # Fecha
            ('ALIGN', (4, 0), (4, -1), 'CENTER'),   # Turno
            ('ALIGN', (5, 0), (5, -1), 'CENTER'),   # Horario
            ('ALIGN', (6, 0), (6, -1), 'CENTER'),   # C (código)
            ('ALIGN', (7, 0), (7, -1), 'CENTER'),   # Mov
            ('ALIGN', (8, 0), (11, -1), 'CENTER'),  # Checadas (todas centradas)
        ]))
        
        return table
    
    def _formatear_fecha(self, fecha) -> str:
        """Formatea fecha como 'Vie 01-08-2024'"""
        if not fecha:
            return ''
        
        from datetime import date
        if isinstance(fecha, str):
            try:
                fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            except:
                return fecha
        
        if isinstance(fecha, date):
            dia_semana = self.dias_semana[fecha.weekday()]
            return f"{dia_semana} {fecha.strftime('%d-%m-%Y')}"
        
        return str(fecha)
    
    def _formatear_horario(self, horario_texto: str) -> str:
        """Formatea horario, manejando horarios mixtos con salto de línea"""
        if not horario_texto:
            return ''
        
        if ',' in horario_texto:
            partes = horario_texto.split(',')
            return '\n'.join(partes)
        
        return horario_texto
    
    def _formatear_hora(self, hora) -> str:
        """Formatea hora para mostrar en tabla"""
        if not hora:
            return ''
        
        if isinstance(hora, str):
            if len(hora) > 5:
                return hora[:5]
            return hora
        
        return str(hora)


# Instancia singleton
generar_pdf_masivo_bitacora_use_case = GenerarPdfMasivoBitacoraUseCase()
