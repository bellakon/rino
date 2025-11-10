"""
Inicialización de la aplicación Flask con arquitectura por features
"""
from flask import Flask, render_template
from app.config.app_config import Config
import os


def create_app():
    """Factory para crear la aplicación Flask"""
    
    # Crear app con template folder en shared
    app = Flask(__name__, template_folder='shared/templates')
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY
    
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
            os.path.join(base_dir, 'features/checadores/templates'),
            os.path.join(base_dir, 'features/asistencias/templates'),
            os.path.join(base_dir, 'features/trabajadores/templates'),
            os.path.join(base_dir, 'features/migrar_datos/templates'),
            os.path.join(base_dir, 'features/departamentos/templates'),
            os.path.join(base_dir, 'features/horarios/templates'),
        ])
    ])
    app.jinja_loader = loader
    
    # Registrar blueprints de features
    from app.features.checadores.routes.checador_routes import checadores_bp
    from app.features.asistencias.routes.asistencia_routes import asistencias_bp
    from app.features.trabajadores.routes.trabajador_routes import trabajadores_bp
    from app.features.migrar_datos.routes.migrar_datos_routes import migrar_datos_bp
    from app.features.departamentos.routes.departamentos_routes import departamentos_bp
    from app.features.horarios.routes.horarios_routes import horarios_bp
    
    app.register_blueprint(checadores_bp)
    app.register_blueprint(asistencias_bp)
    app.register_blueprint(trabajadores_bp)
    app.register_blueprint(migrar_datos_bp)
    app.register_blueprint(departamentos_bp)
    app.register_blueprint(horarios_bp)
    
    # Ruta principal
    @app.route('/')
    def home():
        return render_template('index.html')
    
    return app
