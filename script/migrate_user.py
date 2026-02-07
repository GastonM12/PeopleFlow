from mongoengine import connect, get_db
from app.models.user import User
from datetime import datetime
from werkzeug.security import generate_password_hash

def migrate():
    # Conectamos a Mongo
    connect(
        db="peopleflow",
        host="mongo",  # Esto funciona dentro del contenedor Docker
        port=27017
    )

    # Obtenemos el objeto de base de datos
    db = get_db()

    if 'user' not in db.list_collection_names():
        print("No existe la colección 'user'. Creando usuario de prueba...")

        # Creamos admin con password hasheada
        admin = User(
            name="Admin",
            email="admin@admin.com",
            password=generate_password_hash("123456789"),
            rol="admin",  # rol obligatorio
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        admin.save()

    print("Migración completada")


if __name__ == "__main__":
    migrate()
