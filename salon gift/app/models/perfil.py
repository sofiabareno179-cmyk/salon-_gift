from app import db

class Perfil(db.Model):
    __tablename__ = 'perfiles'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    
    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False, unique=True)

    # Relación: "user" es el nombre del atributo en Perfil
    # "perfil_asociado" debe ser el nombre del atributo en User
    user = db.relationship('User', back_populates='perfil_asociado')


    def __init__(self, nombre, apellido, bio, idusuario):
        self.nombre = nombre
        self.apellido = apellido
        self.bio = bio
        self.idusuario = idusuario

    def __repr__(self):
        return f'<Perfil {self.nombre}>'