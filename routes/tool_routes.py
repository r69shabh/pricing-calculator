from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Tool, Section, Component, db

tool_bp = Blueprint('tool', __name__)

@tool_bp.route('/tools', methods=['POST'])
@jwt_required()
def create_tool():
    company_id = get_jwt_identity()
    data = request.get_json()
    
    if not all(k in data for k in ['name', 'version']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    tool = Tool(
        company_id=company_id,
        name=data['name'],
        version=data['version']
    )
    
    db.session.add(tool)
    db.session.commit()
    
    return jsonify({
        'message': 'Tool created successfully',
        'tool_id': tool.id
    }), 201

@tool_bp.route('/tools', methods=['GET'])
@jwt_required()
def get_tools():
    company_id = get_jwt_identity()
    tools = Tool.query.filter_by(company_id=company_id).all()
    
    return jsonify({
        'tools': [{
            'id': tool.id,
            'name': tool.name,
            'version': tool.version,
            'status': tool.status
        } for tool in tools]
    }), 200

@tool_bp.route('/tools/<int:tool_id>', methods=['PUT'])
@jwt_required()
def update_tool(tool_id):
    company_id = get_jwt_identity()
    tool = Tool.query.filter_by(id=tool_id, company_id=company_id).first()
    
    if not tool:
        return jsonify({'error': 'Tool not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        tool.name = data['name']
    if 'version' in data:
        tool.version = data['version']
    if 'status' in data and data['status'] in ['draft', 'live']:
        tool.status = data['status']
    
    db.session.commit()
    
    return jsonify({'message': 'Tool updated successfully'}), 200

@tool_bp.route('/tools/<int:tool_id>', methods=['DELETE'])
@jwt_required()
def delete_tool(tool_id):
    company_id = get_jwt_identity()
    tool = Tool.query.filter_by(id=tool_id, company_id=company_id).first()
    
    if not tool:
        return jsonify({'error': 'Tool not found'}), 404
    
    db.session.delete(tool)
    db.session.commit()
    
    return jsonify({'message': 'Tool deleted successfully'}), 200

@tool_bp.route('/tools/<int:tool_id>/sections', methods=['POST'])
@jwt_required()
def create_section(tool_id):
    company_id = get_jwt_identity()
    tool = Tool.query.filter_by(id=tool_id, company_id=company_id).first()
    
    if not tool:
        return jsonify({'error': 'Tool not found'}), 404
    
    data = request.get_json()
    
    if 'name' not in data:
        return jsonify({'error': 'Missing section name'}), 400
    
    section = Section(
        tool_id=tool_id,
        name=data['name']
    )
    
    db.session.add(section)
    db.session.commit()
    
    return jsonify({
        'message': 'Section created successfully',
        'section_id': section.id
    }), 201

@tool_bp.route('/tools/<int:tool_id>/sections', methods=['GET'])
@jwt_required()
def get_sections(tool_id):
    company_id = get_jwt_identity()
    tool = Tool.query.filter_by(id=tool_id, company_id=company_id).first()
    
    if not tool:
        return jsonify({'error': 'Tool not found'}), 404
    
    sections = Section.query.filter_by(tool_id=tool_id).all()
    return jsonify({
        'sections': [{
            'id': section.id,
            'name': section.name,
            'components': [{
                'id': comp.id,
                'type': comp.type,
                'variant': comp.variant,
                'pricing': comp.pricing
            } for comp in section.components]
        } for section in sections]
    }), 200

@tool_bp.route('/sections/<int:section_id>/components', methods=['POST'])
@jwt_required()
def create_component(section_id):
    data = request.get_json()
    
    if not all(k in data for k in ['type', 'variant', 'pricing']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate pricing structure
    pricing = data['pricing']
    if not isinstance(pricing, dict):
        return jsonify({'error': 'Invalid pricing structure'}), 400
    
    if 'type' not in pricing or pricing['type'] not in ['fixed', 'tiered', 'quantity']:
        return jsonify({'error': 'Invalid pricing type'}), 400
    
    component = Component(
        section_id=section_id,
        type=data['type'],
        variant=data['variant'],
        pricing=pricing
    )
    
    db.session.add(component)
    db.session.commit()
    
    return jsonify({
        'component_id': component.id,
        'type': component.type,
        'variant': component.variant,
        'pricing': component.pricing
    }), 201

@tool_bp.route('/tools/<int:tool_id>/calculate', methods=['POST'])
def calculate_estimate(tool_id):
    tool = Tool.query.filter_by(id=tool_id, status='live').first()
    
    if not tool:
        return jsonify({'error': 'Tool not found or not published'}), 404
    
    data = request.get_json()
    if not data or 'components' not in data:
        return jsonify({'error': 'Missing components data'}), 400
    
    total_cost = 0
    selected_components = []
    
    for comp_data in data['components']:
        if not isinstance(comp_data, dict) or 'id' not in comp_data:
            continue
            
        component = Component.query.get(comp_data['id'])
        if not component or not component.section or component.section.tool_id != tool_id:
            continue
            
        cost = calculate_component_cost(component, comp_data.get('quantity', 1))
        total_cost += cost
        
        selected_components.append({
            'id': component.id,
            'type': component.type,
            'variant': component.variant,
            'cost': cost,
            'pricing': component.pricing
        })
    
    return jsonify({
        'total_cost': total_cost,
        'components': selected_components,
        'currency': 'USD'
    }), 200

def calculate_component_cost(component, quantity=1, features=None):
    pricing = component.pricing
    if not pricing or 'type' not in pricing:
        return 0.0

    if pricing['type'] == 'fixed':
        return float(pricing['amount'])
    
    elif pricing['type'] == 'tiered':
        for tier in pricing['tiers']:
            if quantity <= tier['up_to']:
                return float(tier['price'])
        return float(pricing['tiers'][-1]['price'])
    
    elif pricing['type'] == 'quantity':
        unit_price = float(pricing['unit_price'])
        min_qty = pricing.get('minimum', 1)
        max_qty = pricing.get('maximum', float('inf'))
        actual_qty = max(min_qty, min(quantity, max_qty))
        return unit_price * actual_qty
    
    elif pricing['type'] == 'feature':
        total = float(pricing.get('base_price', 0))
        if features and pricing.get('features'):
            for feature in pricing['features']:
                if feature['name'] in features:
                    total += float(feature['price'])
        return total
    
    return 0.0