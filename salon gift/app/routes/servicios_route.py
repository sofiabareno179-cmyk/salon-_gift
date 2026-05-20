from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, current_app
from app.models.servicios import Servicio 
from app import db
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bp = Blueprint('servicio', __name__, url_prefix='/Servicio')

#  VISTAS PARA EL FRONTEND 

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

# OPERACIONES CRUD 

@bp.route('/servicios/add/<categoria>', methods=['GET', 'POST'])
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
        

        flash(f'Servicio "{nombre}" agregado exitosamente a {categoria_form}', 'success')
        
        if categoria_form == 'peluqueria':
            return redirect(url_for('servicio.ver_peluqueria'))
        elif categoria_form == 'tratamiento':
            return redirect(url_for('servicio.tratamientos'))
        elif categoria_form == 'manicure':
            return redirect(url_for('servicio.manicure'))
        return redirect(url_for('servicio.index'))

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

#  VISTA GENERAL Y API 

@bp.route('/')
def index():
    servicios = Servicio.query.all() 
    return render_template('servicio/index.html', servicios=servicios)

@bp.route('/api/servicios/<int:id>', methods=['GET'])
def get_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    # Asegúrate de que tu modelo Servicio tenga el método to_dict()
    return jsonify(servicio.to_dict()), 200