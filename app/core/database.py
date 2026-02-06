from pymongo import MongoClient , errors
from app.config import DevelopmentConfig


client = None
db = None


def init_db():
    global client, db

    try:
        client = MongoClient(DevelopmentConfig.MONGO_URI)
        db = client.get_database()
        print(" Conexion a Mongo establecida")

    except errors.ConnectionError as e : 
        print("Error de conexion a Mongo", e)
        raise e
    