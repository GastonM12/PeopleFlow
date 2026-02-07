from flask import Flask
from app.config import DevelopmentConfig
from app.core.database import init_db
from app.routes.user_routes import user_bp
from app.routes.employer_routes import employer_bp
from flask_jwt_extended import JWTManager

from flask_swagger_ui import get_swaggerui_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    init_db()
    
    JWTManager(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(employer_bp)

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "PeopleFlow API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
