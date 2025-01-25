from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from models import db
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pricing_calculator.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Import routes after db initialization to avoid circular imports
from routes import auth_routes, tool_routes

# Register blueprints
app.register_blueprint(auth_routes.auth_bp)
app.register_blueprint(tool_routes.tool_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Modified this line to explicitly set host and port
    app.run(host='0.0.0.0', port=5001, debug=True)