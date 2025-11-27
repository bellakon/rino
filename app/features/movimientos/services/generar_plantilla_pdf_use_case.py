"""
Caso de uso: Generar PDF con Códigos de Movimientos
Genera un PDF de referencia con todos los códigos de falta y resumen del sistema
"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime
from app.core.database.query_executor import query_executor


class GenerarPlantillaPdfUseCase:
    """Genera PDF de plantilla con códigos y resumen del sistema"""
    
    def ejecutar(self) -> tuple[BytesIO | None, str | None]:
        """
        Genera PDF con códigos de movimientos y resumen
        
        Returns:
            tuple: (buffer con PDF, error)
        """
        try:
            # Obtener tipos de movimientos
            query = """
                SELECT nomenclatura, nombre, descripcion, categoria, letra
                FROM tipos_movimientos
                WHERE activo = 1
                ORDER BY categoria, nomenclatura
            """
            movimientos, error = query_executor.ejecutar(query)
            
            if error:
                return None, f"Error al consultar movimientos: {error}"
            
            # Crear buffer en memoria
            buffer = BytesIO()
            
            # Crear documento
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                leftMargin=0.75*inch,
                rightMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            elements = []
            styles = getSampleStyleSheet()
            
            # Estilos personalizados
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                alignment=TA_CENTER,
                spaceAfter=12,
                textColor=colors.HexColor('#1a5490')
            )
            
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=14,
                alignment=TA_CENTER,
                spaceAfter=20,
                textColor=colors.HexColor('#2c3e50')
            )
            
            section_style = ParagraphStyle(
                'SectionHeader',
                parent=styles['Heading2'],
                fontSize=12,
                spaceAfter=10,
                spaceBefore=15,
                textColor=colors.HexColor('#34495e')
            )
            
            body_style = ParagraphStyle(
                'BodyText',
                parent=styles['Normal'],
                fontSize=10,
                alignment=TA_LEFT,
                spaceAfter=8
            )
            
            # Encabezado principal
            elements.append(Paragraph("TecnoTime", title_style))
            elements.append(Paragraph("Sistema de Gestión de Asistencias", subtitle_style))
            elements.append(Spacer(1, 20))
            
            # Información general
            elements.append(Paragraph("Resumen del Sistema", section_style))
            
            info_general = [
                f"<b>Fecha de generación:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                f"<b>Total de códigos registrados:</b> {len(movimientos)}",
                "",
                "<b>Descripción:</b>",
                "Este documento contiene el catálogo completo de códigos de movimientos " +
                "utilizados en el sistema TecnoTime para el registro y control de asistencias, " +
                "incidencias y movimientos del personal.",
                "",
                "<b>Categorías disponibles:</b>",
                "• <b>Falta:</b> Ausencias no justificadas",
                "• <b>Permiso:</b> Ausencias autorizadas",
                "• <b>Incapacidad:</b> Ausencias por motivos médicos",
                "• <b>Retardo:</b> Llegadas tardías",
                "• <b>Otros:</b> Movimientos especiales"
            ]
            
            for texto in info_general:
                if texto:
                    elements.append(Paragraph(texto, body_style))
            
            elements.append(Spacer(1, 20))
            
            # Agrupar movimientos por categoría
            movimientos_por_categoria = {}
            for mov in movimientos:
                cat = mov.get('categoria', 'Sin categoría')
                if cat not in movimientos_por_categoria:
                    movimientos_por_categoria[cat] = []
                movimientos_por_categoria[cat].append(mov)
            
            # Crear tabla por cada categoría
            for categoria, items in sorted(movimientos_por_categoria.items()):
                elements.append(PageBreak())
                elements.append(Paragraph(f"Códigos de {categoria}", section_style))
                elements.append(Spacer(1, 10))
                
                # Encabezados de tabla
                data = [
                    ['Código', 'Nombre', 'Descripción', 'Letra']
                ]
                
                # Agregar movimientos
                for mov in items:
                    data.append([
                        mov.get('nomenclatura', ''),
                        mov.get('nombre', ''),
                        mov.get('descripcion', '')[:50] + '...' if len(mov.get('descripcion', '')) > 50 else mov.get('descripcion', ''),
                        mov.get('letra', '')
                    ])
                
                # Crear tabla
                tabla = Table(data, colWidths=[1*inch, 1.8*inch, 2.8*inch, 0.6*inch])
                tabla.setStyle(TableStyle([
                    # Encabezado
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    
                    # Contenido
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Código centrado
                    ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Letra centrada
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('TOPPADDING', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                    
                    # Bordes
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2980b9')),
                    
                    # Alternado de filas
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')])
                ]))
                
                elements.append(tabla)
                elements.append(Spacer(1, 10))
            
            # Página final - Instrucciones
            elements.append(PageBreak())
            elements.append(Paragraph("Instrucciones de Uso", section_style))
            elements.append(Spacer(1, 10))
            
            instrucciones = [
                "<b>1. Interpretación de Códigos:</b>",
                "Cada código de movimiento está compuesto por una nomenclatura única que identifica " +
                "el tipo de incidencia o movimiento del trabajador.",
                "",
                "<b>2. Letra de Representación:</b>",
                "La columna 'Letra' indica el símbolo que aparecerá en los reportes de bitácora para " +
                "identificar visualmente el tipo de movimiento.",
                "",
                "<b>3. Categorías:</b>",
                "• <b>Falta:</b> Ausencias sin justificación que afectan la asistencia",
                "• <b>Permiso:</b> Ausencias autorizadas previamente por el área correspondiente",
                "• <b>Incapacidad:</b> Ausencias justificadas por motivos de salud",
                "• <b>Retardo:</b> Llegadas después del horario establecido",
                "• <b>Otros:</b> Movimientos especiales (comisiones, suspensiones, etc.)",
                "",
                "<b>4. Aplicación en el Sistema:</b>",
                "Los códigos se utilizan en el módulo de Movimientos para registrar incidencias " +
                "que complementan o modifican los registros de checadas automáticas.",
                "",
                "<b>5. Reportes:</b>",
                "En la bitácora de asistencias, estos códigos aparecen en la columna de movimientos " +
                "indicando las incidencias registradas para cada día.",
                "",
                "<b>Contacto:</b>",
                "Para dudas sobre el uso del sistema o solicitud de nuevos códigos de movimiento, " +
                "contacte al administrador del sistema TecnoTime."
            ]
            
            for texto in instrucciones:
                if texto:
                    elements.append(Paragraph(texto, body_style))
            
            # Footer
            elements.append(Spacer(1, 30))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                alignment=TA_CENTER,
                textColor=colors.grey
            )
            elements.append(Paragraph(
                f"TecnoTime - Sistema de Gestión de Asistencias | " +
                f"Generado: {datetime.now().strftime('%d/%m/%Y')}",
                footer_style
            ))
            
            # Construir PDF
            doc.build(elements)
            
            # Volver al inicio del buffer
            buffer.seek(0)
            
            return buffer, None
            
        except Exception as e:
            return None, f"Error al generar plantilla PDF: {str(e)}"


# Singleton
generar_plantilla_pdf_use_case = GenerarPlantillaPdfUseCase()
