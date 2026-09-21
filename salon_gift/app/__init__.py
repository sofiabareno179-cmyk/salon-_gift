from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import inspect, text
import os

db = SQLAlchemy()
login_manager = LoginManager()

def ensure_schema_columns():
    inspector = inspect(db.engine)
    # Quita la restricción vieja que impedía un horario por día (UNIQUE idusuario)
    try:
        for c in inspector.get_unique_constraints('agenda'):
            if c['name'] == 'agenda_idusuario_key':
                db.session.execute(db.text('ALTER TABLE agenda DROP CONSTRAINT agenda_idusuario_key'))
                db.session.commit()
                print('Dropped legacy constraint agenda_idusuario_key')
                break
    except Exception as e:
        db.session.rollback()
        print(f"Agenda constraint cleanup skipped: {e}")
    existing_tables = set(inspector.get_table_names())
    for table in db.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue
        existing = {c['name'] for c in inspector.get_columns(table.name)}
        for col in table.columns:
            if col.name in existing or col.primary_key or col.unique:
                continue
            if not col.nullable and col.server_default is None and col.default is None:
                continue
            if col.foreign_keys:
                continue
            col_type = col.type.compile(db.engine.dialect)
            try:
                db.session.execute(text(f'ALTER TABLE {table.name} ADD COLUMN {col.name} {col_type}'))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Schema sync skipped column {table.name}.{col.name}: {e}")

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
        usuarios_route, servicios_route,perfil_route,
        galeria_route,catalogo_route,notificaciones_route,
        bloqueos_route,frases_route
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
    app.register_blueprint(galeria_route.bp)
    app.register_blueprint(catalogo_route.bp)
    app.register_blueprint(notificaciones_route.bp)
    app.register_blueprint(bloqueos_route.bp)
    app.register_blueprint(frases_route.bp)

    @app.errorhandler(404)
    def not_found(e):
        return {"error": "404 No Encontrado"}, 404

    @app.errorhandler(403)
    def forbidden(e):
        return {"error": "403 Acceso denegado"}, 403

    @app.template_filter('format_cop')
    def format_cop(value):
        try:
            num = float(value)
        except (TypeError, ValueError):
            return ''
        signo = '-' if num < 0 else ''
        num = abs(num)
        if num == int(num):
            return f"{signo}${int(num):,}".replace(',', '.')
        s = f"{num:,.2f}".replace(',', 'X').replace('.', ',')
        return f"{signo}${s.replace('X', '.')}"

    @app.errorhandler(Exception)
    def handle_error(e):
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            return {"error": e.description}, e.code
        import traceback
        traceback.print_exc()
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}, 500

    with app.app_context():
        try:
            ensure_schema_columns()
        except Exception as e:
            print(f"Schema sync skipped: {e}")

    return app