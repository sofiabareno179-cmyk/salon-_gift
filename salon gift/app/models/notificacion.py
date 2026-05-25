from app import db
from datetime import datetime

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'

    idnotificacion = db.Column(db.Integer, primary_key=True)
    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.String(500), nullable=True)
    leida = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('User', back_populates='notificaciones')

    def __init__(self, idusuario, titulo, mensaje=None):
        self.idusuario = idusuario
        self.titulo = titulo
        self.mensaje = mensaje

    def save(self):
        db.session.add(self)
        db.session.commit()