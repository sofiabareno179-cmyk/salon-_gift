from app import db
from datetime import datetime

class Galeria(db.Model):
    __tablename__ = 'galeria'

    idgaleria = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    imagen = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(500), nullable=True)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, titulo, imagen, descripcion=None):
        self.titulo = titulo
        self.imagen = imagen
        self.descripcion = descripcion

    def save(self):
        db.session.add(self)
        db.session.commit()