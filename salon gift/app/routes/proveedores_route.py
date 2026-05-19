from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.proveedores import Proveedores

bp = Blueprint('proveedores', __name__,url_prefix='/Proveedores')

@bp.route('/proveedores')
@login_required
def listar_proveedores():
    todos_proveedores = Proveedores.query.order_by(Proveedores.nombre_empresa).all()
    return render_template('proveedores/index.html', proveedores=todos_proveedores)

@bp.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_proveedor():
    if request.method == 'POST':
        nombre_empresa = request.form.get('nombre_empresa')
        contacto_nombre = request.form.get('contacto_nombre')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        direccion = request.form.get('direccion')

        if not nombre_empresa or not contacto_nombre or not telefono:
            flash('Por favor llena los campos obligatorios (Empresa, Contacto y Teléfono)', 'warning')
            return redirect(url_for('proveedores.nuevo_proveedor'))

        proveedor = Proveedores(
            nombre_empresa=nombre_empresa,
            contacto_nombre=contacto_nombre,
            telefono=telefono,
            email=email,
            direccion=direccion
        )
        proveedor.save()
        
        flash(f'Proveedor "{nombre_empresa}" guardado con éxito', 'success')
        return redirect(url_for('proveedores.listar_proveedores'))
    
    return render_template('proveedores/add.html')
 
@bp.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(id):
    proveedor = Proveedores.query.get_or_404(id)
    
    if request.method == 'POST':
        proveedor.nombre_empresa = request.form.get('nombre_empresa')
        proveedor.contacto_nombre = request.form.get('contacto_nombre')
        proveedor.telefono = request.form.get('telefono')
        proveedor.email = request.form.get('email')
        proveedor.direccion = request.form.get('direccion')
        
        db.session.commit()
        flash('Información del proveedor actualizada', 'info')
        return redirect(url_for('proveedores.listar_proveedores'))
    
    return render_template('proveedores/index.html', proveedor=proveedor)

@bp.route('/proveedores/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_proveedor(id):
    proveedor = Proveedores.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    flash(f'Se ha eliminado a {proveedor.nombre_empresa} de la lista', 'danger')
    return redirect(url_for('proveedores.listar_proveedores'))