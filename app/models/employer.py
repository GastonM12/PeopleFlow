from datetime import datetime
from mongoengine import Document, StringField, EmailField, FloatField, DateTimeField,signals
from werkzeug.security import generate_password_hash

class Employer(Document):
    nombre = StringField(required=True, max_length=50)
    apellido = StringField(required=True, max_length=50)
    email = EmailField(required=True, unique=True)
    dni = StringField(required=True, unique=True, max_length=20) 
    puesto = StringField(required=True, max_length=50)
    salario = FloatField(required=True, min_value=0)
    fecha_ingreso = DateTimeField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'employer'}