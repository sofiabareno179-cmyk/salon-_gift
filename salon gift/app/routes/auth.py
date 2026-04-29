from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import User
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv
load_dotenv()
bp = Blueprint('auth', __name__)
@bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirigir según el rol si ya está logueado
        return redirect(url_for('user.admin_dashboard' if current_user.rol == 'admin' else 'user.index'))

    if request.method == 'POST':
        email_input = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email_input).first()

        if user and user.check_password(password):
            login_user(user)
            flash("¡Inicio de sesión exitoso!", "success")

            # Redirección basada en rol
            if user.rol == 'admin':
                return redirect(url_for('auth.admin_dashboard'))
            else:
                return redirect(url_for('user.index'))
        
        flash('Credenciales inválidas. Inténtalo de nuevo.', 'danger')

    return render_template("login.html")
@bp.route('/dashboard')
@login_required
def dashboard():    
    return f'Welcome, {current_user.email}! This is your dashboard.'

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@bp.route('/register')
def register():
    example_data = {
        'title': 'Bienvenido a Flet',
        'message': 'Este es un mensaje desde Flask.'
    }
    import json
    return json.dumps(example_data)
