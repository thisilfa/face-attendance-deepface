from app.routes.health import health_bp
from app.routes.recognizer import recognizer_bp
from app.routes.register import register_bp
from app.routes.name_updater import name_updater_bp
from app.routes.noind_updater import noind_updater_bp
from app.routes.deleter import deleter_bp

def register_routes(app):
    """
    Register all the routes (blueprints) with the Flask app instance.
    """
    app.register_blueprint(health_bp, url_prefix='/health')
    app.register_blueprint(recognizer_bp, url_prefix='/predict')
    app.register_blueprint(register_bp, url_prefix='/register')
    app.register_blueprint(name_updater_bp, url_prefix='/update-name')
    app.register_blueprint(noind_updater_bp, url_prefix='/update-noind')
    app.register_blueprint(deleter_bp, url_prefix='/delete')
