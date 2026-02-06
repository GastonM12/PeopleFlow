from flask import Flask
from app.config import DevelopmentConfig
from app.core.database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    init_db()

    return app

