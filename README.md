# PeopleFlow

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

PeopleFlow es una API RESTful para la gestión de empleados y usuarios, desarrollada con Flask y MongoDB. La aplicación está contenerizada con Docker para facilitar su despliegue y desarrollo.

## Características

-   **Gestión de Empleados:** Operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para los empleados.
-   **Gestión de Usuarios:** Registro y autenticación de usuarios con JWT.
-   **Control de Acceso:** Sistema de roles para proteger las rutas (`admin`, `rh`, `usuario`).
-   **Análisis:** Endpoint para calcular el salario promedio.

## Enfoque y Decisiones de Diseño

Al abordar el desarrollo de **PeopleFlow**, identifiqué la **privacidad de los datos** como un requisito no funcional crítico, dada la naturaleza sensible de la información gestionada (salarios y datos personales).

Mi solución se centró en los siguientes pilares:

-   **Seguridad y Privacidad por Diseño:** Implementé un sistema de autenticación obligatorio para evitar la exposición pública de datos confidenciales. No todos los usuarios deben tener acceso a la información financiera de la organización.
-   **Control de Acceso Granular (RBAC):** Diseñé un esquema de permisos donde únicamente los roles de **Admin** y **RRHH (HR)** tienen privilegios para visualizar salarios y realizar operaciones de gestión (Crear, Editar, Eliminar). Esto garantiza la integridad de los datos y protege la privacidad de los empleados frente a accesos no autorizados.
-   **Valor Agregado (Business Intelligence):** Incorporé un endpoint específico para el cálculo automático del **promedio salarial semanal**. Esta funcionalidad permite a la empresa monitorizar sus gastos en nómina de manera eficiente y automatizada, aportando valor más allá de la simple gestión de registros.

## Requisitos Previos

-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

## Instalación y Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/GastonM12/PeopleFlow.git
    cd PeopleFlow
    ```

2.  **Configurar las variables de entorno:**
    Crea un archivo `.env` a partir del archivo de ejemplo `.env.example`:
    ```bash
    cp .env.example .env
    ```
    Abre el archivo `.env` y modifica las variables si es necesario. Asegúrate de cambiar `SECRET_KEY` y `JWT_SECRET_KEY` por valores seguros en un entorno de producción.

    **Importante:** La configuración por defecto de `MONGO_URI` en `docker-compose.yml` está diseñada para funcionar dentro de la red de Docker. La URI `mongodb://mongo:27017/peopleflow` se conectará al contenedor de la base de datos llamado `mongo`. Deberás ajustar tu archivo `.env` para que la aplicación Flask use esta URI:

    ```ini
    MONGO_URI=mongodb://mongo:27017/peopleflow
    ```

## Cómo ejecutar la aplicación

Para construir y levantar los contenedores de la aplicación y la base de datos, ejecuta el siguiente comando:

```bash
docker-compose up --build
```

La API estará disponible en `http://localhost:5000`.

## Documentación (Swagger UI)

Una vez iniciada la aplicación, visita la siguiente URL para ver la documentación interactiva:

http://localhost:5000/api/docs

## Ejecución Manual

Si necesitas ejecutar la aplicación manualmente (fuera de Docker), utiliza el siguiente comando (asegurándote de tener las dependencias instaladas y las variables de entorno configuradas):

```bash
python -m app.main
```

## Ejecutar Migraciones

Después de levantar los contenedores, si necesitas ejecutar migraciones de datos (como la creación inicial de usuarios), sigue estos pasos:

1.  Accede al contenedor de la API:
    ```bash
    docker exec -it peopleflow-api bash
    ```

2.  Una vez dentro, ejecuta el script de migración:
    ```bash
    PYTHONPATH=/app python script/migrate_user.py
    ```
Esto es necesario para que los scripts reconozcan la estructura de directorios de la aplicación.

## Endpoints de la API

A continuación se muestra un resumen de los endpoints disponibles.

### Autenticación de Usuarios (`/api/user`)

-   `POST /register`: Registra un nuevo usuario. Requiere que el email ya exista en la base de datos de empleados. (Público)
-   `POST /login`: Inicia sesión y devuelve un `access_token` y `refresh_token`. (Público)

### Gestión de Empleados (`/api/employer`)

**Nota:** Todos los siguientes endpoints requieren enviar el `access_token` en el header `Authorization: Bearer <token>`.

-   `POST /create`: Crea un nuevo empleado. **(Token requerido - Rol: admin)**
-   `GET /get`: Obtiene una lista paginada de todos los empleados. Se puede filtrar por `puesto`. **(Token requerido - Rol: admin, rh)**
-   `GET /get/<id>`: Obtiene un empleado por su ID. **(Token requerido - Rol: admin, rh, usuario (solo su propia ficha))**
-   `PUT /update/<id>`: Actualiza los datos de un empleado. **(Token requerido - Rol: admin, rh)**
-   `DELETE /delete/<id>`: Elimina un empleado. **(Token requerido - Rol: admin)**
-   `GET /average-salary`: Calcula el salario promedio semanal de todos los empleados. **(Token requerido - Rol: admin, rh)**