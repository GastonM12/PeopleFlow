from datetime import datetime
from mongoengine import Document, StringField, EmailField, DateTimeField, signals
from werkzeug.security import generate_password_hash

class User(Document):
    name = StringField(required=True, max_length=50)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    rol = StringField(required=True, choices=['admin','hr','user'], default='user')
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'user'}

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.updated_at = datetime.utcnow()
        if not document.password.startswith("pbkdf2:sha256") and not document.password.startswith("scrypt:"):
            document.password = generate_password_hash(document.password)

signals.pre_save.connect(User.pre_save, sender=User)