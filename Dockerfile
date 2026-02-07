# Usamos Python 3.12 slim para que sea liviano
FROM python:3.12-slim

# Carpeta de trabajo
WORKDIR /app

# Copiamos las dependencias
COPY requirements.txt .

# Actualizamos pip e instalamos las dependencias
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de la app
COPY . .

# Exponemos el puerto que usará Flask
EXPOSE 5000

# Ejecutamos la app como módulo (importando correctamente paquetes)
CMD ["python", "-m", "app.main"]
