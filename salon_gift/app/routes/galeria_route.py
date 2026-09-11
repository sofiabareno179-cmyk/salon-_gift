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

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'webm', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def es_video(filename):
    return filename.rsplit('.', 1)[1].lower() in {'mp4', 'webm', 'mov', 'avi'}

bp = Blueprint('galeria', __name__, url_prefix='/Galeria')

@bp.route('/ver')
@login_required
def ver_galeria():
    items = Galeria.query.order_by(Galeria.fecha_subida.desc()).all()
    return render_template('galeria/ver_galeria.html', items=items)

@bp.route('/')
@login_required
def index():
    items = Galeria.query.order_by(Galeria.fecha_subida.desc()).all()
    return render_template('galeria/index.html', items=items)

@bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@admin_required
def nueva():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        tipo = request.form.get('tipo', 'imagen')
        file = request.files.get('archivo')

        if not titulo:
            flash('El título es obligatorio', 'danger')
            return redirect(url_for('galeria.nueva'))

        if not file or not file.filename:
            flash('Debes seleccionar un archivo', 'danger')
            return redirect(url_for('galeria.nueva'))

        if not allowed_file(file.filename):
            flash('Formato no válido (png, jpg, jpeg, gif, webp, mp4, webm, mov, avi)', 'danger')
            return redirect(url_for('galeria.nueva'))

        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'galeria')
        os.makedirs(upload_dir, exist_ok=True)
        file.save(os.path.join(upload_dir, filename))

        tipo_real = 'video' if es_video(filename) else 'imagen'
        item = Galeria(titulo=titulo, archivo=filename, tipo=tipo_real, descripcion=descripcion)
        item.save()
        flash(f'{"Video" if tipo_real == "video" else "Imagen"} agregado a la galería', 'success')
        return redirect(url_for('galeria.index'))

    return render_template('galeria/add.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    item = Galeria.query.get_or_404(id)

    if request.method == 'POST':
        item.titulo = request.form.get('titulo')
        item.descripcion = request.form.get('descripcion')
        file = request.files.get('archivo')

        if file and file.filename:
            if not allowed_file(file.filename):
                flash('Formato no válido', 'danger')
                return redirect(url_for('galeria.editar', id=id))

            old_path = os.path.join(current_app.root_path, 'static', 'uploads', 'galeria', item.archivo)
            if os.path.exists(old_path):
                os.remove(old_path)

            filename = secure_filename(file.filename)
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'galeria')
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, filename))
            item.archivo = filename
            item.tipo = 'video' if es_video(filename) else 'imagen'

        db.session.commit()
        flash('Elemento actualizado', 'info')
        return redirect(url_for('galeria.index'))

    return render_template('galeria/edit.html', item=item)

@bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar(id):
    item = Galeria.query.get_or_404(id)
    file_path = os.path.join(current_app.root_path, 'static', 'uploads', 'galeria', item.archivo)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(item)
    db.session.commit()
    flash('Elemento eliminado de la galería', 'warning')
    return redirect(url_for('galeria.index'))