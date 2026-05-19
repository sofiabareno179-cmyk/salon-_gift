from flask_login import UserMixin
from app import db

class Agenda(db.Model): 
    __tablename__ = 'agenda'
    idagenda = db.Column(db.Integer, primary_key=True)
    diasemana = db.Column(db.String(100), nullable=False) 
    horainicio = db.Column(db.String(100), nullable=False) 
    horafin = db.Column(db.String(250), nullable=False)

    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False)
    usuario = db.relationship('User', back_populates='agenda')
    


    def __init__(self, diasemana, horainicio, horafin, idusuario):
        self.diasemana = diasemana
        self.horainicio = horainicio
        self.horafin = horafin
        self.idusuario = idusuario


    def save(self):
        db.session.add(self)
        db.session.commit()