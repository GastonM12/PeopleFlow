from mongoengine import Document, StringField, EmailField, FloatField, DateTimeField
from app.core.database import db

class User(Document):
    nombre = StringField(required=True, max_length=50)
    apellido = StringField(required=True, max_length=50)
    email = EmailField(required=True, unique=True)
    dni = StringField(required=True, unique=True, max_length=20)
    password = StringField(required=True)  
    puesto = StringField(required=True, max_length=50)
    rol = StringField(required=True, choices=['admin', 'hr', 'user'], default='user')
    salario = FloatField(required=True, min_value=0)
    fecha_ingreso = DateTimeField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'user'}
