"""
Caso de uso: Enviar Correo con Bitácora
Envía correo electrónico con PDF de bitácora adjunto + plantilla de instrucciones
Soporta HTML enriquecido con imágenes embebidas
"""
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from datetime import datetime
from typing import Optional
from pathlib import Path

from app.config.email_templates import (
    BITACORA_EMAIL, 
    REPORTE_ASISTENCIA_EMAIL,
    formatear_plantilla,
    obtener_ruta_imagen,
    obtener_ruta_adjunto,
    cargar_configuracion
)
from app.config.smtp_config import SMTP_CONFIG
from app.features.bitacora.services.generar_pdf_bitacora_use_case import generar_pdf_bitacora_use_case
from app.features.bitacora.services.listar_bitacora_use_case import ListarBitacoraUseCase
from app.features.trabajadores.services.obtener_trabajador_use_case import obtener_trabajador_use_case


class EnviarCorreoBitacoraUseCase:
    """Envía correo electrónico con PDF de bitácora y plantilla adjuntos"""
    
    def _adjuntar_imagen_embebida(self, mensaje_relacionado: MIMEMultipart, 
                                   clave_imagen: str) -> bool:
        """
        Adjunta una imagen embebida al mensaje para uso en HTML
        
        Args:
            mensaje_relacionado: El contenedor MIMEMultipart related
            clave_imagen: Clave de la imagen en configuración
            
        Returns:
            True si se adjuntó correctamente
        """
        try:
            # Cargar configuración actual
            config = cargar_configuracion()
            nombre_archivo = config.get(clave_imagen)
            if not nombre_archivo:
                print(f"No hay imagen configurada para: {clave_imagen}")
                return False
                
            ruta_imagen = obtener_ruta_imagen(nombre_archivo)
            if not ruta_imagen.exists():
                print(f"Imagen no encontrada: {ruta_imagen}")
                return False
            
            # Detectar tipo MIME
            mime_type, _ = mimetypes.guess_type(str(ruta_imagen))
            if not mime_type or not mime_type.startswith('image/'):
                mime_type = 'image/png'
            
            subtype = mime_type.split('/')[1]
            
            with open(ruta_imagen, 'rb') as f:
                imagen = MIMEImage(f.read(), _subtype=subtype)
                imagen.add_header('Content-ID', f'<{clave_imagen}>')
                imagen.add_header('Content-Disposition', 'inline', 
                                 filename=nombre_archivo)
                mensaje_relacionado.attach(imagen)
            
            return True
        except Exception as e:
            print(f"Error adjuntando imagen {clave_imagen}: {e}")
            return False
    
    def _crear_mensaje_html(self, plantilla_formateada: dict, 
                            email_destino: str, asunto: str) -> MIMEMultipart:
        """
        Crea un mensaje con HTML enriquecido e imágenes embebidas
        
        Args:
            plantilla_formateada: Resultado de formatear_plantilla()
            email_destino: Email del destinatario
            asunto: Asunto del correo
            
        Returns:
            MIMEMultipart listo para adjuntar archivos
        """
        # Estructura del mensaje para HTML con imágenes:
        # multipart/mixed
        #   multipart/related
        #     multipart/alternative
        #       text/plain
        #       text/html
        #     image/png (embebida 1)
        #     image/png (embebida 2)
        #   application/pdf (adjunto)
        
        mensaje = MIMEMultipart('mixed')
        mensaje['From'] = f"{SMTP_CONFIG['from_name']} <{SMTP_CONFIG['from_email']}>"
        mensaje['To'] = email_destino
        mensaje['Subject'] = asunto
        
        # Contenedor related para HTML + imágenes
        mensaje_related = MIMEMultipart('related')
        
        # Contenedor alternative para texto plano + HTML
        mensaje_alt = MIMEMultipart('alternative')
        
        # Agregar versión texto plano
        if plantilla_formateada.get('cuerpo_texto'):
            texto_plano = MIMEText(plantilla_formateada['cuerpo_texto'], 'plain', 'utf-8')
            mensaje_alt.attach(texto_plano)
        
        # Agregar versión HTML
        if plantilla_formateada.get('cuerpo_html'):
            texto_html = MIMEText(plantilla_formateada['cuerpo_html'], 'html', 'utf-8')
            mensaje_alt.attach(texto_html)
        
        mensaje_related.attach(mensaje_alt)
        
        # Adjuntar imágenes embebidas
        for clave_imagen in plantilla_formateada.get('imagenes_embebidas', []):
            self._adjuntar_imagen_embebida(mensaje_related, clave_imagen)
        
        mensaje.attach(mensaje_related)
        
        return mensaje
    
    def _crear_mensaje_simple(self, cuerpo: str, email_destino: str, 
                               asunto: str) -> MIMEMultipart:
        """
        Crea un mensaje de texto plano simple
        """
        mensaje = MIMEMultipart()
        mensaje['From'] = f"{SMTP_CONFIG['from_name']} <{SMTP_CONFIG['from_email']}>"
        mensaje['To'] = email_destino
        mensaje['Subject'] = asunto
        mensaje.set_charset('utf-8')
        mensaje.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
        return mensaje
    
    def ejecutar(
        self,
        num_trabajador: int,
        nombre_trabajador: str,
        fecha_inicio: str,
        fecha_fin: str,
        usar_plantilla_html: bool = None  # None = usar configuración guardada
    ) -> tuple[bool, Optional[str]]:
        """
        Envía correo con PDF de bitácora adjunto
        
        Args:
            num_trabajador: Número del trabajador
            nombre_trabajador: Nombre completo del trabajador
            fecha_inicio: Fecha inicio (YYYY-MM-DD)
            fecha_fin: Fecha fin (YYYY-MM-DD)
            usar_plantilla_html: Si True usa HTML, si False texto plano, si None usa config guardada
            
        Returns:
            tuple: (éxito, error)
        """
        try:
            # Cargar configuración
            config = cargar_configuracion()
            print(f"[CORREO] Config cargada: usar_plantilla_html={config.get('usar_plantilla_html')}")
            print(f"[CORREO] Config imágenes: encabezado={config.get('imagen_encabezado')}, secundaria={config.get('imagen_secundaria')}")
            
            # Determinar si usar HTML (prioridad: parámetro > configuración)
            if usar_plantilla_html is None:
                usar_plantilla_html = config.get('usar_plantilla_html', True)
            
            print(f"[CORREO] usar_plantilla_html final: {usar_plantilla_html}")
            
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
            
            # Calcular descripción de quincena
            fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            mes_nombre = fecha_inicio_obj.strftime('%B').capitalize()
            quincena = 1 if fecha_inicio_obj.day <= 15 else 2
            descripcion_quincena = f"{'Primera' if quincena == 1 else 'Segunda'} quincena de {mes_nombre}"
            
            # Fecha límite de justificaciones (7 días después del fin del periodo)
            fecha_limite = datetime.strptime(fecha_fin, '%Y-%m-%d')
            from datetime import timedelta
            fecha_limite = fecha_limite + timedelta(days=7)
            fecha_limite_str = fecha_limite.strftime('%d de %B del presente año')
            
            variables = {
                'nombre': nombre_trabajador,
                'num_trabajador': num_trabajador,
                'periodo_inicio': fecha_inicio_formatted,
                'periodo_fin': fecha_fin_formatted,
                'total_dias': len(registros),
                'descripcion_quincena': descripcion_quincena,
                'quincena': quincena,
                'mes': mes_nombre,
                'anio': fecha_inicio_obj.year,
                'fecha_limite_justificaciones': fecha_limite_str,
                'departamento': trabajador.get('departamento', 'Sin departamento')
            }
            
            # 5. Seleccionar plantilla y crear mensaje
            print(f"[CORREO] Creando mensaje. usar_plantilla_html={usar_plantilla_html}")
            if usar_plantilla_html:
                print("[CORREO] Usando plantilla HTML enriquecida (REPORTE_ASISTENCIA_EMAIL)")
                plantilla = REPORTE_ASISTENCIA_EMAIL
                plantilla_formateada = formatear_plantilla(plantilla, variables)
                mensaje = self._crear_mensaje_html(
                    plantilla_formateada, 
                    email_trabajador, 
                    plantilla_formateada['asunto']
                )
            else:
                print("[CORREO] Usando plantilla texto plano (BITACORA_EMAIL)")
                plantilla_formateada = formatear_plantilla(BITACORA_EMAIL, variables)
                mensaje = self._crear_mensaje_simple(
                    plantilla_formateada['cuerpo_texto'],
                    email_trabajador,
                    plantilla_formateada['asunto']
                )
            
            # 6. Adjuntar PDF de bitácora
            buffer.seek(0)
            pdf_bitacora = MIMEApplication(buffer.read(), _subtype='pdf')
            nombre_archivo_bitacora = f"Bitacora_{num_trabajador}_{fecha_inicio}_{fecha_fin}.pdf"
            pdf_bitacora.add_header('Content-Disposition', 'attachment', filename=nombre_archivo_bitacora)
            mensaje.attach(pdf_bitacora)
            
            # 7. Adjuntar archivos configurados en la plantilla
            for nombre_adjunto in plantilla_formateada.get('adjuntos', []):
                ruta_adjunto = obtener_ruta_adjunto(nombre_adjunto)
                if ruta_adjunto.exists():
                    with open(ruta_adjunto, 'rb') as f:
                        adjunto = MIMEApplication(f.read(), _subtype='pdf')
                        # Usar nombre amigable para el usuario
                        nombre_display = 'Instrucciones_Bitacora.pdf' if 'plantilla' in nombre_adjunto.lower() else nombre_adjunto
                        adjunto.add_header('Content-Disposition', 'attachment', filename=nombre_display)
                        mensaje.attach(adjunto)
            
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
