from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import Company, db
from email_validator import validate_email, EmailNotValidError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['name', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate email format
    try:
        validate_email(data['email'])
    except EmailNotValidError:
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Check if company already exists
    if Company.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new company
    company = Company(
        name=data['name'],
        email=data['email']
    )
    company.set_password(data['password'])
    
    db.session.add(company)
    db.session.commit()
    
    return jsonify({
        'message': 'Company registered successfully',
        'company_id': company.id
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Missing email or password'}), 400
    
    company = Company.query.filter_by(email=data['email']).first()
    
    if not company or not company.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=company.id)
    
    return jsonify({
        'access_token': access_token,
        'company_id': company.id
    }), 200

@auth_bp.route('/company', methods=['DELETE'])
@jwt_required()
def delete_company():
    company_id = get_jwt_identity()
    company = Company.query.get(company_id)
    
    if not company:
        return jsonify({'error': 'Company not found'}), 404
    
    db.session.delete(company)
    db.session.commit()
    
    return jsonify({'message': 'Company deleted successfully'}), 200