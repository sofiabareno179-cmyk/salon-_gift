from app import db

class Servicio(db.Model): 
    __tablename__ = 'servicios'
    
    idservicio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False) 
    duracion = db.Column(db.String(250), nullable=False)

    def __init__(self, nombre, precio, duracion):
        self.nombre = nombre
        self.precio = precio
        self.duracion = duracion

    def to_dict(self):
        return {
            "idservicio": self.idservicio,
            "nombre": self.nombre,
            "precio": float(self.precio),
            "duracion": self.duracion
        }

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e