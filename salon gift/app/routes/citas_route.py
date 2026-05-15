from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required,current_user
from app import db
from datetime import datetime, timedelta
from app.models.agenda import Agenda
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
    # Verificar si es admin
    es_admin = current_user.rol == 'admin'

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

    # 2. Obtener citas de la semana
    if es_admin:
        # Admin ve todas las citas
        todas_citas = Citas.query.filter(
            Citas.fechahora >= lunes.replace(hour=0, minute=0, second=0),
            Citas.fechahora <= viernes_fin
        ).all()
    else:
        # Usuario normal ve solo sus citas
        todas_citas = Citas.query.filter(
            Citas.idusuario == current_user.idusuario,
            Citas.fechahora >= lunes.replace(hour=0, minute=0, second=0),
            Citas.fechahora <= viernes_fin
        ).all()

    # 3. Obtener slots bloqueados
    from app.models.slot_bloqueado import SlotBloqueado
    slots_bloqueados = SlotBloqueado.query.filter(
        SlotBloqueado.fecha >= lunes.date(),
        SlotBloqueado.fecha <= viernes_fin.date()
    ).all()

    # 4. Mapear citas a la cuadrícula (Día, Hora)
    agenda = {}
    for cita in todas_citas:
        cita_fecha = cita.fecha_dt
        dia_semana = cita_fecha.weekday()
        hora_str = cita_fecha.strftime('%H:00')
        agenda[(dia_semana, hora_str)] = cita

    # 5. Mapear slots bloqueados
    slots_bloqueados_dict = {}
    for slot in slots_bloqueados:
        dia_semana = slot.fecha.weekday()
        hora_str = slot.hora.strftime('%H:00')
        slots_bloqueados_dict[(dia_semana, hora_str)] = slot

    # 6. Generar horas según configuración de agenda o usar horario por defecto
    agenda_config = Agenda.query.filter_by(idusuario=current_user.idusuario).first()
    if agenda_config:
        try:
            inicio = datetime.strptime(agenda_config.horainicio, '%H:%M')
            fin = datetime.strptime(agenda_config.horafin, '%H:%M')
            horas = []
            hora_actual = inicio
            while hora_actual <= fin:
                horas.append(hora_actual.strftime('%H:%M'))
                hora_actual += timedelta(hours=1)
        except Exception:
            horas = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
    else:
        horas = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]

    anterior = (lunes - timedelta(weeks=1)).strftime('%Y-%m-%d')
    siguiente = (lunes + timedelta(weeks=1)).strftime('%Y-%m-%d')
    hoy = datetime.now().strftime('%Y-%m-%d')

    return render_template('citas/crono.html',
                           agenda=agenda,
                           slots_bloqueados=slots_bloqueados_dict,
                           horas=horas,
                           lunes=lunes,
                           anterior=anterior,
                           siguiente=siguiente,
                           hoy=hoy,
                           timedelta=timedelta,
                           es_admin=es_admin)
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

        try:
            fechahora_dt = datetime.strptime(fechahora, '%Y-%m-%dT%H:%M')
        except Exception:
            flash('Fecha y hora inválidas', 'warning')
            return redirect(url_for('citas.nueva_cita'))

        # 2. Validar que el slot no esté bloqueado
        from app.models.slot_bloqueado import SlotBloqueado
        bloqueado = SlotBloqueado.query.filter_by(
            fecha=fechahora_dt.date(),
            hora=fechahora_dt.time()
        ).first()
        if bloqueado:
            flash('No se puede agendar en este slot: está bloqueado.', 'warning')
            return redirect(url_for('citas.nueva_cita', fecha=fechahora_dt.strftime('%Y-%m-%d'), hora=fechahora_dt.strftime('%H:%M')))

        # 3. Validar que no haya otra cita en ese horario exacto
        conflict = Citas.query.filter_by(fechahora=fechahora_dt).first()
        if conflict:
            flash('Ya existe una cita en ese horario.', 'warning')
            return redirect(url_for('citas.nueva_cita', fecha=fechahora_dt.strftime('%Y-%m-%d'), hora=fechahora_dt.strftime('%H:%M')))

        # 4. Crear la instancia pasando explícitamente el id del usuario actual
        nueva_cita = Citas(
            fechahora=fechahora_dt,
            servicio=servicio,
            estado=estado,
            idusuario=current_user.idusuario
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


@bp.route('/citas/bloquear-slot', methods=['POST'])
@login_required
def bloquear_slot():
    if current_user.rol != 'admin':
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('citas.crono_citas'))

    fecha_str = request.form.get('fecha')
    hora_str = request.form.get('hora')
    motivo = request.form.get('motivo', '')

    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora = datetime.strptime(hora_str, '%H:%M').time()

        from app.models.slot_bloqueado import SlotBloqueado

        # Verificar si ya está bloqueado
        existente = SlotBloqueado.query.filter_by(fecha=fecha, hora=hora).first()
        if existente:
            flash('Este slot ya está bloqueado', 'warning')
        else:
            nuevo_bloqueo = SlotBloqueado(
                fecha=fecha,
                hora=hora,
                motivo=motivo,
                creado_por=current_user.idusuario
            )
            db.session.add(nuevo_bloqueo)
            db.session.commit()
            flash('Slot bloqueado exitosamente', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al bloquear el slot: {str(e)}', 'error')

    return redirect(url_for('citas.crono_citas', fecha=fecha_str))


@bp.route('/citas/desbloquear-slot/<int:slot_id>', methods=['POST'])
@login_required
def desbloquear_slot(slot_id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('citas.crono_citas'))

    try:
        from app.models.slot_bloqueado import SlotBloqueado
        slot = SlotBloqueado.query.get_or_404(slot_id)
        db.session.delete(slot)
        db.session.commit()
        flash('Slot desbloqueado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al desbloquear el slot: {str(e)}', 'error')

    return redirect(url_for('citas.crono_citas'))