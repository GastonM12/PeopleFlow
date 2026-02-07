# PeopleFlow

PeopleFlow es una API RESTful para la gestión de empleados y usuarios, desarrollada con Flask y MongoDB. La aplicación está contenerizada con Docker para facilitar su despliegue y desarrollo.

## Características

-   **Gestión de Empleados:** Operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para los empleados.
-   **Gestión de Usuarios:** Registro y autenticación de usuarios con JWT.
-   **Control de Acceso:** Sistema de roles para proteger las rutas (`admin`, `rh`, `usuario`).
-   **Análisis:** Endpoint para calcular el salario promedio.

## Requisitos Previos

-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

## Instalación y Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
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

## Endpoints de la API

A continuación se muestra un resumen de los endpoints disponibles.

### Autenticación de Usuarios (`/api/user`)

-   `POST /register`: Registra un nuevo usuario. Requiere que el email ya exista en la base de datos de empleados.
-   `POST /login`: Inicia sesión y devuelve un `access_token` y `refresh_token`.

### Gestión de Empleados (`/api/employer`)

-   `POST /create`: Crea un nuevo empleado. **(Rol: admin)**
-   `GET /get`: Obtiene una lista paginada de todos los empleados. Se puede filtrar por `puesto`. **(Rol: admin, rh)**
-   `GET /get/<id>`: Obtiene un empleado por su ID. **(Rol: admin, rh, usuario (solo su propia ficha))**
-   `PUT /update/<id>`: Actualiza los datos de un empleado. **(Rol: admin, rh)**
-   `DELETE /delete/<id>`: Elimina un empleado. **(Rol: admin)**
-   `GET /average-salary`: Calcula el salario promedio semanal de todos los empleados. **(Rol: admin, rh)**