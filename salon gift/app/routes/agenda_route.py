from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.agenda import Agenda  
import os
from dotenv import load_dotenv

load_dotenv()
bp = Blueprint('agenda', __name__, url_prefix='/Agenda')

@bp.route('/agendas')
@login_required
def listar_agendas():
    agendas = Agenda.query.all()
    return render_template('agenda/index.html', agendas=agendas)

@bp.route('/agenda/nuevo', methods=['GET', 'POST'])
@login_required
def crear_agenda():
    if request.method == 'POST':
        diasemana = request.form.get('diasemana')
        horainicio = request.form.get('horainicio')
        horafin = request.form.get('horafin')

        nueva_agenda = Agenda(diasemana=diasemana, horainicio=horainicio, horafin=horafin)
        nueva_agenda.save()
        
        flash('Agenda creada exitosamente', 'success')
        return redirect(url_for('agenda.listar_agendas'))
    
    return render_template('agenda/add.html')

@bp.route('/agenda/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_agenda(id):
    agenda = Agenda.query.get_or_404(id)
    
    if request.method == 'POST':
        agenda.diasemana = request.form.get('diasemana')
        agenda.horainicio = request.form.get('horainicio')
        agenda.horafin = request.form.get('horafin')
        
        db.session.commit()
        flash('Agenda actualizada', 'info')
        return redirect(url_for('agenda.listar_agendas'))
    
    return render_template('agenda/index.html', agenda=agenda)

@bp.route('/agenda/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_agenda(id):
    agenda = Agenda.query.get_or_404(id)
    db.session.delete(agenda)
    db.session.commit()
    flash('Agenda eliminada correctamente', 'danger')
    return redirect(url_for('agenda.listar_agendas'))