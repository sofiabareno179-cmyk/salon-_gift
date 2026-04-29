from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db  # Asegúrate de que 'db' esté inicializado en tu __init__.py

class Perfil(db.Model):
    __tablename__ = 'perfil'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False)

    user = db.relationship("User", back_populates="perfil")
    
    def __repr__(self):
        return f"<Perfil id={self.id}, nombre={self.nombre} {self.apellido}>"