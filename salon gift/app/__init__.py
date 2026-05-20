from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import text
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)    
    app.config.from_object('config.Config')
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    def ensure_citas_servicio_column():
        with app.app_context():
            try:
                with db.engine.begin() as conn:
                    # Check if table exists (PostgreSQL compatible)
                    result = conn.execute(text(
                        "SELECT 1 FROM information_schema.tables WHERE table_name='citas'"
                    ))
                    if result.first() is None:
                        return
                    # Check if column exists
                    result = conn.execute(text(
                        "SELECT 1 FROM information_schema.columns WHERE table_name='citas' AND column_name='servicio'"
                    ))
                    if result.first() is None:
                        conn.execute(text("ALTER TABLE citas ADD COLUMN servicio VARCHAR(100)"))
            except Exception as e:
                print(f"Warning: Could not ensure citas.servicio column: {e}")

    ensure_citas_servicio_column()
 
    @login_manager.user_loader
    def load_user(idusuario):
        from .models.usuario import User
        return User.query.get(int(idusuario))

    # Register blueprints
    from app.routes import (
        auth,agenda_route,citas_route,inventario_route,
        producto_route,proveedores_route,recordatorios_route,
        usuarios_route, servicios_route,perfil_route
    
    )
    app.register_blueprint(auth.bp)
    app.register_blueprint(agenda_route.bp)
    app.register_blueprint(citas_route.bp)
    app.register_blueprint(inventario_route.bp)
    app.register_blueprint(producto_route.bp)
    app.register_blueprint(proveedores_route.bp)
    app.register_blueprint(recordatorios_route.bp)
    app.register_blueprint(usuarios_route.bp)
    app.register_blueprint(servicios_route.bp)
    app.register_blueprint(perfil_route.bp)

    @app.errorhandler(Exception)
    
    def handle_error(e):
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}, 500

    return app