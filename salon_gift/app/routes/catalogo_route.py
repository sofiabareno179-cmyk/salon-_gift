from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.catalogo_precio import CatalogoPrecio

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or getattr(current_user, 'rol', None) != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

bp = Blueprint('catalogo', __name__, url_prefix='/Catalogo')

@bp.route('/ver')
@login_required
def ver_catalogo():
    items = CatalogoPrecio.query.order_by(CatalogoPrecio.categoria).all()
    return render_template('catalogo/ver_catalogo.html', items=items)

@bp.route('/')
@login_required
def index():
    items = CatalogoPrecio.query.order_by(CatalogoPrecio.categoria).all()
    return render_template('catalogo/index.html', items=items)

@bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def nuevo():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        categoria = request.form.get('categoria')
        descripcion = request.form.get('descripcion')

        if not nombre or not precio or not categoria:
            flash('Nombre, precio y categoría son obligatorios', 'danger')
            return redirect(url_for('catalogo.nuevo'))

        try:
            precio_float = float(precio)
        except ValueError:
            flash('El precio debe ser un valor numérico', 'danger')
            return redirect(url_for('catalogo.nuevo'))

        item = CatalogoPrecio(nombre=nombre, precio=precio_float, categoria=categoria, descripcion=descripcion)
        item.save()
        flash(f'"{nombre}" agregado al catálogo', 'success')
        return redirect(url_for('catalogo.index'))

    return render_template('catalogo/add.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    item = CatalogoPrecio.query.get_or_404(id)

    if request.method == 'POST':
        item.nombre = request.form.get('nombre')
        item.categoria = request.form.get('categoria')
        item.descripcion = request.form.get('descripcion')

        try:
            item.precio = float(request.form.get('precio'))
        except ValueError:
            flash('El precio debe ser un valor numérico', 'danger')
            return redirect(url_for('catalogo.editar', id=id))

        db.session.commit()
        flash('Elemento actualizado', 'info')
        return redirect(url_for('catalogo.index'))

    return render_template('catalogo/edit.html', item=item)

@bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar(id):
    item = CatalogoPrecio.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash(f'"{item.nombre}" eliminado del catálogo', 'warning')
    return redirect(url_for('catalogo.index'))