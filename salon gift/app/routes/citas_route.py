from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.citas import Citas 

bp = Blueprint('citas', __name__,url_prefix='/Citas')

@bp.route('/citas')
@login_required
def listar_citas():
    todas_las_citas = Citas.query.all()
    return render_template('citas/index.html', citas=todas_las_citas)

@bp.route('/citas/nueva', methods=['GET', 'POST'])
@login_required
def nueva_cita():
    if request.method == 'POST':
        fechahora = request.form.get('fechahora')
        estado = request.form.get('estado', 'Pendiente') 

        if not fechahora:
            flash('La fecha y hora son obligatorias', 'warning')
            return redirect(url_for('citas.nueva_cita'))

        cita = Citas(fechahora=fechahora, estado=estado)
        cita.save()
        
        flash('Cita agendada correctamente', 'success')
        return redirect(url_for('citas.listar_citas'))
    
    return render_template('citas/add.html')

@bp.route('/citas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cita(id):
    cita = Citas.query.get_or_404(id)
    
    if request.method == 'POST':
        cita.fechahora = request.form.get('fechahora')
        cita.estado = request.form.get('estado')
        
        db.session.commit()
        flash('Cita actualizada con éxito', 'info')
        return redirect(url_for('citas.listar_citas'))
    
    return render_template('citas/index.html', cita=cita)
@bp.route('/citas/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_cita(id):
    cita = Citas.query.get_or_404(id)
    db.session.delete(cita)
    db.session.commit()
    flash('Cita eliminada permanentemente', 'danger')
    return redirect(url_for('citas.listar_citas'))