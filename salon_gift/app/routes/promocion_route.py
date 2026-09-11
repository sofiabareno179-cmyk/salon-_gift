from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.promocion import Promocion

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or getattr(current_user, 'rol', None) != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

bp = Blueprint('promocion', __name__, url_prefix='/Promocion')

@bp.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def editar():
    promo = Promocion.query.first()
    if not promo:
        promo = Promocion(titulo='✨ Promo del Mes ✨', descripcion='Trae a una amiga y ambas obtienen un 15% de descuento en tratamientos de hidratación.', activa=True)
        promo.save()

    if request.method == 'POST':
        promo.titulo = request.form.get('titulo')
        promo.descripcion = request.form.get('descripcion')
        promo.activa = 'activa' in request.form
        db.session.commit()
        flash('Promoción actualizada', 'success')
        return redirect(url_for('promocion.editar'))

    return render_template('promocion/edit.html', promo=promo)