from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.models.servicios import Servicio 
from app import db

bp = Blueprint('servicio', __name__, url_prefix='/Servicio')

# --- VISTAS PARA EL FRONTEND ---

@bp.route('/peluqueria')
def ver_peluqueria():
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
        
        try:
            db.session.add(nuevo_servicio)
            db.session.commit()
            flash(f'Servicio "{nombre}" agregado exitosamente', 'success')
            
            # Redirección dinámica basada en la categoría
            vistas = {
                'peluqueria': 'servicio.ver_peluqueria',
                'tratamiento': 'servicio.tratamientos',
                'manicure': 'servicio.manicure'
            }
            # Si la categoría no está en el mapa, vuelve al index
            return redirect(url_for(vistas.get(categoria, 'servicio.index')))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar: {str(e)}", "danger")

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
            # Cambié 'indexjs' por 'index' que es la ruta que tienes definida abajo
            return redirect(url_for('servicio.index')) 
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar: {str(e)}", "danger")

    return render_template('servicio/edit.html', servicio=servicio)

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

# --- VISTA GENERAL Y API ---

@bp.route('/')
def index():
    servicios = Servicio.query.all() 
    return render_template('servicio/index.html', servicios=servicios)

@bp.route('/api/servicios/<int:id>', methods=['GET'])
def get_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    # Asegúrate de que tu modelo Servicio tenga el método to_dict()
    return jsonify(servicio.to_dict()), 200