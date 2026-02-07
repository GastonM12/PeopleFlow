from mongoengine import connect, get_db
from app.models.user import User
from app.models.employer import Employer
from datetime import datetime

def migrate():
    connect(
        db="peopleflow",
        host="mongo",
        port=27017
    )
    db = get_db()

    if 'employer' not in db.list_collection_names() or db['employer'].count_documents({}) == 0:
        print("Creando empleados de ejemplo...")
        empleados_data = [
            {
                "nombre": "nacho",
                "apellido": "Chief",
                "email": "admin@admin.com",
                "dni": "00000001A",
                "puesto": "CFO",
                "salario": 120000,
                "fecha_ingreso": datetime(2020, 1, 1)
            },
            {
                "nombre": "Recursos",
                "apellido": "Humanos",
                "email": "rh@example.com",
                "dni": "12345678A",
                "puesto": "Recursos Humanos",
                "salario": 60000,
                "fecha_ingreso": datetime(2023, 5, 10)
            },
            {
                "nombre": "Juan",
                "apellido": "Pérez",
                "email": "juan.perez@example.com",
                "dni": "87654321B",
                "puesto": "Desarrollador Backend",
                "salario": 55000,
                "fecha_ingreso": datetime(2024, 1, 15)
            },
            {
                "nombre": "Maria",
                "apellido": "Gomez",
                "email": "maria.gomez@example.com",
                "dni": "11223344C",
                "puesto": "Diseñadora Gráfica",
                "salario": 50000,
                "fecha_ingreso": datetime(2023, 8, 20)
            },
            {
                "nombre": "Carlos",
                "apellido": "Rodriguez",
                "email": "carlos.rodriguez@example.com",
                "dni": "44556677D",
                "puesto": "Analista de Datos",
                "salario": 52000,
                "fecha_ingreso": datetime(2022, 11, 30)
            }
        ]

        for data in empleados_data:
            empleado = Employer(**data)
            empleado.save()
        print(f"{len(empleados_data)} empleados creados.")

    if 'user' not in db.list_collection_names() or db['user'].count_documents({}) == 0:
        print("Creando usuarios de ejemplo...")

        admin = User(
            name="nacho",
            email="admin@admin.com",
            password="supersecretpassword",
            rol="admin"
        )
        admin.save()

        rh_user = User(
            name="Recursos Humanos",
            email="rh@example.com",
            password="password123",
            rol="hr"
        )
        rh_user.save()

        regular_user = User(
            name="Juan Pérez",
            email="juan.perez@example.com",
            password="password123",
            rol="user"
        )
        regular_user.save()
        
        print("Usuarios admin, hr y user creados.")

    print("Migración completada")

if __name__ == "__main__":
    migrate()
