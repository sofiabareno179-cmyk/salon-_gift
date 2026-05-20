from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.usuario import User
from app.models.perfil import Perfil 
from flask_login import login_required, current_user 
from app import db


bp = Blueprint('perfil', __name__, url_prefix='/perfil')

# Listar todos los perfiles
@bp.route('/')
def index():
    perfiles = Perfil.query.all()
    return render_template('perfil/index.html', perfiles=perfiles)
@bp.route('/mi-perfil')
@login_required
def perfil_usuario():
    # Buscamos el perfil que pertenece al ID del usuario logueado
    perfil = Perfil.query.filter_by(idusuario=current_user.idusuario).first()

    # Si no tiene perfil, lo creamos automáticamente
    if not perfil:
        perfil = Perfil(nombre=current_user.nombreuser, apellido=None, bio=None, idusuario=current_user.idusuario)
        db.session.add(perfil)
        db.session.commit()
        flash("Perfil creado automáticamente.", "info")

    # Si existe, cargamos una plantilla que muestre solo sus datos
    return render_template('perfil/ver_perfil.html', perfil=perfil)
# Crear un nuevo perfil
@bp.route('/add', methods=['GET', 'POST'])
@login_required # Importante: nadie puede crear perfil sin estar logueado
def add():
    # Verificación extra: Si ya tiene perfil, no dejarlo crear otro
    perfil_existente = Perfil.query.filter_by(idusuario=current_user.idusuario).first()
    if perfil_existente:
        flash("Ya tienes un perfil creado.", "info")
        return redirect(url_for('perfil.perfil_usuario'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        bio = request.form.get('bio')
        
        # USAMOS EL ID DEL USUARIO LOGUEADO, NO DEL FORMULARIO
        idusuario = current_user.idusuario 

        if not nombre:
            flash("El nombre es obligatorio", "error")
            return redirect(url_for('perfil.add'))

        nuevo_perfil = Perfil(
            nombre=nombre,
            apellido=apellido,
            bio=bio,
            idusuario=idusuario
        )
        
        try:
            db.session.add(nuevo_perfil)
            db.session.commit()
            flash("¡Perfil creado exitosamente!", "success")
            return redirect(url_for('perfil.perfil_usuario')) # Ir a SU perfil
        except Exception as e:
            db.session.rollback()
            flash("Error al crear el perfil. Intenta de nuevo.", "error")


    return render_template('perfil/add.html')
# Editar un perfil existente
@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    perfil = Perfil.query.get_or_404(id)

    if request.method == 'POST':
        nuevo_email = request.form.get('email')
        nuevo_nombreuser = request.form.get('nombreuser')

        if User.query.filter(User.email == nuevo_email, User.idusuario != current_user.idusuario).first():
            flash("Ese correo electrónico ya está registrado por otro usuario.", "danger")
            return redirect(url_for('perfil.edit', id=id))

        if User.query.filter(User.nombreuser == nuevo_nombreuser, User.idusuario != current_user.idusuario).first():
            flash("Ese nombre de usuario ya está en uso.", "danger")
            return redirect(url_for('perfil.edit', id=id))

        perfil.nombre = request.form.get('nombre')
        perfil.apellido = request.form.get('apellido')
        perfil.bio = request.form.get('bio')

        current_user.nombreuser = nuevo_nombreuser
        current_user.email = nuevo_email
        current_user.telefono = request.form.get('telefono')

        db.session.commit()
        flash("Perfil actualizado correctamente", "success")
        return redirect(url_for('perfil.perfil_usuario'))
    return render_template('perfil/edit.html', perfil=perfil)

# Eliminar un perfil
@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    perfil = Perfil.query.get_or_404(id)
    db.session.delete(perfil)
    db.session.commit()
    flash("Perfil eliminado", "info")
    return redirect(url_for('perfil.index'))