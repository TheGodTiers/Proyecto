# Imagen base de Python
FROM python:3.9-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copio requirements desde un nivel arriba (porque Dockerfile está en /login)
COPY ../requirements.txt /app/

# Instalo dependencias
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copio todo el código de la carpeta login al contenedor
COPY . /app/

# Expongo el puerto de FastAPI
EXPOSE 8001

# Comando para correr FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

