from flask import Flask
from mongoengine import connect
import os 

def create_app():
    app = Flask(__name__)
    connect(
        db=os.getenv("MONGO_DB"),
        host=os.getenv("MONGO_HOST"),
        port=os.getenv("MONGO_PORT"),
        username=os.getenv("MONGO_USERNAME"),
        password=os.getenv("MONGO_PASSWORD"),
    )

    from app.routes.user_routes import user_bp
    from app.routes.employer_routes import employer_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(employer_bp)
    return app