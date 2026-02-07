from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt

def role_required(required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role')

            if user_role not in required_roles:
                return jsonify({'mensaje': 'Acceso no autorizado. Rol insuficiente.'}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

admin_required = role_required(['admin'])
rh_or_admin_required = role_required(['admin', 'rh'])
user_rh_or_admin_required = role_required(['admin', 'rh', 'usuario'])
