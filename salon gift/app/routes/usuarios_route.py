from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, abort
from app.models.usuario import User
from flask_login import current_user, login_required
from functools import wraps
from app import db

# Definición del Blueprint
bp = Blueprint('user', __name__, url_prefix='/User')

# --- DECORADOR PARA ADMINISTRADORES ---
# Debe ir fuera de cualquier ruta para poder usarse en todo el blueprint
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificamos si está autenticado Y si tiene el rol de admin
        if not current_user.is_authenticated or getattr(current_user, 'rol', None) != 'admin':
            abort(403)  # Prohibido
        return f(*args, **kwargs)
    return decorated_function

# --- RUTAS PÚBLICAS ---


@bp.route('/inicio')
def inicio(): 
    return render_template('home.html')

# --- RUTAS PRIVADAS (CLIENTE) ---

@bp.route('/dashboard')
@login_required
def index():
    data = User.query.all()
    return render_template('cliente.html', data=data)

@bp.route('/detail/<int:id>')
@login_required
def detail(id):
    user = User.query.get_or_404(id)
    return render_template('users/detail.html', user=user)

# --- RUTAS DE ADMINISTRADOR ---

@bp.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin.html')

@bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    if request.method == 'POST':
        nombreuser = request.form.get('nombreuser')
        password = request.form.get('password') 
        email = request.form.get('email')   
        telefono = request.form.get('telefono')

        if User.query.filter_by(email=email).first():
            flash(f"El correo {email} ya está registrado.", "danger")
            return redirect(url_for('user.add'))    
        
        try:
            # Asegúrate de que los nombres de los atributos coincidan con tu modelo User
            new_user = User(nombreuser=nombreuser, email=email, telefono=telefono)
            new_user.set_password(password) # Método para hashear la contraseña
            db.session.add(new_user)
            db.session.commit()
            flash(f"Usuario {nombreuser} creado con éxito.", "success")
            return redirect(url_for('user.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear usuario: {str(e)}", "danger")
            
    return render_template('users/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        # Nota: He normalizado a 'nombreuser' para que coincida con la ruta 'add'
        user.nombreuser = request.form.get('nombreuser')
        user.email = request.form.get('email')
        user.telefono = request.form.get('telefono')
        
        # Opcional: actualizar contraseña solo si se envía una nueva
        nueva_pass = request.form.get('password')
        if nueva_pass:
            user.set_password(nueva_pass)
            
        db.session.commit()         
        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for('user.index'))

    return render_template('users/edit.html', user=user)

@bp.route('/delete/<int:id>')
@login_required
@admin_required
def delete(id):
    user = User.query.get_or_404(id)    
    db.session.delete(user)
    db.session.commit()
    flash("Usuario eliminado.", "warning")
    return redirect(url_for('user.index'))

# --- API / JSON ---

@bp.route('/js')
def indexjs():
    data = User.query.all()
    result = [user.to_dict() for user in data] 
    return jsonify(result)
