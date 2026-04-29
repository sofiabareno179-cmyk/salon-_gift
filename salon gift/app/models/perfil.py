from app import db

class Perfil(db.Model):
    __tablename__ = 'perfiles'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    
    # Llave foránea que conecta con el modelo User
    idusuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, unique=True)

    def __init__(self, nombre, apellido, bio, idusuario):
        self.nombre = nombre
        self.apellido = apellido
        self.bio = bio
        self.idusuario = idusuario

    def __repr__(self):
        return f'<Perfil {self.nombre}>'