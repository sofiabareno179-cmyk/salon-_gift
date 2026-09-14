import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.frases import Frase

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or getattr(current_user, 'rol', None) != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

bp = Blueprint('frases', __name__, url_prefix='/Frases')

@bp.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def editar():
    frase = Frase.query.filter_by(activa=True).order_by(Frase.idpromocion.asc()).first()
    if not frase:
        frase = Frase(titulo='✨ Frase del Día ✨', descripcion='El éxito es la suma de pequeños esfuerzos repetidos día tras día.', activa=True)
        frase.save()

    if request.method == 'POST':
        frase.titulo = request.form.get('titulo')
        frase.descripcion = request.form.get('descripcion')
        frase.activa = 'activa' in request.form
        for otra in Frase.query.filter(Frase.idpromocion != frase.idpromocion).all():
            otra.activa = False
        db.session.commit()
        flash('Frase motivadora actualizada', 'success')
        return redirect(url_for('frases.editar'))

    return render_template('frases/edit.html', frase=frase)