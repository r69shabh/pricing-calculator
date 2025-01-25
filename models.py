from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tools = db.relationship('Tool', backref='company', lazy=True)

    def set_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft or live
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sections = db.relationship('Section', backref='tool', lazy=True)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    components = db.relationship('Component', backref='section', lazy=True)

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    variant = db.Column(db.String(50), nullable=False)
    pricing = db.Column(JSON, nullable=False)  # Stores the pricing structure
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def validate_pricing(self):
        if not isinstance(self.pricing, dict) or 'type' not in self.pricing:
            return False
            
        pricing_type = self.pricing['type']
        
        if pricing_type == 'fixed':
            return 'amount' in self.pricing and 'currency' in self.pricing
            
        elif pricing_type == 'tiered':
            return ('tiers' in self.pricing and 
                   isinstance(self.pricing['tiers'], list) and
                   all('up_to' in tier and 'price' in tier 
                       for tier in self.pricing['tiers']))
            
        elif pricing_type == 'quantity':
            return ('unit_price' in self.pricing and
                   'currency' in self.pricing)
            
        elif pricing_type == 'feature':
            return ('base_price' in self.pricing and
                   'features' in self.pricing and
                   isinstance(self.pricing['features'], list) and
                   all('name' in feature and 'price' in feature 
                       for feature in self.pricing['features']))
        
        return False

    def calculate_cost(self, quantity=1, features=None):
        if not self.validate_pricing():
            return 0.0
            
        pricing_type = self.pricing['type']
        
        if pricing_type == 'fixed':
            return float(self.pricing['amount'])
            
        elif pricing_type == 'tiered':
            for tier in self.pricing['tiers']:
                if quantity <= tier['up_to']:
                    return float(tier['price'])
            return float(self.pricing['tiers'][-1]['price'])
            
        elif pricing_type == 'quantity':
            unit_price = float(self.pricing['unit_price'])
            min_qty = self.pricing.get('minimum', 1)
            max_qty = self.pricing.get('maximum', float('inf'))
            actual_qty = max(min_qty, min(quantity, max_qty))
            return unit_price * actual_qty
            
        elif pricing_type == 'feature':
            total = float(self.pricing.get('base_price', 0))
            if features and self.pricing.get('features'):
                for feature in self.pricing['features']:
                    if feature['name'] in features:
                        total += float(feature['price'])
            return total
            
        return 0.0