from app import db
from datetime import datetime

class CatalogoPrecio(db.Model):
    __tablename__ = 'catalogo_precios'

    idcatalogo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(500), nullable=True)
    precio = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, nombre, precio, categoria, descripcion=None):
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.descripcion = descripcion

    def save(self):
        db.session.add(self)
        db.session.commit()