from flask_login import UserMixin
from app import db
from io import BytesIO
import base64
import os
from flask import url_for, current_app
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model, UserMixin): 

    __tablename__='usuario'

    __tablename__ = 'usuario'  # Nombre de la tabla

    idusuario = db.Column(db.Integer, primary_key=True)
    nombreuser = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)

    rol = db.Column(db.String(20), nullable=False, default='cliente')

    def __repr__(self):
        return f'<Usuario {self.nombreuser} - Rol {self.rol}>' # Corregido


    # El back_populates debe apuntar al nombre de la VARIABLE en la clase Perfil (que es 'user')
    perfil = db.relationship("Perfil", back_populates="user", uselist=False)

    def __init__(self, nombreuser, email, password, telefono, rol='cliente'):
        self.nombreuser = nombreuser
        self.email = email
        self.telefono = telefono
        self.rol = rol
        self.set_password(password)


    def get_id(self):
        return str(self.idusuario)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "idusuario": self.idusuario,
            "nombreuser": self.nombreuser,
            "email": self.email,
            "telefono": self.telefono,
            "rol": self.rol
        }
    def save(self):
        db.session.add(self)
        db.session.commit()
