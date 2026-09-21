from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime
from app import db
from app.models.bloqueo import Bloqueo

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or getattr(current_user, 'rol', None) != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

bp = Blueprint('bloqueos', __name__, url_prefix='/Bloqueos')

@bp.route('/')
@login_required
@admin_required
def index():
    bloqueos = Bloqueo.query.order_by(Bloqueo.fecha.desc(), Bloqueo.hora_inicio).all()
    return render_template('bloqueos/index.html', bloqueos=bloqueos)

@bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def nuevo():
    if request.method == 'POST':
        fecha_str = request.form.get('fecha')
        hora_inicio = request.form.get('hora_inicio')
        hora_fin = request.form.get('hora_fin')
        motivo = request.form.get('motivo')

        if not fecha_str or not hora_inicio or not hora_fin:
            flash('Fecha, hora inicio y hora fin son obligatorios', 'danger')
            return redirect(url_for('bloqueos.nuevo'))

        if hora_inicio >= hora_fin:
            flash('La hora de fin debe ser mayor a la hora de inicio', 'danger')
            return redirect(url_for('bloqueos.nuevo'))

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Fecha inválida', 'danger')
            return redirect(url_for('bloqueos.nuevo'))

        bloqueo = Bloqueo(fecha=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin, idusuario=current_user.idusuario, motivo=motivo)
        bloqueo.save()
        flash('Horario bloqueado correctamente', 'success')
        return redirect(url_for('bloqueos.index'))

    return render_template('bloqueos/add.html')

@bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar(id):
    bloqueo = Bloqueo.query.get_or_404(id)
    db.session.delete(bloqueo)
    db.session.commit()
    flash('Bloqueo eliminado', 'info')
    return redirect(url_for('bloqueos.index'))