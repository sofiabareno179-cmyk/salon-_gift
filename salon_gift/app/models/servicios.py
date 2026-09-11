from app import db

# Tabla intermedia para Servicios y Productos
servicio_productos = db.Table('servicio_productos',
    db.Column('servicio_id', db.Integer, db.ForeignKey('servicios.idservicio'), primary_key=True),
    db.Column('producto_id', db.Integer, db.ForeignKey('productos.idproductos'), primary_key=True)
)

class Servicio(db.Model): 
    __tablename__ = 'servicios'
    
    idservicio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False) 
    duracion = db.Column(db.String(250), nullable=False)  
    categoria = db.Column(db.String(50), nullable=False) 
    imagen = db.Column(db.String(255), nullable=True)
    idcitas = db.Column(db.Integer, db.ForeignKey('citas.idcitas'), nullable=True, unique=True)
    citas = db.relationship('Citas', back_populates='servicios')
    
    productos = db.relationship('Productos', secondary=servicio_productos, backref='servicios')

    def __init__(self, nombre, precio, duracion, categoria, imagen=None):
        self.nombre = nombre
        self.precio = precio
        self.duracion = duracion
        self.categoria = categoria
        self.imagen = imagen

    def to_dict(self):
        return {
            "idservicio": self.idservicio,
            "nombre": self.nombre,
            "precio": float(self.precio),
            "duracion": self.duracion,
            "categoria": self.categoria,
            "imagen": self.imagen
        }

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e