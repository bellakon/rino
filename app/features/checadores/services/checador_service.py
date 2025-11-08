"""
Servicio de checadores ZKTeco
Responsabilidad: Toda la comunicación con dispositivos ZKTeco
"""
from zk import ZK
from app.config.checadores_config import CheckadoresConfig


class ChecadorService:
    """Maneja todas las operaciones con dispositivos ZKTeco"""
    
    def __init__(self, timeout=None):
        self.timeout = timeout or CheckadoresConfig.TIMEOUT
    
    def conectar(self, ip, puerto=4370):
        """
        Establece conexión con un checador
        
        Args:
            ip (str): IP del checador
            puerto (int): Puerto del checador
            
        Returns:
            tuple: (conexion, error)
        """
        try:
            zk = ZK(ip, port=puerto, timeout=self.timeout)
            conn = zk.connect()
            return conn, None
        except Exception as e:
            return None, f"Error de conexión: {str(e)}"
    
    def desconectar(self, conn):
        """
        Cierra la conexión con el checador
        
        Args:
            conn: Objeto de conexión
        """
        try:
            if conn:
                conn.disconnect()
        except Exception:
            pass
    
    def probar_conexion(self, ip, puerto=4370):
        """
        Prueba si se puede conectar al checador
        
        Args:
            ip (str): IP del checador
            puerto (int): Puerto del checador
            
        Returns:
            tuple: (exito, error)
        """
        conn, error = self.conectar(ip, puerto)
        if error:
            return False, error
        
        self.desconectar(conn)
        return True, None
    
    def obtener_info_dispositivo(self, ip, puerto=4370):
        """
        Obtiene información detallada del dispositivo
        
        Args:
            ip (str): IP del checador
            puerto (int): Puerto del checador
            
        Returns:
            tuple: (info_dict, error)
        """
        conn, error = self.conectar(ip, puerto)
        if error:
            return None, error
        
        try:
            info = {
                'serial_number': conn.get_serialnumber() if hasattr(conn, 'get_serialnumber') else None,
                'platform': conn.get_platform() if hasattr(conn, 'get_platform') else None,
                'firmware_version': conn.get_firmware_version() if hasattr(conn, 'get_firmware_version') else None,
                'device_name': conn.get_device_name() if hasattr(conn, 'get_device_name') else None,
                'mac_address': conn.get_mac() if hasattr(conn, 'get_mac') else None,
                'work_code': conn.get_workcode() if hasattr(conn, 'get_workcode') else None,
                'vendor': conn.get_vendor() if hasattr(conn, 'get_vendor') else None,
                'product_code': conn.get_product_code() if hasattr(conn, 'get_product_code') else None,
                'pin_width': conn.get_pin_width() if hasattr(conn, 'get_pin_width') else None,
                'face_version': conn.get_face_version() if hasattr(conn, 'get_face_version') else None,
                'fp_version': conn.get_fp_version() if hasattr(conn, 'get_fp_version') else None,
            }
            
            self.desconectar(conn)
            return info, None
            
        except Exception as e:
            self.desconectar(conn)
            return None, f"Error al obtener información: {str(e)}"
    
    def obtener_usuarios(self, ip, puerto=4370):
        """
        Obtiene usuarios registrados en un checador
        
        Args:
            ip (str): IP del checador
            puerto (int): Puerto del checador
            
        Returns:
            tuple: (lista_usuarios, error)
        """
        conn, error = self.conectar(ip, puerto)
        if error:
            return None, error
        
        try:
            usuarios = conn.get_users()
            
            # Convertir usuarios a diccionarios
            usuarios_lista = []
            for usuario in usuarios:
                usuarios_lista.append({
                    'user_id': usuario.user_id,  # num_trabajador
                    'name': usuario.name,
                    'privilege': usuario.privilege,
                    'password': usuario.password,
                    'group_id': usuario.group_id,
                    'uid': usuario.uid,
                    'card': getattr(usuario, 'card', None)
                })
            
            self.desconectar(conn)
            return usuarios_lista, None
            
        except Exception as e:
            self.desconectar(conn)
            return None, f"Error al obtener usuarios: {str(e)}"
    
    def obtener_asistencias(self, ip, puerto=4370):
        """
        Obtiene asistencias (attendance) del checador
        
        Args:
            ip (str): IP del checador
            puerto (int): Puerto del checador
            
        Returns:
            tuple: (lista_asistencias, error)
        """
        conn, error = self.conectar(ip, puerto)
        if error:
            return None, error
        
        try:
            # Obtener número de serie del dispositivo
            serial_number = None
            try:
                serial_number = conn.get_serialnumber()
            except:
                # Si falla, usar IP como fallback
                serial_number = ip
            
            asistencias = conn.get_attendance()
            
            # Convertir a diccionarios compatibles con modelo Asistencia
            asistencias_lista = []
            for asistencia in asistencias:
                # pyzk estructura: user_id, timestamp, status, punch
                # timestamp es datetime completo
                timestamp = asistencia.timestamp
                
                asistencias_lista.append({
                    'num_trabajador': int(asistencia.user_id),
                    'fecha': timestamp.strftime('%Y-%m-%d'),
                    'hora': timestamp.strftime('%H:%M:%S'),
                    'checador': serial_number  # Número de serie del checador
                })
            
            self.desconectar(conn)
            return asistencias_lista, None
            
        except Exception as e:
            self.desconectar(conn)
            return None, f"Error al obtener asistencias: {str(e)}"


# Instancia singleton
checador_service = ChecadorService()
