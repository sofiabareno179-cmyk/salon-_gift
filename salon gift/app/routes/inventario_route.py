from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.inventario import Inventario 

bp = Blueprint('inventario', __name__,url_prefix='/Inventario')

@bp.route('/inventario')
@login_required
def listar_inventario():
    items = Inventario.query.all()
    return render_template('inventario/index.html', inventario=items)

@bp.route('/inventario/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_item():
    if request.method == 'POST':
       
        try:
            stock = int(request.form.get('stock'))
            fecha = request.form.get('fecha')
            
            nuevo_registro = Inventario(stock=stock, fecha=fecha)
            nuevo_registro.save()
            
            flash('Inventario actualizado correctamente', 'success')
            return redirect(url_for('inventario.listar_inventario'))
        except ValueError:
            flash('Error: El stock debe ser un número entero', 'danger')
            return redirect(url_for('inventario.nuevo_item'))
            
    return render_template('inventario/add.html')

@bp.route('/inventario/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_item(id):
    item = Inventario.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            item.stock = int(request.form.get('stock'))
            item.fecha = request.form.get('fecha')
            
            db.session.commit()
            flash('Registro de inventario actualizado', 'info')
            return redirect(url_for('inventario.listar_inventario'))
        except ValueError:
            flash('Error: El stock debe ser un número válido', 'danger')
            
    return render_template('inventario/index.html', item=item)

@bp.route('/inventario/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_item(id):
    item = Inventario.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Registro eliminado del inventario', 'warning')
    return redirect(url_for('inventario.listar_inventario'))