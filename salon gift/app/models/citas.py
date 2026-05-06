from flask_login import UserMixin
from app import db

class Citas(db.Model, UserMixin): 
    __tablename__ = 'citas'
    
    idcitas = db.Column(db.Integer, primary_key=True)
    fechahora = db.Column(db.String(100), nullable=False) 
    estado = db.Column(db.String(100), nullable=False)  
    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False)
    idservicio= db.Column(db.Integer, db.ForeignKey('servicios.idservicio'), nullable=False)
    id
    def __init__(self, fechahora, estado):
        self.fechahora = fechahora
        self.estado = estado
    def get_id(self):
        return str(self.idcitas)

    def save(self):
        db.session.add(self)
        db.session.commit()