from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.notificacion import Notificacion

bp = Blueprint('notificaciones', __name__, url_prefix='/Notificaciones')

@bp.route('/')
@login_required
def index():
    notifs = Notificacion.query.filter_by(idusuario=current_user.idusuario).order_by(Notificacion.fecha_creacion.desc()).all()
    return render_template('notificaciones/index.html', notificaciones=notifs)

@bp.route('/marcar-leida/<int:id>')
@login_required
def marcar_leida(id):
    notif = Notificacion.query.get_or_404(id)
    if notif.idusuario != current_user.idusuario:
        flash('No autorizado', 'danger')
        return redirect(url_for('notificaciones.index'))
    notif.leida = True
    db.session.commit()
    return redirect(url_for('notificaciones.index'))

@bp.route('/marcar-todas')
@login_required
def marcar_todas():
    Notificacion.query.filter_by(idusuario=current_user.idusuario, leida=False).update({'leida': True})
    db.session.commit()
    flash('Todas las notificaciones marcadas como leídas', 'info')
    return redirect(url_for('notificaciones.index'))