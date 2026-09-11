from app import db
from datetime import datetime

class Bloqueo(db.Model):
    __tablename__ = 'bloqueos'

    idbloqueo = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.String(5), nullable=False)
    hora_fin = db.Column(db.String(5), nullable=False)
    motivo = db.Column(db.String(255), nullable=True)
    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.relationship('User', back_populates='bloqueos')

    def __init__(self, fecha, hora_inicio, hora_fin, idusuario, motivo=None):
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.idusuario = idusuario
        self.motivo = motivo

    def save(self):
        db.session.add(self)
        db.session.commit()