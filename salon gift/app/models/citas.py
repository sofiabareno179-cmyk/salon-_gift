from datetime import datetime
from flask_login import UserMixin
from app import db

class Citas(db.Model, UserMixin): 
    __tablename__ = 'citas'
    
    idcitas = db.Column(db.Integer, primary_key=True)
    fechahora = db.Column(db.DateTime, nullable=False)
    servicio = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(100), nullable=False, default='Pendiente')

    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False)
    user = db.relationship('User', foreign_keys=[idusuario], lazy=True)
    # Relación 1:1 con Servicio
    servicios = db.relationship('Servicio', back_populates='citas', uselist=False)

    def __init__(self, fechahora, servicio=None, estado='Pendiente', idusuario=None):
        self.fechahora = fechahora
        self.servicio = servicio
        self.estado = estado
        self.idusuario = idusuario

    def get_id(self):
        return str(self.idcitas)

    @property
    def fecha_dt(self):
        if isinstance(self.fechahora, str):
            try:
                return datetime.fromisoformat(self.fechahora)
            except Exception:
                return datetime.strptime(self.fechahora, '%Y-%m-%d %H:%M:%S')
        return self.fechahora

    def save(self):
        db.session.add(self)
        db.session.commit()