from flask import Blueprint, render_template, request, redirect, url_for, jsonify, send_file,flash
from app.models.usuario import User
from app import db
from io import BytesIO
import base64
import json

bp = Blueprint('user', __name__, url_prefix='/User')

@bp.route('/')
def index():
    data = User.query.all()
    return render_template('users/index.html', data=data)

@bp.route('/js')
def indexjs():
    data = User.query.all()
    result = [user.to_dict() for user in data] 
    return jsonify(result)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombreuser = request.form['nombreuser']
        password = request.form['password'] 
        email=request.form.get('email')   
        telefono=request.form.get('telefono')
        if User.query.filter_by(email=email).first():
            flash(f"El correo {email} ya está registrado.", "danger")
            return redirect(url_for('user.add'))    
        try:
            new_user = User(nombreuser=nombreuser, email=email,password=password,telefono=telefono)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash(f"Usuario {nombreuser} creado con éxito.", "success")
            return redirect(url_for('user.index'))
        except Exception as e:
           db.session.rollback()
           flash(f"Error al crear usuario: {str(e)}", "danger")
        return redirect(url_for('user.add'))
    return render_template('users/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(idusuario):
    user = User.query.get_or_404(idusuario)
    if request.method == 'POST':
        user.nameUser = request.form['nameUser']
        user.email = request.form['email']
        user.telefono=request.form['telefono']
        user.passwordUser = request.form['passwordUser']
        db.session.commit()        
        return redirect(url_for('usuasrio.index'))

    return render_template('users/edit.html', user=user)
@bp.route('/detail/<int:id>')
def detail(id):
    user = User.query.get_or_404(id)
    return render_template('users/detail.html', user=user)

@bp.route('/delete/<int:id>')
def delete(id):
    user = User.query.get_or_404(id)    
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user.index'))
