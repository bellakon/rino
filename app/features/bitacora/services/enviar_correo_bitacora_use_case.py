"""
Caso de uso: Enviar Correo con Bitácora
Envía correo electrónico con PDF de bitácora adjunto + plantilla de instrucciones
"""
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from typing import Optional
from pathlib import Path

from app.config.email_templates import BITACORA_EMAIL
from app.config.smtp_config import SMTP_CONFIG
from app.features.bitacora.services.generar_pdf_bitacora_use_case import generar_pdf_bitacora_use_case
from app.features.bitacora.services.listar_bitacora_use_case import ListarBitacoraUseCase
from app.features.trabajadores.services.obtener_trabajador_use_case import obtener_trabajador_use_case


class EnviarCorreoBitacoraUseCase:
    """Envía correo electrónico con PDF de bitácora y plantilla adjuntos"""
    
    def ejecutar(
        self,
        num_trabajador: int,
        nombre_trabajador: str,
        fecha_inicio: str,
        fecha_fin: str
    ) -> tuple[bool, Optional[str]]:
        """
        Envía correo con PDF de bitácora adjunto
        
        Args:
            num_trabajador: Número del trabajador
            nombre_trabajador: Nombre completo del trabajador
            fecha_inicio: Fecha inicio (YYYY-MM-DD)
            fecha_fin: Fecha fin (YYYY-MM-DD)
            
        Returns:
            tuple: (éxito, error)
        """
        try:
            # 1. Obtener datos del trabajador (incluye email)
            trabajador, error = obtener_trabajador_use_case.ejecutar(num_trabajador)
            
            if error:
                return False, error
            
            email_trabajador = trabajador.get('email')
            if not email_trabajador:
                return False, f"El trabajador {nombre_trabajador} no tiene correo electrónico registrado"
            
            # 2. Obtener registros de bitácora
            fecha_inicio_date = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin_date = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            
            listar_use_case = ListarBitacoraUseCase()
            registros = listar_use_case.ejecutar(
                num_trabajador=num_trabajador,
                fecha_inicio=fecha_inicio_date,
                fecha_fin=fecha_fin_date,
                codigo_incidencia=None
            )
            
            if not registros:
                return False, "No hay registros de bitácora para el periodo especificado"
            
            # 3. Generar PDF de bitácora
            buffer, error = generar_pdf_bitacora_use_case.ejecutar(
                registros=registros,
                nombre_trabajador=nombre_trabajador,
                num_trabajador=num_trabajador,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            
            if error:
                return False, f"Error al generar PDF: {error}"
            
            # 4. Preparar variables para la plantilla
            fecha_inicio_formatted = datetime.strptime(fecha_inicio, '%Y-%m-%d').strftime('%d/%m/%Y')
            fecha_fin_formatted = datetime.strptime(fecha_fin, '%Y-%m-%d').strftime('%d/%m/%Y')
            
            variables = {
                'nombre': nombre_trabajador,
                'num_trabajador': num_trabajador,
                'periodo_inicio': fecha_inicio_formatted,
                'periodo_fin': fecha_fin_formatted,
                'total_dias': len(registros)
            }
            
            # 4. Generar asunto y cuerpo desde plantilla
            asunto = BITACORA_EMAIL['asunto'].format(**variables)
            cuerpo = BITACORA_EMAIL['cuerpo'].format(**variables)
            
            # 5. Crear mensaje de correo con encoding UTF-8
            mensaje = MIMEMultipart()
            mensaje['From'] = f"{SMTP_CONFIG['from_name']} <{SMTP_CONFIG['from_email']}>"
            mensaje['To'] = email_trabajador
            mensaje['Subject'] = asunto
            mensaje.set_charset('utf-8')  # Importante para caracteres especiales
            
            # Adjuntar cuerpo del mensaje con encoding UTF-8
            mensaje.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
            
            # 6. Adjuntar PDF de bitácora
            buffer.seek(0)
            pdf_bitacora = MIMEApplication(buffer.read(), _subtype='pdf')
            nombre_archivo_bitacora = f"Bitacora_{num_trabajador}_{fecha_inicio}_{fecha_fin}.pdf"
            pdf_bitacora.add_header('Content-Disposition', 'attachment', filename=nombre_archivo_bitacora)
            mensaje.attach(pdf_bitacora)
            
            # 7. Adjuntar plantilla.pdf si existe
            plantilla_path = Path(__file__).parent.parent.parent.parent.parent / 'plantilla.pdf'
            if plantilla_path.exists():
                with open(plantilla_path, 'rb') as f:
                    pdf_plantilla = MIMEApplication(f.read(), _subtype='pdf')
                    pdf_plantilla.add_header('Content-Disposition', 'attachment', filename='Instrucciones_Bitacora.pdf')
                    mensaje.attach(pdf_plantilla)
            
            # 8. Enviar correo
            with smtplib.SMTP(SMTP_CONFIG['host'], SMTP_CONFIG['port']) as servidor:
                if SMTP_CONFIG['use_tls']:
                    servidor.starttls()
                
                servidor.login(SMTP_CONFIG['username'], SMTP_CONFIG['password'])
                servidor.send_message(mensaje)
            
            return True, None
            
        except smtplib.SMTPAuthenticationError:
            return False, "Error de autenticación SMTP. Verifica usuario y contraseña en smtp_config.py"
        except smtplib.SMTPException as e:
            return False, f"Error al enviar correo: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"


# Instancia singleton
enviar_correo_bitacora_use_case = EnviarCorreoBitacoraUseCase()
