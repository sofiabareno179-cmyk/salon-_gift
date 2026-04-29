from flask_login import UserMixin
from app import db

class Inventario(db.Model, UserMixin): 
    __tablename__ = 'inventario'
    
    idinventario = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.String(100), nullable=False) 

    def __init__(self, stock, fecha):
        self.stock = stock
        self.fecha = fecha

    def get_id(self):
        return str(self.idinventario)

    def save(self):
        db.session.add(self)
        db.session.commit()