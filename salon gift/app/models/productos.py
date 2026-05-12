from flask_login import UserMixin
from app import db
# Tabla intermedia para Productos y Proveedores
producto_proveedores = db.Table('producto_proveedores',
    db.Column('producto_id', db.Integer, db.ForeignKey('productos.idproductos'), primary_key=True),
    db.Column('proveedor_id', db.Integer, db.ForeignKey('proveedores.idproveedores'), primary_key=True)
)

class Productos(db.Model, UserMixin): 
    __tablename__ = 'productos'
    
    idproductos = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(500), nullable=True)
    precio = db.Column(db.Float, nullable=False) 
    categoria = db.Column(db.String(100), nullable=False)


    proveedores = db.relationship('Proveedores', secondary=producto_proveedores, backref='productos')
    inventario = db.relationship('Inventario', back_populates='producto', uselist=False)

    def __init__(self, nombre, descripcion, precio, categoria):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria

    def get_id(self):
        return str(self.idproductos)

    def save(self):
        db.session.add(self)
        db.session.commit()