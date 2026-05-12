from app import db

class SlotBloqueado(db.Model):
    __tablename__ = 'slots_bloqueados'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    motivo = db.Column(db.String(200), nullable=True)
    creado_por = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relación con usuario
    usuario = db.relationship('User', backref='slots_bloqueados')

    def __repr__(self):
        return f'<SlotBloqueado {self.fecha} {self.hora}>'