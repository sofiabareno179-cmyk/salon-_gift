from flask_login import UserMixin
from app import db

class Proveedores(db.Model, UserMixin): 
    __tablename__ = 'proveedores'
    
    idproveedores = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(150), nullable=False)
    contacto_nombre = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    direccion = db.Column(db.String(250), nullable=True)

    def __init__(self, nombre_empresa, contacto_nombre, telefono, email=None, direccion=None):
        self.nombre_empresa = nombre_empresa
        self.contacto_nombre = contacto_nombre
        self.telefono = telefono
        self.email = email
        self.direccion = direccion

    def get_id(self):
        # Retorna el ID único de la tabla proveedores
        return str(self.idproveedores)

    def save(self):
        db.session.add(self)
        db.session.commit()