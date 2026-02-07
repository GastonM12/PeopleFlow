from mongoengine import connect
from app.config import DevelopmentConfig
from pymongo import errors

def init_db():
    try:
        connect(host=DevelopmentConfig.MONGO_URI)
        print("Conexión a MongoEngine establecida")
    except errors.ConnectionFailure as e:
        print(f"Error de conexión a MongoEngine: {e}")
        raise