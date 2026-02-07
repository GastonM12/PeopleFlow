from flask import Flask
from app.config import DevelopmentConfig
from app.core.database import init_db
from app.routes.user_routes import user_bp
from app.routes.employer_routes import employer_bp
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    init_db()
    
    JWTManager(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(employer_bp)

    return app
