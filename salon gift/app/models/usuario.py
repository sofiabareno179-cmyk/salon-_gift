from flask_login import UserMixin
from app import db
from datetime import datetime
from io import BytesIO
import base64
import os
from flask import url_for, current_app
from werkzeug.security import generate_password_hash,check_password_hash
class User(db.Model, UserMixin): 
    __tablename__='usuario'
    idusuario=db.Column(db.Integer,primary_key=True)
    nombreuser=db.Column(db.String(100),unique=True,nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password_hash=db.Column(db.String(250),nullable=False)
    telefono=db.Column(db.String(20), nullable=True)
    def __init__(self, nombreuser, email, password,telefono):
        self.nombreuser = nombreuser
        self.email = email
        self.telefono = telefono
        self.set_password(password)
    def get_id(self):
        return str(self.idusuario)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash,password)
    def to_dict(self):
        return {
            "idsuario": self.idusuario,
            "nombreuser": self.nombreuser,
            "email": self.email,
            "telefono":self.telefono
        }
    def save(self):
        db.session.add(self)
        db.session.commit()
