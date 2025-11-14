"""
Caso de uso: Generar PDF de Bitácora
Genera un PDF con el formato estándar de checadas
"""
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
from typing import List, Optional
from app.features.bitacora.models.bitacora_models import BitacoraRecord


class GenerarPdfBitacoraUseCase:
    """Genera PDF de bitácora en formato estándar"""
    
    def __init__(self):
        self.dias_semana = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        self.registros_por_pagina = 15
    
    def ejecutar(
        self,
        registros: List[BitacoraRecord],
        nombre_trabajador: str,
        num_trabajador: int,
        fecha_inicio: str,
        fecha_fin: str
    ) -> tuple[Optional[BytesIO], Optional[str]]:
        """
        Genera PDF de bitácora
        
        Args:
            registros: Lista de registros de bitácora
            nombre_trabajador: Nombre completo del trabajador
            num_trabajador: Número del trabajador
            fecha_inicio: Fecha inicio del periodo
            fecha_fin: Fecha fin del periodo
            
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
            
            # Procesar registros por páginas
            pagina_actual = 1
            total_registros = len(registros)
            
            for i in range(0, total_registros, self.registros_por_pagina):
                # Agregar encabezado de página
                elements.extend(self._crear_encabezado(
                    nombre_trabajador,
                    num_trabajador,
                    fecha_inicio,
                    fecha_fin,
                    title_style
                ))
                
                # Obtener lote de registros
                lote_registros = registros[i:i + self.registros_por_pagina]
                
                # Crear tabla para este lote
                tabla = self._crear_tabla(lote_registros)
                elements.append(tabla)
                
                # Agregar información de página
                elements.append(Spacer(1, 10))
                elements.append(
                    Paragraph(f"HOJA #{pagina_actual}", page_info_style)
                )
                
                # Agregar salto de página si no es la última
                if i + self.registros_por_pagina < total_registros:
                    elements.append(PageBreak())
                    pagina_actual += 1
            
            # Construir PDF
            doc.build(elements)
            
            # Volver al inicio del buffer
            buffer.seek(0)
            
            return buffer, None
            
        except Exception as e:
            return None, f"Error al generar PDF: {str(e)}"
    
    def _crear_encabezado(
        self,
        nombre_trabajador: str,
        num_trabajador: int,
        fecha_inicio: str,
        fecha_fin: str,
        title_style
    ) -> list:
        """Crea encabezado de página"""
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
                f"Empleado: {num_trabajador} - {nombre_trabajador}",
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
    
    def _crear_tabla(self, registros: List[BitacoraRecord]) -> Table:
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
        
        # Agregar datos de cada registro (filtrar DESCANSO)
        for reg in registros:
            # Saltar días sin horario o con horario de descanso
            if not reg.horario_texto or reg.horario_texto.upper() == 'DESCANSO':
                continue
            
            row = [
                str(reg.num_trabajador),
                str(reg.departamento or ''),  # Ahora es el ID del departamento
                reg.nombre_trabajador or '',
                self._formatear_fecha(reg.fecha),
                str(reg.turno_id or ''),
                self._formatear_horario(reg.horario_texto),
                reg.codigo_incidencia or '',
                reg.tipo_movimiento or '',
                self._formatear_hora(reg.checada1),
                self._formatear_hora(reg.checada2),
                self._formatear_hora(reg.checada3),
                self._formatear_hora(reg.checada4)
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
            # Parsear string a date si es necesario
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
        
        # Si tiene coma, es horario mixto: "08:00-12:00,14:00-18:00"
        # Lo convertimos a dos líneas: "08:00-12:00\n14:00-18:00"
        if ',' in horario_texto:
            partes = horario_texto.split(',')
            return '\n'.join(partes)
        
        return horario_texto
    
    def _formatear_hora(self, hora) -> str:
        """Formatea hora para mostrar en tabla"""
        if not hora:
            return ''
        
        from datetime import time, timedelta
        
        # Si es string, retornar directamente (formato HH:MM:SS)
        if isinstance(hora, str):
            # Tomar solo HH:MM si tiene segundos
            if len(hora) > 5:
                return hora[:5]
            return hora
        
        # Si es time
        if isinstance(hora, time):
            return hora.strftime('%H:%M')
        
        # Si es timedelta (MySQL TIME)
        if isinstance(hora, timedelta):
            total_seconds = int(hora.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours:02d}:{minutes:02d}"
        
        return str(hora)


# Instancia singleton
generar_pdf_bitacora_use_case = GenerarPdfBitacoraUseCase()
