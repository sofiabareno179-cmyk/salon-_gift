from flask_login import UserMixin
from app import db
class Agenda(db.Model, UserMixin): 
    __tablename__ = 'agenda'
    idagenda = db.Column(db.Integer, primary_key=True)
    diasemana = db.Column(db.String(100), nullable=False) 
    horainicio = db.Column(db.String(100), nullable=False) 
    horafin = db.Column(db.String(250), nullable=False)
    def __init__(self, diasemana, horainicio, horafin):
        self.diasemana = diasemana
        self.horainicio = horainicio
        self.horafin = horafin
    def get_id(self):
        return str(self.idagenda)

    def save(self):
        db.session.add(self)
        db.session.commit()