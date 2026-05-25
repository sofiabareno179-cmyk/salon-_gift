from flask import Blueprint, request, jsonify,render_template
from app.models.servicios import Servicio 
from flask_login import login_required
from app import db

bp = Blueprint('servicio', __name__, url_prefix='/Servicio')

<<<<<<< Updated upstream
@bp.route('/servicios', methods=['GET'])
def get_servicios():
    servicios = Servicio.query.all()
    return jsonify([s.to_dict() for s in servicios]), 200
@bp.route('/peluqueria')
def ver_peluqueria():
    servicios = Servicio.query.all() 
=======
#  VISTAS PARA EL FRONTEND 

@bp.route('/peluqueria')
def ver_peluqueria():
    servicios = Servicio.query.filter_by(categoria='peluqueria').all() 
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
@bp.route('/add', methods=['GET', 'POST'])
def add():
=======
# OPERACIONES CRUD 

@bp.route('/servicios/add/<categoria>', methods=['GET', 'POST'])
@login_required
def add(categoria):
>>>>>>> Stashed changes
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        duracion = request.form.get('duracion')

<<<<<<< Updated upstream
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
=======
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
>>>>>>> Stashed changes

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    servicio = Servicio.query.get_or_404(id)  
    if request.method == 'POST':
        servicio.nombre = request.form.get('nombre')
        servicio.precio = request.form.get('precio')
        servicio.duracion = request.form.get('duracion')
        
        try:
            db.session.commit()
            flash("Servicio actualizado correctamente.", "success")
<<<<<<< Updated upstream
            return redirect(url_for('servicio.index'))
=======
<<<<<<< HEAD
            return redirect(url_for('servicio.index'))
=======
            # Cambié 'indexjs' por 'index' que es la ruta que tienes definida abajo
            return redirect(url_for('servicio.index')) 
>>>>>>> a84baa09a112d86e9c3464f7b4ecee06f66b9a8e
>>>>>>> Stashed changes
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar: {str(e)}", "danger")

    return render_template('servicios/edit.html', servicio=servicio)

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

<<<<<<< Updated upstream
# --- API / JSON (Igual que el de usuarios) ---

@bp.route('/js')
def indexjs():
    data = Servicio.query.all()
    # Asegúrate de tener el método to_dict() en tu modelo Servicio
    result = [s.to_dict() for s in data] 
    return jsonify(result)
=======
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
>>>>>>> Stashed changes
