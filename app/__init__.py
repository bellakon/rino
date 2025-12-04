"""
Inicialización de la aplicación Flask con arquitectura por features
"""
from flask import Flask, render_template, redirect, url_for, session
from app.config.app_config import Config
from app.config.users_config import SESSION_LIFETIME_SECONDS
from datetime import timedelta
import os


def create_app():
    """Factory para crear la aplicación Flask"""
    
    # Crear app con template folder en shared
    app = Flask(__name__, template_folder='shared/templates')
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY
    
    # Configurar duración de sesión
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=SESSION_LIFETIME_SECONDS)
    
    # Registrar filtros de Jinja personalizados
    @app.template_filter('number_format')
    def number_format_filter(value):
        """Formatea números con separadores de miles"""
        try:
            return "{:,}".format(int(value)).replace(",", ",")
        except (ValueError, TypeError):
            return value
    
    # Registrar template folders adicionales por feature (rutas absolutas)
    import jinja2
    base_dir = os.path.abspath(os.path.dirname(__file__))
    loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader([
            os.path.join(base_dir, 'features/auth/templates'),
            os.path.join(base_dir, 'features/checadores/templates'),
            os.path.join(base_dir, 'features/asistencias/templates'),
            os.path.join(base_dir, 'features/trabajadores/templates'),
            os.path.join(base_dir, 'features/migrar_datos/templates'),
            os.path.join(base_dir, 'features/departamentos/templates'),
            os.path.join(base_dir, 'features/horarios/templates'),
            os.path.join(base_dir, 'features/movimientos/templates'),
            os.path.join(base_dir, 'features/bitacora/templates'),
            os.path.join(base_dir, 'features/configuracion/templates'),
        ])
    ])
    app.jinja_loader = loader
    
    # Registrar blueprint de autenticación primero
    from app.features.auth.routes import auth_bp, login_required
    app.register_blueprint(auth_bp)
    
    # Registrar blueprints de features
    from app.features.checadores.routes.checador_routes import checadores_bp
    from app.features.asistencias.routes.asistencia_routes import asistencias_bp
    from app.features.trabajadores.routes.trabajador_routes import trabajadores_bp
    from app.features.migrar_datos.routes.migrar_datos_routes import migrar_datos_bp
    from app.features.departamentos.routes.departamentos_routes import departamentos_bp
    from app.features.horarios.routes.horarios_routes import horarios_bp
    from app.features.movimientos.routes.movimientos_routes import movimientos_bp
    from app.features.bitacora.routes.bitacora_routes import bitacora_bp
    from app.features.configuracion.routes.configuracion_routes import configuracion_bp
    
    app.register_blueprint(checadores_bp)
    app.register_blueprint(asistencias_bp)
    app.register_blueprint(trabajadores_bp)
    app.register_blueprint(migrar_datos_bp)
    app.register_blueprint(departamentos_bp)
    app.register_blueprint(horarios_bp)
    app.register_blueprint(movimientos_bp)
    app.register_blueprint(bitacora_bp)
    app.register_blueprint(configuracion_bp)
    
    # Proteger TODAS las rutas excepto auth
    @app.before_request
    def require_login():
        from flask import request
        # Rutas que no requieren autenticación
        allowed_routes = ['auth.login', 'auth.logout', 'static']
        
        if request.endpoint and not any(request.endpoint.startswith(r) for r in allowed_routes):
            if not session.get('logged_in'):
                return redirect(url_for('auth.login', next=request.url))
    
    # Ruta principal
    @app.route('/')
    def home():
        return render_template('index.html')
    
    # Agregar contexto global para templates
    @app.context_processor
    def inject_user():
        return {
            'current_user': session.get('username'),
            'is_logged_in': session.get('logged_in', False)
        }
    
    return app
