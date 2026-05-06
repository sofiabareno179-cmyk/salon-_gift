from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required,current_user
from app import db
from datetime import datetime, timedelta
from app.models.citas import Citas 

bp = Blueprint('citas', __name__,url_prefix='/Citas')

@bp.route('/citas')
@login_required
def listar_citas():
    todas_las_citas = Citas.query.all()
    return render_template('citas/index.html', citas=todas_las_citas)
@bp.route('/citas/cronograma')
@login_required
def crono_citas():
    # 1. Gestión de fechas
    fecha_query = request.args.get('fecha')
    if fecha_query:
        try:
            fecha_actual = datetime.strptime(fecha_query, '%Y-%m-%d')
        except:
            fecha_actual = datetime.now()
    else:
        fecha_actual = datetime.now()

    lunes = fecha_actual - timedelta(days=fecha_actual.weekday())
    viernes_fin = (lunes + timedelta(days=4)).replace(hour=23, minute=59, second=59)

    # 2. Obtener citas de la semana para el usuario
    mis_citas = Citas.query.filter(
        Citas.idusuario == current_user.idusuario,
        Citas.fechahora >= lunes.replace(hour=0, minute=0, second=0),
        Citas.fechahora <= viernes_fin
    ).all()
    
    # 3. Mapear citas a la cuadrícula (Día, Hora)
    agenda = {}
    for cita in mis_citas:
        dia_semana = cita.fechahora.weekday() 
        hora_str = cita.fechahora.strftime('%H:00')
        agenda[(dia_semana, hora_str)] = cita

    # 4. Variables de navegación
    horas = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
    anterior = (lunes - timedelta(weeks=1)).strftime('%Y-%m-%d')
    siguiente = (lunes + timedelta(weeks=1)).strftime('%Y-%m-%d')
    hoy = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('citas/crono.html', 
                           agenda=agenda, 
                           horas=horas, 
                           lunes=lunes, 
                           anterior=anterior, 
                           siguiente=siguiente, 
                           hoy=hoy,
                           timedelta=timedelta)
@bp.route('/citas/nueva', methods=['GET', 'POST'])
@login_required # Esto asegura que current_user tenga datos
def nueva_cita():
    if request.method == 'POST':
        fechahora = request.form.get('fechahora')
        servicio = request.form.get('servicio')
        estado = request.form.get('estado', 'Pendiente') 

        # 1. Validar que los datos no estén vacíos
        if not fechahora:
            flash('La fecha es obligatoria', 'warning')
            return redirect(url_for('citas.nueva_cita'))

        # 2. Crear la instancia pasando explícitamente el id del usuario actual
        nueva_cita = Citas(
            fechahora=fechahora,
            servicio=servicio,
            estado=estado,
            idusuario=current_user.idusuario  # <-- AQUÍ ESTABA EL FALLO
        )

        try:
            db.session.add(nueva_cita)
            db.session.commit()
            flash('Cita agendada correctamente', 'success')
            return redirect(url_for('citas.crono_citas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar: {str(e)}', 'danger')
            return redirect(url_for('citas.nueva_cita'))
    
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