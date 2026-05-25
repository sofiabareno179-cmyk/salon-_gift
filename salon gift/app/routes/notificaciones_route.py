from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models.citas import Citas
from app.models.notificacion import Notificacion

bp = Blueprint('notificaciones', __name__, url_prefix='/Notificaciones')


def sync_proxima_cita_notification():
    proxima_cita = Citas.query.filter(
        Citas.idusuario == current_user.idusuario,
        Citas.fechahora >= datetime.utcnow()
    ).order_by(Citas.fechahora.asc()).first()

    if not proxima_cita:
        return

    titulo = 'Próxima cita'
    mensaje = (
        f'Tu próxima cita es {proxima_cita.servicio} '
        f'el {proxima_cita.fechahora.strftime("%d/%m/%Y %H:%M")}'
    )

    notif = Notificacion.query.filter_by(idusuario=current_user.idusuario, titulo=titulo).order_by(
        Notificacion.fecha_creacion.desc()
    ).first()

    if notif and notif.mensaje == mensaje:
        if notif.leida:
            notif.leida = False
            db.session.commit()
        return

    if notif:
        notif.mensaje = mensaje
        notif.leida = False
        db.session.commit()
        return

    nueva_notif = Notificacion(idusuario=current_user.idusuario, titulo=titulo, mensaje=mensaje)
    db.session.add(nueva_notif)
    db.session.commit()


@bp.route('/')
@login_required
def index():
    sync_proxima_cita_notification()
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