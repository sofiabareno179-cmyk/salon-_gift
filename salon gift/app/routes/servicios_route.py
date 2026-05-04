from flask import Blueprint, request, jsonify,render_template
from app.models.servicios import Servicio 
from app import db

bp = Blueprint('servicio', __name__, url_prefix='/Servicio')

@bp.route('/servicios', methods=['GET'])
def get_servicios():
    servicios = Servicio.query.all()
    return jsonify([s.to_dict() for s in servicios]), 200
@bp.route('/peluqueria')
def ver_peluqueria():
    servicios = Servicio.query.all() 
    return render_template('servicio/peluqueria.html', servicios=servicios)
@bp.route('/Tratamiento')
def tratamientos():
    servicios = Servicio.query.all() 
    return render_template('servicio/tratamiento.html', servicios=servicios)
@bp.route('/Manicure')
def manicure():
    servicios = Servicio.query.all() 
    return render_template('servicio/manicure.html', servicios=servicios)
@bp.route('/servicios/<int:id>', methods=['GET'])
def get_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    return jsonify(servicio.to_dict()), 200
from flask import render_template, request, redirect, url_for, flash, jsonify

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        duracion = request.form.get('duracion')

        # Validación: evitar servicios con el mismo nombre si es necesario
        if Servicio.query.filter_by(nombre=nombre).first():
            flash(f"El servicio '{nombre}' ya existe.", "danger")
            return redirect(url_for('servicio.add'))

        try:
            nuevo_servicio = Servicio(
                nombre=nombre, 
                precio=precio, 
                duracion=duracion
            )
            db.session.add(nuevo_servicio)
            db.session.commit()
            flash(f"Servicio '{nombre}' creado con éxito.", "success")
            return redirect(url_for('servicio.index')) # Ajusta 'servicio.index' a tu ruta principal
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear el servicio: {str(e)}", "danger")
            
    return render_template('servicios/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    servicio = Servicio.query.get_or_404(id)  
    if request.method == 'POST':
        servicio.nombre = request.form.get('nombre')
        servicio.precio = request.form.get('precio')
        servicio.duracion = request.form.get('duracion')
        
        try:
            db.session.commit()
            flash("Servicio actualizado correctamente.", "success")
            return redirect(url_for('servicio.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar: {str(e)}", "danger")

    return render_template('servicios/edit.html', servicio=servicio)

@bp.route('/delete/<int:id>')
def delete(id):
    servicio = Servicio.query.get_or_404(id)
    try:
        db.session.delete(servicio)
        db.session.commit()
        flash(f"Servicio '{servicio.nombre}' eliminado.", "warning")
    except Exception as e:
        db.session.rollback()
        flash(f"No se pudo eliminar el servicio: {str(e)}", "danger")
        
    return redirect(url_for('servicio.index'))

# --- API / JSON (Igual que el de usuarios) ---

@bp.route('/js')
def indexjs():
    data = Servicio.query.all()
    # Asegúrate de tener el método to_dict() en tu modelo Servicio
    result = [s.to_dict() for s in data] 
    return jsonify(result)