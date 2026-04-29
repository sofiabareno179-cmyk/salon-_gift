from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)    
    app.config.from_object('config.Config')
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
 
    @login_manager.user_loader
    def load_user(idusuario):
        from .models.usuario import User
        return User.query.get(int(idusuario))

    # Register blueprints
    from app.routes import (
        auth,agenda_route,citas_route,inventario_route,
        producto_route,proveedores_route,recordatorios_route,
        usuarios_route, servicios_route
    
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


    @app.errorhandler(Exception)
    def handle_error(e):
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}, 500

    return app