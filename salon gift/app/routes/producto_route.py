from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.productos import Productos

bp = Blueprint('productos', __name__,url_prefix='/Productos')

@bp.route('/productos')
@login_required
def listar_productos():
 
    lista_productos = Productos.query.order_by(Productos.categoria).all()
    return render_template('productos/index.html', productos=lista_productos)

@bp.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        categoria = request.form.get('categoria')

        try:
            precio_float = float(precio)
            
            producto = Productos(
                nombre=nombre, 
                descripcion=descripcion, 
                precio=precio_float, 
                categoria=categoria
            )
            producto.save()
            
            flash(f'Producto "{nombre}" registrado con éxito', 'success')
            return redirect(url_for('productos.listar_productos'))
        
        except ValueError:
            flash('Error: El precio debe ser un valor numérico (ej: 10.50)', 'danger')
            return redirect(url_for('productos.nuevo_producto'))
    
    return render_template('productos/add.html')

@bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto = Productos.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            producto.nombre = request.form.get('nombre')
            producto.descripcion = request.form.get('descripcion')
            producto.precio = float(request.form.get('precio'))
            producto.categoria = request.form.get('categoria')
            
            db.session.commit()
            flash('Producto actualizado correctamente', 'info')
            return redirect(url_for('productos.listar_productos'))
        except ValueError:
            flash('Error en el formato del precio', 'danger')
            
    return render_template('productos/index.html', producto=producto)

@bp.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    producto = Productos.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash(f'El producto {producto.nombre} ha sido eliminado', 'warning')
    return redirect(url_for('productos.listar_productos'))