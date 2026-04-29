from flask_login import UserMixin
from app import db

class Recordatorios(db.Model, UserMixin): 
    __tablename__ = 'recordatorios'
    
    idrecordatorios = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    mensaje = db.Column(db.String(500), nullable=True)
    fecha_recordatorio = db.Column(db.String(100), nullable=False) 
    def __init__(self, titulo, mensaje, fecha_recordatorio, prioridad):
        self.titulo = titulo
        self.mensaje = mensaje
        self.fecha_recordatorio = fecha_recordatorio
        self.prioridad = prioridad

    def get_id(self):
        return str(self.idrecordatorios)

    def save(self):
        db.session.add(self)
        db.session.commit()