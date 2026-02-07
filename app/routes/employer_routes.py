import math
import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.models.employer import Employer
from app.core.decorators import admin_required, rh_or_admin_required
from datetime import datetime

employer_bp = Blueprint('employer_bp', __name__, url_prefix='/api/employer')

@employer_bp.route('/create', methods=['POST'])
@jwt_required()
@admin_required
def create_employer():
    data = request.json
    if not data:
        return jsonify({'mensaje': 'Datos requeridos'}), 400
    
    try:
        employer = Employer(
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            email=data.get('email'),
            dni=data.get('dni'),
            puesto=data.get('puesto'),
            salario=data.get('salario'),
            fecha_ingreso=data.get('fecha_ingreso'),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        employer.save()
        return jsonify({'mensaje': 'Empleado creado exitosamente'}), 201
    except Exception as e:
        return jsonify({'mensaje': 'Error al crear empleado', 'error': str(e)}), 400

@employer_bp.route('/get', methods=['GET'])
@jwt_required()
@rh_or_admin_required
def get_employer():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    puesto = request.args.get('puesto', None, type=str)

    if puesto:
        employers_qs = Employer.objects(puesto__icontains=puesto)
    else:
        employers_qs = Employer.objects()

    
    total = employers_qs.count()
    paginated_employers = employers_qs.skip((page - 1) * per_page).limit(per_page)
    
    return jsonify({
        'mensaje': 'Empleados obtenidos exitosamente',
        'data': json.loads(paginated_employers.to_json()),
        'total': total,
        'pages': math.ceil(total / per_page),
        'current_page': page
    }), 200

@employer_bp.route('/get/<id>', methods=['GET'])
@jwt_required()
def get_employer_by_id(id):
    claims = get_jwt()
    user_role = claims.get('role')
    user_id = claims.get('sub')

    if user_role == 'usuario' and user_id != id:
        return jsonify({'mensaje': 'Acceso no autorizado. Solo puedes ver tu propia ficha.'}), 403

    if user_role not in ['admin', 'rh', 'usuario']:
        return jsonify({'mensaje': 'Rol no válido para esta operación.'}), 403

    try:
        employer = Employer.objects(id=id).first()
        if not employer:
            return jsonify({'mensaje': 'Empleado no encontrado'}), 404
        
        return jsonify({'mensaje': 'Empleado obtenido exitosamente', 'data': json.loads(employer.to_json())}), 200
    except Exception as e:
        return jsonify({'mensaje': 'ID inválido o error al buscar', 'error': str(e)}), 400

@employer_bp.route('/update/<id>', methods=['PUT'])
@jwt_required()
@rh_or_admin_required
def update_employer(id):
    data = request.json
    if not data:
        return jsonify({'mensaje': 'Datos requeridos'}), 400
    try:
        employer = Employer.objects(id=id).first()
        if not employer:
            return jsonify({'mensaje': 'Empleado no encontrado'}), 404
        
        data['updated_at'] = datetime.utcnow()
        
        employer.update(**data)
        return jsonify({'mensaje': 'Empleado actualizado exitosamente'}), 200
    except Exception as e:
        return jsonify({'mensaje': 'Error al actualizar empleado', 'error': str(e)}), 400

@employer_bp.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_employer(id):
    try:
        employer = Employer.objects(id=id).first()
        if not employer:
            return jsonify({'mensaje': 'Empleado no encontrado'}), 404
        employer.delete()
        return jsonify({'mensaje': 'Empleado eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'mensaje': 'Error al eliminar empleado', 'error': str(e)}), 400

@employer_bp.route('/average-salary', methods=['GET'])
@jwt_required()
@rh_or_admin_required
def get_average_salary():
    try:
        pipeline = [
            {
                '$group': {
                    '_id': None,
                    'total_salary': {'$sum': '$salario'},
                    'total_employees': {'$sum': 1}
                }
            }
        ]
        result = list(Employer.objects.aggregate(*pipeline))

        if not result:
            return jsonify({'mensaje': 'No se encontraron empleados'}), 404

        data = result[0]
        total_salary = data.get('total_salary', 0)
        total_employees = data.get('total_employees', 1)

        average_salary = (total_salary / total_employees) / 4
        return jsonify({'salario_promedio': average_salary}), 200

    except Exception as e:
        return jsonify({'mensaje': 'Ocurrió un error', 'error': str(e)}), 500