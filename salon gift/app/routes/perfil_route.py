from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.usuario import User
from app.models.perfil import Perfil 
from app import db


bp = Blueprint('perfil', __name__, url_prefix='/perfil')

# Listar todos los perfiles
@bp.route('/')
def index():
    perfiles = Perfil.query.all()
    return render_template('perfil/index.html', perfiles=perfiles)

# Crear un nuevo perfil
@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        bio = request.form.get('bio')
        idusuario = request.form.get('idusuario')

        if not nombre or not idusuario:
            flash("El nombre y el usuario son obligatorios", "error")
            return redirect(url_for('perfil.add'))

        nuevo_perfil = Perfil(
            nombre=nombre,
            apellido=apellido,
            bio=bio,
            idusuario=idusuario
        )
        db.session.add(nuevo_perfil)
        db.session.commit()
        flash("Perfil creado exitosamente", "success")
        return redirect(url_for('perfil.index'))

    users = User.query.all()
    return render_template('perfil/add.html', users=users)

# Editar un perfil existente
@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    perfil = Perfil.query.get_or_404(id)

    if request.method == 'POST':
        perfil.nombre = request.form.get('nombre')
        perfil.apellido = request.form.get('apellido')
        perfil.bio = request.form.get('bio')
        db.session.commit()
        flash("Perfil actualizado correctamente", "success")
        return redirect(url_for('perfil.index'))

    return render_template('perfil/edit.html', perfil=perfil)

# Eliminar un perfil
@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    perfil = Perfil.query.get_or_404(id)
    db.session.delete(perfil)
    db.session.commit()
    flash("Perfil eliminado", "info")
    return redirect(url_for('perfil.index'))