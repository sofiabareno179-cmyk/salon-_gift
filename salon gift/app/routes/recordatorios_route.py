from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.recordatorios import Recordatorios

bp = Blueprint('recordatorios', __name__,url_prefix='/Recordatorios')

@bp.route('/recordatorios')
@login_required
def listar_recordatorios():
    lista = Recordatorios.query.order_by(Recordatorios.fecha_recordatorio).all()
    return render_template('recordatorios/index.html', recordatorios=lista)

@bp.route('/recordatorios/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_recordatorio():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        mensaje = request.form.get('mensaje')
        fecha = request.form.get('fecha_recordatorio')
      
        nuevo_rec = Recordatorios(
            titulo=titulo, 
            mensaje=mensaje, 
            fecha_recordatorio=fecha,
            prioridad="Media" 
        )
        
        nuevo_rec.save()
        flash('Recordatorio programado con éxito', 'success')
        return redirect(url_for('recordatorios.listar_recordatorios'))
    
    return render_template('recordatorios/add.html')

@bp.route('/recordatorios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_recordatorio(id):
    recordatorio = Recordatorios.query.get_or_404(id)
    
    if request.method == 'POST':
        recordatorio.titulo = request.form.get('titulo')
        recordatorio.mensaje = request.form.get('mensaje')
        recordatorio.fecha_recordatorio = request.form.get('fecha_recordatorio')
        
        db.session.commit()
        flash('Recordatorio actualizado', 'info')
        return redirect(url_for('recordatorios.listar_recordatorios'))
    
    return render_template('recordatorios/editar.html', recordatorio=recordatorio)

@bp.route('/recordatorios/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_recordatorio(id):
    recordatorio = Recordatorios.query.get_or_404(id)
    db.session.delete(recordatorio)
    db.session.commit()
    flash('Recordatorio borrado', 'warning')
    return redirect(url_for('recordatorios.listar_recordatorios'))