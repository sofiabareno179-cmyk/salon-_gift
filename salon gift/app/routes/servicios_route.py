from flask import Blueprint, request, jsonify,render_template
from app.models.servicios import Servicio 
from app import db

bp = Blueprint('servicio', __name__, url_prefix='/Servicio')

@bp.route('/servicios', methods=['GET'])
def get_servicios():
    servicios = Servicio.query.all()
    return jsonify([s.to_dict() for s in servicios]), 200
@bp.route('/peluqueria')
def ver_peluqueria():
    servicios = Servicio.query.all() 
    return render_template('servicio/peluqueria.html', servicios=servicios)
@bp.route('/Tratamiento')
def tratamientos():
    servicios = Servicio.query.all() 
    return render_template('servicio/tratamiento.html', servicios=servicios)
@bp.route('/Manicure')
def manicure():
    servicios = Servicio.query.all() 
    return render_template('servicio/manicure.html', servicios=servicios)
@bp.route('/servicios/<int:id>', methods=['GET'])
def get_servicio(id):
    servicio = Servicio.query.get_or_404(id)
    return jsonify(servicio.to_dict()), 200

@bp.route('/servicios', methods=['POST'])
def add():
    data = request.get_json()
    
    if not data or 'nombre' not in data or 'precio' not in data:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    nuevo_servicio = Servicio(
        nombre=data['nombre'],
        precio=data['precio'],
        duracion=data['duracion']
    )
    
    try:
        nuevo_servicio.save()
        return jsonify(nuevo_servicio.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@bp.route('/servicios/<int:id>', methods=['PUT'])
def edit(id):
    servicio = Servicio.query.get_or_404(id)
    data = request.get_json()
    
    servicio.nombre = data.get('nombre', servicio.nombre)
    servicio.precio = data.get('precio', servicio.precio)
    servicio.duracion = data.get('duracion', servicio.duracion)
    
    try:
        db.session.commit()
        return jsonify(servicio.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/servicios/<int:id>', methods=['DELETE'])
def delete(id):
    servicio = Servicio.query.get_or_404(id)
    try:
        db.session.delete(servicio)
        db.session.commit()
        return jsonify({"message": "Servicio eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500