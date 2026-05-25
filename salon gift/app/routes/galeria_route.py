import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.utils import secure_filename
from app import db
from app.models.galeria import Galeria

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or getattr(current_user, 'rol', None) != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bp = Blueprint('galeria', __name__, url_prefix='/Galeria')

@bp.route('/')
@login_required
def index():
    imagenes = Galeria.query.order_by(Galeria.fecha_subida.desc()).all()
    return render_template('galeria/index.html', imagenes=imagenes)

@bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@admin_required
def nueva():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        file = request.files.get('imagen')

        if not titulo:
            flash('El título es obligatorio', 'danger')
            return redirect(url_for('galeria.nueva'))

        if not file or not file.filename:
            flash('Debes seleccionar una imagen', 'danger')
            return redirect(url_for('galeria.nueva'))

        if not allowed_file(file.filename):
            flash('Formato de imagen no válido (png, jpg, jpeg, gif, webp)', 'danger')
            return redirect(url_for('galeria.nueva'))

        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'galeria')
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)

        imagen = Galeria(titulo=titulo, imagen=filename, descripcion=descripcion)
        imagen.save()
        flash('Imagen agregada a la galería', 'success')
        return redirect(url_for('galeria.index'))

    return render_template('galeria/add.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    imagen = Galeria.query.get_or_404(id)

    if request.method == 'POST':
        imagen.titulo = request.form.get('titulo')
        imagen.descripcion = request.form.get('descripcion')
        file = request.files.get('imagen')

        if file and file.filename:
            if not allowed_file(file.filename):
                flash('Formato de imagen no válido', 'danger')
                return redirect(url_for('galeria.editar', id=id))

            old_path = os.path.join(current_app.root_path, 'static', 'uploads', 'galeria', imagen.imagen)
            if os.path.exists(old_path):
                os.remove(old_path)

            filename = secure_filename(file.filename)
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'galeria')
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, filename))
            imagen.imagen = filename

        db.session.commit()
        flash('Imagen actualizada', 'info')
        return redirect(url_for('galeria.index'))

    return render_template('galeria/edit.html', imagen=imagen)

@bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar(id):
    imagen = Galeria.query.get_or_404(id)
    file_path = os.path.join(current_app.root_path, 'static', 'uploads', 'galeria', imagen.imagen)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(imagen)
    db.session.commit()
    flash('Imagen eliminada de la galería', 'warning')
    return redirect(url_for('galeria.index'))