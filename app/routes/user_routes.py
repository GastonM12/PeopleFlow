from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.employer import Employer
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/user')

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'mensaje': 'Nombre, email y contraseña son obligatorios'}), 400

    employee = Employer.objects(email=data.get('email')).first()
    if not employee:
        return jsonify({'mensaje': 'El email no está registrado como empleado'}), 400

    if User.objects(email=data.get('email')).first():
        return jsonify({'mensaje': 'El usuario ya existe'}), 400

    # Al ser un registro público, el rol se asigna como 'user' por defecto por seguridad.
    user = User(
        name=data.get('name'),
        email=data.get('email'),
        password=data.get('password'),
        rol='user',
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    user.save()
    return jsonify({'mensaje': 'Usuario creado exitosamente'}), 201


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'mensaje': 'Email y contraseña son obligatorios'}), 400

    user = User.objects(email=data.get('email')).first()
    if not user:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    if not check_password_hash(user.password, data.get('password')):
        return jsonify({'mensaje': 'Contraseña inválida'}), 401

    # Añadimos el rol del usuario como un "claim" adicional en el token
    additional_claims = {"role": user.rol}
    
    # Usamos el ID del usuario/empleado como la identidad del token
    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200

