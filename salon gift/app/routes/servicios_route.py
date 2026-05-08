from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.models.servicios import Servicio 
from app import db

bp = Blueprint('servicio', __name__, url_prefix='/Servicio')

# --- VISTAS PARA EL FRONTEND ---

@bp.route('/peluqueria')
def ver_peluqueria():
    # Filtramos por categoría para que la página sea específica
    servicios = Servicio.query.filter_by(categoria='peluqueria').all() 
    return render_template('servicio/peluqueria.html', servicios=servicios)

@bp.route('/Tratamiento')
def tratamientos():
    servicios = Servicio.query.filter_by(categoria='tratamiento').all() 
    return render_template('servicio/tratamiento.html', servicios=servicios)

@bp.route('/Manicure')
def manicure():
    servicios = Servicio.query.filter_by(categoria='manicure').all() 
    return render_template('servicio/manicure.html', servicios=servicios)

# --- OPERACIONES CRUD ---

@bp.route('/servicios/add/<categoria>', methods=['GET', 'POST'])
def add(categoria):
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        duracion = request.form.get('duracion')
        
        nuevo_servicio = Servicio(
            nombre=nombre, 
            precio=precio, 
            duracion=duracion, 
            categoria=categoria
        )
        db.session.add(nuevo_servicio)
        db.session.commit()
        
        flash(f'Servicio "{nombre}" agregado exitosamente a {categoria}', 'success')
        # Redirige a la vista de la categoría que acabas de agregar
        if categoria == 'peluqueria':
            return redirect(url_for('servicio.ver_peluqueria'))
            
        elif categoria == 'tratamiento':
            # Esto lo enviará a la función tratamientos() que carga tratamiento.html
            if categoria == 'peluqueria':
               return redirect(url_for('servicio.ver_peluqueria'))
            
        elif categoria == 'tratamiento':
            # Esto lo enviará a la función tratamientos() que carga tratamiento.html
             return redirect(url_for('servicio.tratamientos'))
            
        elif categoria == 'manicure':
             return redirect(url_for('servicio.manicure'))
            
        elif categoria == 'manicure':
            return redirect(url_for('servicio.manicure'))
        return redirect(url_for('servicio.index'))
    return render_template('servicio/add_servicio.html', categoria=categoria)

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
            return redirect(url_for('servicio.indexjs')) # Ajustado al nombre real de la función
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
        
    return redirect(url_for('servicio.indexjs'))

# --- API / JSON ---

@bp.route('/')
def index():
    # Traemos todos los servicios sin filtrar por categoría
    servicios = Servicio.query.all() 
    return render_template('servicio/index.html', servicios=servicios)
@bp.route('/servicios/<int:id>', methods=['GET'])
def get_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    return jsonify(servicio.to_dict()), 200