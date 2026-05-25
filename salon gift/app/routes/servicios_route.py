from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, current_app
from app.models.servicios import Servicio 
from flask_login import login_required
from app import db
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
@login_required
def add(categoria):
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        duracion = request.form.get('duracion')
        categoria_form = request.form.get('categoria') or categoria
        
        # Manejo de imagen
        imagen_filename = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Crear el directorio si no existe
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'servicios')
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                
                file.save(os.path.join(upload_path, filename))
                imagen_filename = filename

        nuevo_servicio = Servicio(
            nombre=nombre, 
            precio=precio, 
            duracion=duracion, 
            categoria=categoria_form,
            imagen=imagen_filename
        )
        db.session.add(nuevo_servicio)
        db.session.commit()
        
        flash(f'Servicio "{nombre}" agregado exitosamente a {categoria_form}', 'success')
        
        if categoria_form == 'peluqueria':
            return redirect(url_for('servicio.ver_peluqueria'))
        elif categoria_form == 'tratamiento':
            return redirect(url_for('servicio.tratamientos'))
        elif categoria_form == 'manicure':
            return redirect(url_for('servicio.manicure'))
        return redirect(url_for('servicio.index'))
    return render_template('servicio/add_servicio.html', categoria=categoria)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    servicio = Servicio.query.get_or_404(id)  
    if request.method == 'POST':
        servicio.nombre = request.form.get('nombre')
        servicio.precio = request.form.get('precio')
        servicio.duracion = request.form.get('duracion')
        servicio.categoria = request.form.get('categoria')
        
        # Manejo de nueva imagen si se sube
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'servicios')
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                file.save(os.path.join(upload_path, filename))
                servicio.imagen = filename
        
        try:
            db.session.commit()
            flash("Servicio actualizado correctamente.", "success")
            return redirect(url_for('servicio.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar: {str(e)}", "danger")

    return render_template('servicio/edit.html', servicio=servicio)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
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