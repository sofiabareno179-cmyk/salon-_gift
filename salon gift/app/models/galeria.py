from app import db
from datetime import datetime

class Galeria(db.Model):
    __tablename__ = 'galeria'

    idgaleria = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    archivo = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(10), nullable=False, default='imagen')
    descripcion = db.Column(db.String(500), nullable=True)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, titulo, archivo, tipo='imagen', descripcion=None):
        self.titulo = titulo
        self.archivo = archivo
        self.tipo = tipo
        self.descripcion = descripcion

    def save(self):
        db.session.add(self)
        db.session.commit()